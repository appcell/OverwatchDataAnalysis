import ora.pool as pool
from ora.cml import MSG
from sys import argv


def main():
    if 'help' in argv:
        print(MSG.get('help'))
        exit(0)
    if 'help1' in argv:
        print(MSG.get('help1'))
        exit(0)
    if 'help2' in argv:
        print(MSG.get('help2'))
        exit(0)
    if '--json1' in argv:
        print(MSG.get('json1'))
        exit(0)

    length = len(argv)
    if length == 1:
        print(MSG.get('help'))
        exit(0)
    elif length == 2:
        from ora.cmd_json import program
        program.run()
    else:
        from ora.command_line import program
        program.run()

if __name__ == '__main__':
    pool.initPool()

    main()