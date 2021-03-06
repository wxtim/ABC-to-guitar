#!/usr/bin/env python3
# Convert simple ABC files into guitar notation.

import pyabc
import argparse


def get_args():
    # Get Import args
    parser = argparse.ArgumentParser(
        description="Take and ABC file and render possible guitar tabs")
    parser.add_argument("input", type=str,
                        help="An ABC file to feed to this script.")
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help=(
            "Name for output file. If unset will replace *.abc"
            " with *.tab"
        )
    )
    parser.add_argument(
        "--maxfret", "-x",
        type=int,
        default=5,
        help="The highest fret to allow use of. Default is 5th."
    )
    parser.add_argument(
        "--minfret", "-m",
        type=int,
        default=0,
        help="the lowest fret you wish to use. Default is 0."
    )
    parser.add_argument(
        "--testmode",
        action="store_true",
        help="turns on verbose printing out output"
    )
    parser.add_argument(
        "--transpose", '-t',
        type=int,
        default=0,
        help=('Number of octaves to transpose')
    )
    parser.add_argument(
        "--tuning",
        type=str,
        choices=["EADGBE", "DADGBE"],
        default='DADGBE',
        help="Guitar tunings."
    )
    args = parser.parse_args()
    return args


def output_filename(input_filename, output_filename=None):
    # Creates a sensible filename for programme output
    # @TODO refactor to not need all args.
    if output_filename:
        return output_filename
    else:
        if input_filename[-4:].lower() == ".abc":
            return input_filename[:-4] + ".tab"
        else:
            return input_filename + ".tab"


# Setup the Tuning
DADGAD = [pyabc.Pitch('D', -1),
          pyabc.Pitch('A', -1),
          pyabc.Pitch('D', 0),
          pyabc.Pitch('G', 0),
          pyabc.Pitch('A', 0),
          pyabc.Pitch('D', 1)]
DADGAD.reverse()
EADGBE = [pyabc.Pitch('E', -1),
          pyabc.Pitch('A', -1),
          pyabc.Pitch('D', 0),
          pyabc.Pitch('G', 0),
          pyabc.Pitch('B', 0),
          pyabc.Pitch('E', 1)]
EADGBE.reverse()
TUNINGS = [EADGBE, DADGAD]


def setup_strings(tuning, maxfret=5, minfret=0):
    """
    Create a data structure representing all the playable notes

    Args:
        tuning (list of pyabc.Pitch):
            representing all the strings 0th fret note
        maxfret (int):
            the highest fret the guitarist is willing to use
        minfret (int):
            the lowest fret the guitarist is willing to use.
            @TODO -not yet implemented

    Returns:
        strings (dict):
            Nested dictionaries wit the form:
                {string: {fret: note_int}}
    """
    strings = {}
    for i, string in enumerate(tuning):
        frets = {}
        for fret in range(minfret, maxfret):
            frets[fret + string.abs_value] = fret
        strings[i + 1] = frets
    return strings


def main():
    args = get_args()

    # Open input file
    with open(args.input, 'r') as fhandle:
        RAW_TUNE = fhandle.read()

    # Parse the tune using pyabc
    try:
        tune = pyabc.Tune(RAW_TUNE)
    except KeyError:
        tune = pyabc.Tune("X:0\n" + RAW_TUNE)

    if args.tuning == 'EADGBE':
        tuning = EADGBE
    else:
        tuning = DADGAD
    strings = setup_strings(tuning, args.maxfret, args.minfret)
    # Memoize this?
    possible_tabs = []
    for note in tune.tokens:
        if type(note) == pyabc.Beam:
            x = [note._text for i in range(6)]
            possible_tabs.append(x)
        elif type(note) != pyabc.Note:
            pass
        else:
            note.octave += args.transpose
            options = []
            for gstring in strings.values():
                if note.pitch.abs_value in gstring.keys():
                    options.append("{}".format(gstring[note.pitch.abs_value]))
                else:
                    options.append("")

            possible_tabs.append(options)

    import numpy as np
    notation = np.array(possible_tabs).T
    # print(notation)

    str_outs = []
    for line in notation:
        str_out = ''

        for i in line:
            if len(i) == 0:
                str_out += ("----")
            else:
                str_out += f"-{i:2s}-"

        bars = [bar for bar in str_out.split('|')]
        bargroups = []

        for i in range(0, len(bars), 4):
            bargroups.append('|' + '|'.join(bars[i: i+4]) + '|')

        str_outs.append(bargroups)

    # Finsh off and write a file, if that's what's been asked for.
    final_out = str(np.array(str_outs).T)
    if args.output:
        with open(args.output, 'w') as fhandle:
            fhandle.write(final_out)
    else:
        with open(output_filename(args.input, args.output), 'w') as fhandle:
            fhandle.write(final_out)

    if args.testmode:
        print(final_out)


if __name__ == '__main__':
    main()
