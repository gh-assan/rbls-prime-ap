"""Compile actual CUDA device functions as C++; this does not test a GPU launch."""
import ast
from pathlib import Path
import random
import re
import shutil
import subprocess

import pytest
from sympy import isprime

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ['rbls_gpu_pipeline.py', 'rbls_gpu_pipeline_ap8.py',
           'rbls_gpu_pipeline_ap8_opt.py', 'rbls_gpu_pipeline_ap9.py',
           'rbls_gpu_pipeline_ap28.py', 'bench_ap9.py', 'bench_gpu.py',
           'test_prime_kernel.py', 'test_ap_finder.py']


@pytest.mark.parametrize('filename', SOURCES)
def test_device_arithmetic_with_host_compiler(filename, tmp_path):
    compiler = shutil.which('c++')
    if not compiler:
        pytest.skip('C++ compiler unavailable; CUDA hardware is not required')
    tree = ast.parse((ROOT / filename).read_text())
    snippets = [node.value for node in ast.walk(tree) if isinstance(node, ast.Constant)
                and isinstance(node.value, str) and '__device__' in node.value]
    for number, snippet in enumerate(snippets):
        functions = snippet.split('__global__')[0].replace('__device__', '')
        function_name = 'is_prime_fast' if 'bool is_prime_fast' in functions else 'is_prime'
        functions = re.sub(r'__forceinline__', 'inline', functions)
        code = '#include <iostream>\n' + functions + '''
int main() {
    unsigned long long a,b,m;
    while (std::cin >> a >> b >> m) {
        std::cout << mul_mod(a,b,m) << " " << '''+function_name+'''(m) << "\\n";
    }
}
'''
        source = tmp_path / f'kernel{number}.cpp'
        binary = tmp_path / f'kernel{number}'
        source.write_text(code)
        subprocess.run([compiler,'-std=c++11','-O2',str(source),'-o',str(binary)],check=True,
                       capture_output=True)
        rng = random.Random(281)
        samples = [(2**64-60, 2**64-60, 2**64-59), (2**63-1,2**63-1,2**64-59)]
        samples += [(rng.randrange(2**64),rng.randrange(2**64),rng.randrange(1,2**64))
                    for _ in range(100)]
        samples += [(1,1,n) for n in [1,2,3,37,41,2**63-25,2**64-1,3825123056546413051]]
        payload=''.join(f'{a} {b} {m}\n' for a,b,m in samples)
        result=subprocess.run([str(binary)],input=payload,text=True,capture_output=True,check=True)
        for line,(a,b,m) in zip(result.stdout.splitlines(),samples):
            actual, prime=map(int,line.split())
            assert actual == a*b % m
            assert bool(prime) == bool(isprime(m))
        assert len(result.stdout.splitlines()) == len(samples)
