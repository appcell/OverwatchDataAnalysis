from ora.command_line import program
import ora.pool as pool
import logging

def main():
    program.run()

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    pool.initPool()

    main()
