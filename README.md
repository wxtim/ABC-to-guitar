# ABC to Guitar TAB Converter

## Summary

![test](https://github.com/wxtim/ABC-to-guitar/workflows/Test%20with%20pytest/badge.svg)

Take an ABC tune file and convert to guitar tab showing possible string/fret
combinations that will play the required note.

## Installation
This script is very heavily dependent on Lucas Campagnola's pyabc script which
you need to install in your environment.
At present the easiet method for installing this is:
```bash
wget https://github.com/wxtim/pyabc/archive/makepyabc-a-module.zip -O pyabc.zip
unzip pyabc.zip -d 
pip install -e pyabc-makepyabc-a-module

wget https://github.com/wxtim/ABC-to-guitar/archive/master.zip
unzip master.zip
cd ABC-to-guitar-master
```


## Current Command Line usage.

```
usage: abctoguitar.py [-h] [--output OUTPUT] [--maxfret MAXFRET] [--minfret MINFRET] [--testmode] [--transpose TRANSPOSE] [--tuning {EADGBE,DADGBE}] input

Take and ABC file and render possible guitar tabs

positional arguments:
  input                 An ABC file to feed to this script.

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        Name for output file. If unset will replace *.abc with *.tab
  --maxfret MAXFRET, -x MAXFRET
                        The highest fret to allow use of. Default is 5th.
  --minfret MINFRET, -m MINFRET
                        the lowest fret you wish to use. Default is 0.
  --testmode            turns on verbose printing out output
  --transpose TRANSPOSE, -t TRANSPOSE
                        Number of octaves to transpose
  --tuning {EADGBE,DADGBE}
                        Guitar tunings.


```

Tim Pillinger, 2019
based on the work of
Luke Campagnola, 2014

# Licence
[GNU GPL3](LICENSE)
