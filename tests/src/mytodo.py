#!/usr/bin/env python
# encoding: utf-8

"""
Simple python script implementing todo management used to demonstrate and test bbtest.
"""

import os
import sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


version = 0.1


todo_file = None


def main(args=None):

    """ A simple and extensible script for managing your todo.txt file. """
    program_version = "v%s" % version
    program_version_message = '%%(prog)s %s' % (program_version)
    description = '''A simple and extensible script for managing your todo.txt file.'''

    # Setup argument parser
    parser = ArgumentParser(description=description,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-V', '--version', action='version', version=program_version_message)

    subparsers = parser.add_subparsers(help='type "todo [subcommand] -h" for help.')

    # add sub-parser
    add_convert = subparsers.add_parser('add', formatter_class=ArgumentDefaultsHelpFormatter)
    add_convert.set_defaults(func=add_todo)
    add_convert.add_argument('todo', nargs=1, metavar='todo',
                             help='Add todo to the end of the list')

    # del sub-parser
    add_convert = subparsers.add_parser('del', formatter_class=ArgumentDefaultsHelpFormatter)
    add_convert.set_defaults(func=del_todo)
    add_convert.add_argument('todo', nargs=1, metavar='todo',
                             help='Delete todo from the list')

    # list sub-parser
    load_analyze = subparsers.add_parser('list', formatter_class=ArgumentDefaultsHelpFormatter)
    load_analyze.set_defaults(func=list_todos)

    # nothing sub-parser
    load_analyze = subparsers.add_parser('nothing', formatter_class=ArgumentDefaultsHelpFormatter)
    load_analyze.set_defaults(func=do_nothing)

    # Process arguments
    parsed_args = parser.parse_args(args)

    parsed_args.func(parsed_args)


def add_todo(parsed_args):

    if not parsed_args.todo[0]:
        sys.exit('empty TODO is not supported')

    with open(todo_file, 'a+') as f:
        f.write(f'{parsed_args.todo[0]}\n')


def del_todo(parsed_args):

    with open(todo_file, 'r+') as f:
        todos = [l.strip() for l in f.readlines()]
    if parsed_args.todo[0] in todos:
        todos.remove(parsed_args.todo[0])
    if not todos:
        os.remove(todo_file)
        return
    with open(todo_file, 'w+') as f:
        f.writelines('\n'.join(todos))


def list_todos(parsed_args):

    if not os.path.isfile(todo_file):
        return []
    with open(todo_file, 'r+') as f:
        todos = [t.strip() for t in f.readlines()]
    print('\n'.join(todos))

def do_nothing(parsed_args):
    return


if __name__ == "__main__":
    todo_file = os.path.join(os.path.dirname(__file__), 'todo.txt')
    sys.exit(main((sys.argv[1:])))
