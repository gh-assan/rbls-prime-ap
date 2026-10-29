import json

import pytest

from search_prime_ap import main


def test_cli_writes_complete_search_result(tmp_path,capsys):
    path=tmp_path/'run.json'
    assert main(['--start','2','--count','98','--k','3','--difference','6',
                 '--output',str(path)])==0
    payload=json.loads(capsys.readouterr().out)
    assert json.loads(path.read_text())==payload
    assert payload['raw_starts']==98
    assert 5 in payload['matches']


def test_invalid_cli_does_not_write_result(tmp_path):
    path=tmp_path/'invalid.json'
    with pytest.raises(SystemExit) as error:
        main(['--start','2','--count','-1','--output',str(path)])
    assert error.value.code==2
    assert not path.exists()
