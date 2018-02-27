import ora.gui as Gui
import ora.pool as pool
import multiprocessing as mp

def main():
    Gui.gui_instance.show()

if __name__ == '__main__':
    mp.set_start_method('spawn')
    pool.initPool()

    main()