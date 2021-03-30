#!/usr/bin/python3
"""
fhash is a simple python tool for generating, passing and formatting hash
values. It can be used to print hashes of strings or files in various FORMATS
including as a hex string (lower and uppercase), binary string, or decimal
number. It can also be used for testing the speed of these various functions

"""
import os
import sys
import locale
import hashlib
import argparse
import time

# Defines the basic options and constants used
ALGOS = ['md5', 'sha1', 'sha2', 'sha3']
SIZES = [224, 256, 384, 512]
FORMATS = ['lowercase', 'uppercase', 'binary', 'decimal']
os_encoding = locale.getpreferredencoding()

# For sha256 and sha3 only
DEFAULT_SIZE = 256

# For the verbose option, enables warning and error messages
VERBOSE = False

# For splitting data into chunks for larger files for accurate hash values
BUFF_SIZE = 2048

# For handling directories
DIR_ERROR = 'Error: "{}" specified is a directory.'


def check_function(func, size):
    """Specifies the size in bits of the chosen function.
    If the user put in a invalid length, throw an error
    Returns the default length if no size is provided
    @func: the hash function use (md5, sha1, sha2, sha3)
    @size: the desired length of the output. i.e. sha256
            outputs a message of 256 bits or 64 hex-digits
    """
    if (func in ALGOS[0:2]):
        bsize = 160 if (ALGOS.index(func)) else 128
        if (size == None):
            v_print('Using default message size of \
                    {} bits'.format(bsize))
        else:
            v_print('Warning: "size" option is ignored for  \
                    sha1 and md5 since they are fixed-length')
            v_print('Using message size of {} bits'.format(bsize))
        return bsize
    else:
        if (size == None):
            v_print('Using default message size, 256-bits')
            return DEFAULT_SIZE
        elif (size not in SIZES):
            print('Error: Message size must be  \
            224, 256, 384, or 512 for {}'.format(func))
            sys.exit()
        else:
            v_print('Using message size of {} bits'.format(size))
            return size


def format_output(msg, fmt):
    """FORMATS the hash value according to the user's choice
    @msg: the string to be formatted
    @fmt: the target format
    """
    if (fmt == 'lowercase'):
        return msg.lower()
    elif (fmt == 'uppercase'):
        return msg.upper()
    elif (fmt == 'binary'):
        # Omit the trailing 0b
        return '{}'.format(bin(int(msg, 16))[2:].zfill(8))
    elif (fmt == 'decimal'):
        return str(int(msg, 16))
    else:
        print('You somehow passed an invalid format. Please file a bug report')
        sys.exit()


def get_algorithm(func, size):
    """Returns the requested hash function "func" at the specified "size"
    (if it applies)
    @func: the hash function use (md5, sha1, sha2, sha3)
    @size: the desired length of the output. i.e. sha256
            outputs a message of 256 bits or 64 hex-digits
    """
    if (func == 'md5'):
        return hashlib.md5()
    elif(func == 'sha1'):
        return hashlib.sha1()
    elif (func == 'sha2'):
        return eval('hashlib.sha' + str(size) + '()')
    elif (func == 'sha3'):
        return eval('hashlib.sha3_' + str(size) + '()')
    else:
        print('You somehow passed an invalid function, \
        which should not happen.'
              'Please file a bug report at https://github.com/mjfernez/fhash')
        print('Quitting...')
        sys.exit()


def get_hash(msg, algo):
    """The core hasing function.
    This takes an input string or file "msg" and hashes it with "algo"
    @msg: the string or file to be hashed
    @algo: the hashing algorithm to use
    """
    hasher = algo
    if (os.path.isfile(msg)):
        with open(msg, 'rb') as f:
            while True:
                buf = f.read(BUFF_SIZE)

                # If there's no data read into the buffer, EOF
                if not buf:
                    break
                hasher.update(buf)
    else:
        buf = msg
        hasher.update(buf.encode(os_encoding))
    return hasher.hexdigest()


def get_options(args=sys.argv[1:]):
    """Sets up the tool to parse arguments correctly
    (help menu is added by default)
    @args: all arguments inputted by the user
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input',
                        nargs='+',
                        required=True,
                        help='Input file or text. \
                        Try using sha2 -i "Hello, World!"'
                        )
    parser.add_argument('-o', '--output',
                        nargs='?',
                        default=None,
                        help='Destination file to save to. '
                        'Prints to screen if none specified. '
                        'You can save a comma separated list '
                        'of files and hashes by specifying the '
                        'file extension ".csv", otherwise saves hash values \
                        only as text')
    parser.add_argument('-s', '--size',
                        default=None,
                        type=int,
                        help='Message length in bytes 224, 256, 384, 512 '
                        '(only valid for sha 2 and 3).')
    parser.add_argument('-f', '--format',
                        choices=FORMATS,
                        default=FORMATS[0],
                        help='Formatting for the output')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='Optionally add additional information to the \
                        output. Without this flag, the program will just \
                        print the hash')
    parser.add_argument('function',
                        choices=ALGOS,
                        help='Use the specified hash function')

    return parser.parse_args(args)


def save_output(hashes, output):
    """Saves one or more hashes to file. Overwrites the file if it exists
    @hashes: the hash or list of hashes to be saved
    @output: the output destination specified by the user
                (expects a file or "None" to print to screen)
    """
    while (os.path.isfile(output)):
        opt = input('That file exists. Ok to overwrite? (y/n): ')
        if (opt.lower() in ['y', 'yes']):
            break
        elif (opt.lower() in ['n', 'no']):
            output = input('Ok, type the new file name or file path: ')
        else:
            pass

    with open(output, 'w+') as f:
        f.seek(0)
        for h in hashes:
            f.write(h + '\n')
        f.truncate()
    print('File {} created!'.format(output))


# v_print is a function conditionally defined if the user passes the verbose
# option.
# This is preferable to writing "if (VERBOSE)" everytime we need to print error
# info
v_print = None


def main():
    start = time.perf_counter()
    opts = get_options(sys.argv[1:])
    inp = opts.input
    out = opts.output
    func = opts.function
    size = opts.size
    fmt = opts.format
    VERBOSE = opts.verbose

    if (inp == None):
        print('Error: No input given')
        sys.exit()

    if VERBOSE:
        def _v_print(arg):
            print(arg)
    else:
        _v_print = lambda *a: None  # do nothing

    global v_print
    v_print = _v_print

    # Check to make sure size and function inputs are valid
    size = check_function(func, size)

    # If the user chose to output to a file/directory
    if (out != None):
        if os.path.isdir(out):
            print(DIR_ERROR.format(out) + ' Output must be a file.')
            sys.exit()

    # Go through the list of arguments provided by the user after the -i option
    # Remove directories
    for i in inp:
        if os.path.isdir(i):
            print(DIR_ERROR.format(i))
            inp.remove(i)

   # After going through the list, check to see if there are any files to hash
   # Really not the most elegant way to do this... consider refactoring
    if (inp == None):
        print('Error: No files in input!')
        sys.exit()

    hashes = []
    last_clock = time.perf_counter_ns()
    for j in inp:
        v_print('Calculating {} hash for "{}"...'.format(func, j))
        md = get_hash(j, get_algorithm(func, size))
        formatted = format_output(md, fmt)
        hashes.append(formatted)
        if(out == None):
            print(formatted)

        curr_clock = time.perf_counter_ns()
        v_print('Completed in {}ns'.format(curr_clock - last_clock))
        last_clock = curr_clock

    if (out != None):
        if(out.endswith('.csv')):
            save_output(['{}, {}'.format(i, j)
                         for i, j in zip(inp, hashes)], out)
        else:
            save_output(hashes, out)

    end = time.perf_counter()
    v_print('The job took {}s total'.format(end - start))


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt):
        print('\nUser stopped the program')
        sys.exit()
