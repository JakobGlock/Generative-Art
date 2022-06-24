#! venv/bin/python

"""
Generate - Tool for running scripts

Usage:
  generate project (new | delete) <name>
  generate artwork new <name> [--number=<n>] [--open] [--svg] [--twitter]
  generate artwork random [--number=<n>] [--open] [--svg] [--twitter]
  generate artwork all [--open] [--svg]
  generate list

Options:
  -h --help             Show this screen.
  -n --number=<n>       Number of images to generate [default: 1].
  -o --open             Open the file, in an image viewer (Linux only) [default: False].
  --svg                 Create an SVG file [default: False].
  --twitter             Post to output image to Twitter [default: False].
"""

from docopt import docopt
import subprocess
import glob
import random
import os
import shutil

python_path = 'venv/bin/python'
dashes = "".join(["-" for x in range(0, 81)])


def print_msg(typ, msg):
    print(dashes)
    print(" ".join([typ + ":", msg]))
    print(dashes)


def run_script(filename, open_file, file_format, twitter_post):
    subprocess.call([python_path, filename, open_file, file_format, twitter_post])


def check_filename(args):
    filename = args['<name>']
    if not filename.endswith(".py"):
        print_msg("ERROR", "Filename must end with .py")
        exit()

    elif os.path.isfile(filename) and not args['delete'] and not args['artwork']:
        print_msg("ERROR", "File already exists, pick another name")
        exit()

    elif not os.path.isfile(filename) and args['delete']:
        print_msg("ERROR", "File {} does not exist, pick a valid name".format(filename))
        exit()

    return filename


def projects(args):
    filename = check_filename(args)
    if args['new']:
        shutil.copy2("templates/basic.py", filename)
        print_msg("INFO", "Generated new project {}".format(filename))

    elif args['delete']:
        print("")
        x = input("WARNING: Are you REALLY sure you want to delete {} and all images (e.g. Y|N or y|n)? ".format(filename))
        if x == "Y" or x == "y":
            print_msg("INFO", "Deleting script and related image folder")
            os.remove(filename)

            f = os.path.splitext(filename)[0]
            path = "Images/{}".format(f)
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                print_msg("ERROR", "Directory {} does not exist, skipping".format(path))
        else:
            exit()


def artworks(args):
    filename = None
    if args['<name>']:
        filename = check_filename(args)
    number = int(args['--number'])
    open_file = str(args['--open'])
    file_format = str(args['--svg'])
    twitter_post = str(args['--twitter'])

    if filename and args['new']:
        for i in range(0, number):
            run_script(filename, open_file, file_format, twitter_post)

    elif args['random']:
        for i in range(0, number):
            files = glob.glob('*.py')
            filename = random.choice(files)
            run_script(filename, open_file, file_format, twitter_post)

    elif args['all']:
        files = glob.glob('*.py')
        for filename in files:
            run_script(filename, open_file, file_format, twitter_post)


def list_projects(args):
    files = glob.glob('*.py')
    print_msg("INFO", "List of Projects")
    for filename in files:
        print(filename)
    print(dashes)


def main(args):
    if args['project']:
        projects(args)

    elif args['artwork']:
        artworks(args)

    elif args['list']:
        list_projects(args)


if __name__ == '__main__':
    args = docopt(__doc__, version='Generate 0.0.1')
    main(args)
