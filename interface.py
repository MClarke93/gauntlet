import os
import tkinter as tk

from PIL import Image, ImageTk

from gauntlet import Gauntlet, HOME_DIR

# ----------------------------------------------------------------------------

VALID_EXTENSIONS = [".bmp", ".gif", ".jpg", ".jpeg", ".png", ".tiff"]

# ----------------------------------------------------------------------------

class GUI(tk.Tk):
    def __init__(self, gauntlet: Gauntlet):
        '''Constructs a GUI object.'''
        super().__init__()
        self.gauntlet = gauntlet
        self._prepare_gauntlet()
        self._prepare_gui()
        self._run_match()

    def _prepare_gauntlet(self):
        '''Prepares the gauntlet.'''
        self.gauntlet.gladiator_load(os.path.join(HOME_DIR, "img"),
        VALID_EXTENSIONS)
    
    def _prepare_gui(self):
        '''Prepares the root window.'''
        self.title("Gauntlet")
        self.geometry("640x480")
        self.resizable(width = False, height = False)
    
    def _clear(self):
        '''Clears the root window of widgets.'''
        for slave in self.slaves():
            slave.destroy()
    
    def _display_match(self):
        '''Displays/refreshes the match screen.'''
        left_gladiator, right_gladiator = self.gauntlet.match.gladiators

        left_image = Image.open(left_gladiator.path)
        left_image.thumbnail((240,240))
        left_image = ImageTk.PhotoImage(left_image)
        right_image = Image.open(right_gladiator.path)
        right_image.thumbnail((240,240))
        right_image = ImageTk.PhotoImage(right_image)

        self._clear()

        frame_match = tk.Frame(master=self, background="gray20")
        frame_match.rowconfigure(0, weight=1)
        frame_match.columnconfigure(0, weight=1)
        frame_match.columnconfigure(1, weight=3)
        frame_match.columnconfigure(2, weight=1)

        frame_left = tk.Frame(master=frame_match, background="gray20")
        frame_left.rowconfigure(0, weight=6)
        frame_left.rowconfigure(1, weight=1)
        frame_left.columnconfigure(0, weight=1)

        frame_mid = tk.Frame(master=frame_match, background="gray20")
        frame_mid.rowconfigure(0, weight=1)
        frame_mid.columnconfigure(0, weight=1)

        frame_right = tk.Frame(master=frame_match, background="gray20")
        frame_right.rowconfigure(0, weight=6)
        frame_right.rowconfigure(1, weight=1)
        frame_right.columnconfigure(0, weight=1)

        button_gladiator_left = tk.Button(master=frame_left, 
        image=left_image, bd=0, background="gray20", 
        activebackground="gray20", command=lambda: self._press_gladiator(0))
        
        label_gladiator_left = tk.Label(master=frame_left, 
        text=(f"{left_gladiator.name} [{left_gladiator.wins}W/"
        f"{left_gladiator.losses}L]"), font="Arial 11 bold", 
        background="gray20", foreground="white", height=1, width=30, 
        wraplength=240)

        label_mid = tk.Label(master=frame_mid, text="VS", 
        font="Arial 24 bold", background="gray20", foreground="white")

        button_gladiator_right = tk.Button(master=frame_right, 
        image=right_image, bd=0, background="gray20", 
        activebackground="gray20", command=lambda: self._press_gladiator(1))

        label_gladiator_right = tk.Label(master=frame_right, 
        text=(f"{right_gladiator.name} [{right_gladiator.wins}W/"
        f"{right_gladiator.losses}L]"), font="Arial 11 bold", 
        background="gray20", foreground="white", height=1, width=30, 
        wraplength=240)

        # Prevent the images from being garbage collected by Python
        button_gladiator_left.image = left_image
        button_gladiator_right.image = right_image

        frame_match.pack(fill=tk.BOTH, expand=True)
        frame_left.grid(row=0, column=0, sticky="nsew")
        frame_mid.grid(row=0, column=1, sticky="nsew")
        frame_right.grid(row=0, column=2, sticky="nsew")
        button_gladiator_left.grid(row=0, column=0, sticky="nsew")
        label_gladiator_left.grid(row=1, column=0, sticky="nsew")
        label_mid.grid(row=0, column=0, sticky="nsew")
        button_gladiator_right.grid(row=0, column=0, sticky="nsew")
        label_gladiator_right.grid(row=1, column=0, sticky="nsew")

    def _display_win(self):
        '''Displays/refreshes the win screen.'''
        winner, = self.gauntlet.gladiators

        winner_image = Image.open(winner.path)
        winner_image.thumbnail((360,360))
        winner_image = ImageTk.PhotoImage(winner_image)

        self._clear()

        frame_winner = tk.Frame(master=self, background="darkgoldenrod4")
        frame_winner.rowconfigure(0, weight=5)
        frame_winner.rowconfigure(1, weight=1)
        frame_winner.columnconfigure(0, weight=1)

        button_winner = tk.Button(master=frame_winner, image=winner_image, 
        bd=0, background="darkgoldenrod4", activebackground="darkgoldenrod4", 
        command=lambda: self.destroy())
        
        label_winner = tk.Label(master=frame_winner, 
        text=f"{winner.name} wins!", font="Arial 15 bold", 
        background="darkgoldenrod4", foreground="white", 
        height=1, width=64, wraplength=600)

        # Prevent the image from being garbage collected by Python
        button_winner.image = winner_image

        frame_winner.pack(fill=tk.BOTH, expand=True)
        button_winner.grid(row=0, column=0, sticky="nsew")
        label_winner.grid(row=1, column=0, sticky="nsew")

    def _run_match(self):
        '''Runs the next gauntlet match.'''
        self.gauntlet.match_create()
        self._display_match()

    def _run_win(self):
        '''Finishes the gauntlet.'''
        self._display_win()
        self.gauntlet.csv_save()

    def _press_gladiator(self, index: int):
        '''Submits selection in match.'''
        gladiator = self.gauntlet.match.gladiators[index]
        self.gauntlet.match_resolve(gladiator)
        x = self.gauntlet.is_done()
        if x:
            self._run_win()
        else:
            self._run_match()

    def run(self):
        '''Runs the GUI.'''
        self.mainloop()

    def __repr__(self):
        '''
        Canonical representation.
        '''
        return f"GUI(gauntlet={repr(self.gauntlet)})"

# ----------------------------------------------------------------------------