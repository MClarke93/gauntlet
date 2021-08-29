# Gauntlet

This application is a basic Python clone of an older Java application used by the gauntlet crew on [GameFAQs' Contest Board](https://gamefaqs.gamespot.com/boards/8-gamefaqs-contests) for ranking things. I created it as part of learning how to use [tkinter](https://docs.python.org/3/library/tkinter.html).

Additional functionality may be added in future if time permits. Things that can still be done:
* Add a 'start screen' that lets the user select which image folder to use.
* Add an option to the GUI to allow the user to change how many losses are required to eliminate a participant.
* Add support for N-way matches, as opposed to always being 2-way.
* Output match history, in addition to the results.
* Clean up documentation.

Usage:
1. Install [Python 3.9](https://www.python.org/downloads/).
2. Clone this repo and open the project's root folder in a command line.
3. Install the requirements using `pip install -r requirements.txt`.
4. Run the app using `python main.py`.
5. The app will use images placed in the `/img` directory as the participants.
