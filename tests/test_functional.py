# Functional tests of abctoguitar

from subprocess import Popen, PIPE
from shlex import split
import pytest


@pytest.mark.parametrize(
    "command, stdout, stderr",
    [
        (
            "./abctoguitar.py",
            b"",
            (
                b"usage: abctoguitar.py [-h] [--output OUTPUT] "
                b"[--maxfret MAXFRET]\n                      "
                b"[--minfret MINFRET] [--testmode] [--transpose TRANSPOSE]\n"
                b"                      input\nabctoguitar.py: error: the "
                b"following arguments are required: input\n"
            ),
        ),
        (
            "./abctoguitar.py tests/example.abc",
            b'|:E2c cBA|FAF E3|E2c cBA|cde B3:|\n',
            b""
        ),
        (
            "./abctoguitar.py tests/example.abc --testmode",
            (b"""|:E2c cBA|FAF E3|E2c cBA|cde B3:|
[['|-|:----------------------| ------------------| ----------------------|'
  '|-|:------4 --4 --2 --0 --| ------0 ----------| ------4 --4 --2 --0 --|'
  '|-|:--------------4 --2 --| ------2 ----------| --------------4 --2 --|'
  '|-|:--2 ------------------| --4 ------4 --2 --| --2 ------------------|'
  '|-|:----------------------| ------------------| ----------------------|'
  '|-|:----------------------| ------------------| ----------------------|']
 ['| ------0 --2 ------:|-|' '| --4 ----------2 --:|-|'
  '| --------------4 --:|-|' '| ------------------:|-|'
  '| ------------------:|-|' '| ------------------:|-|']]
"""
            ),
            b''
        ),
        (
            "./abctoguitar.py tests/example.abc --testmode --maxfret 12",
            (b"""|:E2c cBA|FAF E3|E2c cBA|cde B3:|
[['|-|:----------------------| ------------------| ----------------------|'
  '|-|:------4 --4 --2 --0 --| ------0 ----------| ------4 --4 --2 --0 --|'
  '|-|:------6 --6 --4 --2 --| ------2 ----------| ------6 --6 --4 --2 --|'
  '|-|:--2 --11--11--9 --7 --| --4 --7 --4 --2 --| --2 --11--11--9 --7 --|'
  '|-|:--7 ------------------| --9 ------9 --7 --| --7 ------------------|'
  '|-|:----------------------| ------------------| ----------------------|']
 ['| ------0 --2 ------:|-|' '| --4 --5 --7 --2 --:|-|'
  '| --6 --7 --9 --4 --:|-|' '| --11----------9 --:|-|'
  '| ------------------:|-|' '| ------------------:|-|']]
"""
            ),
            b''
        ), 
    ],
)
def test_no_args(command, stdout, stderr):
    result = Popen(split(command), stdout=PIPE, stderr=PIPE)
    # breakpoint()
    assert result.stderr.read() == stderr
    assert result.stdout.read() == stdout
