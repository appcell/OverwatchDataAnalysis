from ora.command_line import program
import ora.pool as pool


def main():
    program.run()

if __name__ == '__main__':
    pool.initPool()

    main()
