import ora.gui as Gui
import ora.pool as pool

def main():
    Gui.gui_instance.show()

if __name__ == '__main__':
    pool.initPool()

    main()
