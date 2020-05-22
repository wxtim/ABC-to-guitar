# Test module for abctoguitar

from abctoguitar import *
import pytest

@pytest.mark.parametrize(
    'ifilename, oufilename, result',
    [
        ('hello.abc', '', 'hello.tab'),
        ('hello.abc', 'my_output.tab', 'my_output.tab'),
        ('hello.ABC', '', 'hello.tab'),
        ('hello', '', 'hello.tab'),
        ('hello.xml', '', 'hello.xml.tab')
    ]
)
def test_output_filename(ifilename, oufilename, result):
    assert output_filename(ifilename, oufilename) == result
    

@pytest.mark.parametrize(
    'tuning, maxfret, minfret, result',
    [
        (DADGAD, 5, 0, {-10: 0, -9: 1, -8: 2, -7: 3, -6: 4}),
        (DADGAD, 6, 1, {-9: 1, -8: 2, -7: 3, -6: 4, -5: 5}),
        (EADGBE, 5, 0, {-8: 0, -7: 1, -6: 2, -5: 3, -4: 4}),   
    ]
)
def test_setup_strings(tuning, maxfret, minfret, result):
    strings = setup_strings(tuning, maxfret, minfret)
    assert strings[6] == result
