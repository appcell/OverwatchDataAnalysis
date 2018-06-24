import ora.gui as Gui
import multiprocessing as mp

def main():
    Gui.gui_instance.show()

if __name__ == '__main__':
    mp.freeze_support()
    main()