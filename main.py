import sys

from gauntlet import Gauntlet
from interface import GUI

# ----------------------------------------------------------------------------

if __name__ == "__main__":
    gauntlet = Gauntlet(chances = 2)
    gui = GUI(gauntlet = gauntlet)
    gui.run()
    sys.exit(0)

# ----------------------------------------------------------------------------