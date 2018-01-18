import time
from ora.game import Game
from ora.gui import Gui

def main():
    gui = Gui()
    gui.info()
    gui.show()


if __name__ == '__main__':
    main()
    # T = time.time()
    # print "time:", time.time() - T