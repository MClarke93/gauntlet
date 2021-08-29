import csv
import os
import random
import sys

# ----------------------------------------------------------------------------

HOME_DIR = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) \
    else os.path.split(os.path.realpath(__file__))[0]

# ----------------------------------------------------------------------------

class Gladiator:
    '''
    A gladiator that is participating in the gauntlet.
    
    Attributes:
        name: Gladiators name.
        path: Full filepath to gladiator's image.
        wins: Gladiator's win count.
        losses: Gladiator's loss count.
    '''

    def __init__(self, name: str, path: str, *, wins: int = 0, 
    losses: int = 0):
        '''
        Constructs a Gladiator object.
        
        Arguments:
            name: Gladiator's name. Required.
            path: Full filepath to gladiator's image. Required.
        Keyword Arguments:
            wins: Number of wins. Optional.
            losses: Number of losses. Optional.
        '''
        self.name = name
        self.path = path
        self.wins = wins
        self.losses = losses

    def __repr__(self):
        '''
        Canonical representation.
        '''
        return (f"Gladiator(name={repr(self.name)}, path={repr(self.path)}, "
        f"wins={repr(self.wins)}, losses={repr(self.losses)})")

# ----------------------------------------------------------------------------

class Match:
    '''
    A match between gladiators in a gauntlet.

    Attributes:
        gladiators: List of gladiators involved in the match.
        winner: Who won the match, if a winner has been declared.
    '''
    def __init__(self, *gladiators: Gladiator, winner: Gladiator = None):
        '''
        Constructs a Match object.
        Arguments:
            *gladiators: The gladiators involved in the match. Required.
        Keyword Arguments:
            winner: The gladiator that won the match. Optional.
        '''
        self.gladiators = gladiators
        self.winner = winner
    
    def __repr__(self):
        '''
        Canonical representation.
        '''
        temp_str = ""
        for gladiator in self.gladiators:
            temp_str = temp_str + f"{repr(gladiator)}, "
        return (f"Match({temp_str[:-2]})")

# ----------------------------------------------------------------------------

class Gauntlet:
    '''
    Tthe gauntlet and its matches.
    
    Attributes:
        gladiators: The active gauntlet participants.
        defeated: The eliminated gauntlet participants.
        chances: Losses needed to eliminate a gladiator from the gauntlet.
        match: The currently active gauntlet match.
        history: A list of resolved matches.
        state: The state of the gauntlet...
            -1 = Freshly created
            0 = In-progress
            1 = Completed (only one gladiator left)
    '''

    def __init__(self, *, gladiators: list[Gladiator] = None, 
    defeated: list[Gladiator] = None, chances: int = 1):
        '''
        Constructs a Gauntlet object.
        
        Keyword Arguments:
            gladiators: List of Gladiator objects. Optional.
            defeated: List of eliminated Gladiator objects. Optional.
            chances: Losses needed to eliminate gladiator. Optional.
        '''
        self.gladiators = [] if gladiators == None else gladiators
        self.defeated = [] if defeated == None else defeated
        self.chances = chances
        self.match = None
        self.history = []
        self.state = -1

    def gladiator_load(self, dir: str, ext: list[str]):
        '''
        Loads a list of gladiators by referencing images in a directory.
        
        Arguments:
            dir: Path to directory containing Gladiators images. Required.
            ext: List containing image file extensions to include. Required.
        '''
        img_list = map(os.path.splitext, os.listdir(dir))
        for name, end in img_list:
            if end in ext:
                path = os.path.join(dir, name + end)
                new_gladiator = Gladiator(name = name, path = path)
                self.gladiators.append(new_gladiator)
    
    def _gladiator_get(self, name: str, *, defeated: bool = False):
        '''
        Takes a name and returns first Gladiator object with that name.
        If the name is not found, a ValueError is raised.
        
        Arguments:
            name: Name to search for. Required.
        Keyword Arguments:
            defeated: Whether or not to search the defeated list. Optional.
        '''
        for gladiator in self.gladiators:
            if gladiator.name == name:
                return gladiator
        if defeated == True:
            for gladiator in self.defeated:
                if gladiator.name == name:
                    return gladiator
        raise ValueError(f"{repr(name)} is not in this gauntlet.")
    
    def _gladiator_defeat(self, gladiator: Gladiator):
        '''
        Moves a gladiator from gladiator list to defeated list.
        
        Arguments:
            gladiator: Which gladiator to move. Required.
        '''
        self.defeated.append(gladiator)
        self.gladiators.remove(gladiator)
    
    def match_create(self):
        '''
        Creates a new gauntlet match.
        If there's too few gladiators left, raises a ValueError.
        '''
        if len(self) > 1:
            self.match = Match(*random.sample(self.gladiators, 2))
        else:
            raise ValueError("Not enough gladiators to create match.")
    
    def match_resolve(self, winner: Gladiator):
        '''
        Declares a winner in the current match.
        If the name is not found, a ValueError is raised.
        If there is no current match, a RuntimeError is raised.
        
        Arguments:
            winner: The gladiator which won the match. Required.
        '''
        if isinstance(self.match, Match):
            if winner in self.match.gladiators:
                for gladiator in self.match.gladiators:
                    if gladiator == winner:
                        gladiator.wins += 1
                        self.match.winner = gladiator
                    else:
                        gladiator.losses += 1
                        if gladiator.losses >= self.chances:
                            self._gladiator_defeat(gladiator)
                self.history.append(self.match)
                self.match = None
            else:
                raise ValueError(f"{repr(winner)} is not in this match.")
        else:
            raise RuntimeError("No match to resolve.")
    
    def csv_save(self):
        '''
        Saves the results of the gauntlet to a CSV file.
        '''
        path = os.path.join(HOME_DIR, "results.csv")
        print(path)
        with open(path, 'w', newline="") as f:
            writer = csv.writer(f)
            for gladiator in self.gladiators:
                writer.writerow((1, gladiator.name, gladiator.wins, gladiator.losses))
            for gladiator in enumerate(self.defeated[::-1], start=2):
                number, object = gladiator
                writer.writerow((number, object.name, object.wins, object.losses))

    def is_done(self):
        '''
        Updates the state of the gauntlet and returns it.
        '''
        if len(self) > 1:
            self.state = 0
        elif len(self) == 1:
            self.state = 1
        return self.state

    def __len__(self):
        '''
        Gauntlet's 'length' is the number of remaining participants.
        '''
        return len(self.gladiators)

    def __repr__(self):
        '''
        Canonical representation.
        '''
        return (f"Gauntlet(gladiators={repr(self.gladiators)}, "
        f"defeated={repr(self.defeated)})")

# ----------------------------------------------------------------------------