# Author: Joshua Luo
# Date: 7/31/2020
# Description - Portfolio Project - implementation of the Black Box game

import random
from ray import Ray


class BlackBoxGame:
    """
    Class for implementing the Black Box board game.
    Used with the Ray class to shoot rays through the black box.
    """

    # assume atom locations are valid coordinates, don't contain duplicates, and contains at least one tuple
    def __init__(self, atom_pos):
        """
        Initializes a 10x10 Black Box Game.
            Parameters: list of tuples of the atom locations.
        """
        # use set - avoid duplicates and allows set difference for atoms_left method
        self._atom_pos = set(atom_pos)
        self._atom_guess_mem = set()

        self._ray_mem = {}

        self._score = 25

    def shoot_ray(self, row, column):
        """
        Shoots a ray from the given square and returns the exit square. Updates the score accordingly.
        Each new entry/exit square costs 1 point.
            Parameters: row, column coordinate the ray starts from
            Returns False if coordinates are invalid (corner or non-border squares).
            Returns a tuple of the exit border square coordinate if the ray exits.
            Returns None if there is no exit border square.
        """
        # check for invalid corner coordinates
        if row == column == 0 or row == column == 9 or (row == 0 and column == 9) or (row == 9 and column == 0):
            return False

        # check for invalid non-border coordinates
        if 1 <= row <= 8 and 1 <= column <= 8:
            return False

        if (row, column) in self._ray_mem:  # ray has already been shot before (or was an exit square)
            return self._ray_mem[(row, column)]  # exit is known, don't need to shoot

        new_ray = Ray((row, column))
        new_ray.shoot_ray(self._atom_pos)

        self.update_ray_mem(new_ray)  # add new_ray to memory and update score accordingly

        return new_ray.get_exit()

    def guess_atom(self, row, column):
        """
        Executes an atom location check and updates the score accordingly.
        Each new incorrect guess costs 5 points.
            Parameters: row, column of the atom location guess
            Returns True if the row/column coordinate matches an atom location.
            Returns False if the row/column coordinate does not match and atom location.
        """
        if (row, column) in self._atom_pos:  # atom guess coordinate is an atom location
            self._atom_guess_mem.add((row, column))  # update atom guess memory
            return True

        # guess must be incorrect
        # if new guess - deduct points
        if (row, column) not in self._atom_guess_mem:
            self._score -= 5
            self._atom_guess_mem.add((row, column))  # update atom guess memory
        return False

    def get_score(self):
        """
        Returns the current score.
        """
        return self._score

    def atoms_left(self):
        """
        Returns the number of atoms that haven't been guess yet.
        """
        # set difference keeps only atom location elements that haven't been guessed in memory
        # then use len to get the number
        return len(self._atom_pos - self._atom_guess_mem)

    def update_ray_mem(self, ray):
        """
        Determines if a coordinate is new, deducts a point if it is, and adds the coordinate to memory.
            Parameters: row, column coordinates of entry/exit square
        """
        if ray not in self._ray_mem:  # new ray entry/exit square coordinate - deduct from the score
            self._score -= 1
            self._ray_mem[ray.get_entry()] = ray.get_exit()  # update ray entry/exit memory

            # if a ray has an exit square and the exit square is a different square than the entry square
            if ray.get_exit() is not None and ray.get_exit() != ray.get_entry():
                self._score -= 1
                # entry/exit rays are interchangeable (have the same path)
                self._ray_mem[ray.get_exit()] = ray.get_entry()

    def print_board(self, show_atoms):
        """
        Prints a text representation of the game board.
        """
        print("                        Board")
        print("    0    1    2    3    4    5    6    7    8    9")
        # board[row][column]
        board = []
        for row in range(10):
            a_row = []
            for column in range(10):
                a_row.append(" ")
            board.append(a_row)

        # change the atom squares to "A" if show_atoms is True
        if show_atoms:
            for coordinate in self._atom_pos:
                board[coordinate[0]][coordinate[1]] = "A"
        # else: hides atom locations

        for ray in self._ray_mem:
            if self._ray_mem[ray] is None:
                board[ray[0]][ray[1]] = "H"
            else:
                board[self._ray_mem[ray][0]][self._ray_mem[ray][1]] = "x"

        for row in range(10):
            print(row, board[row], row)
        print("    0    1    2    3    4    5    6    7    8    9")

    def print_atom_guesses(self):
        """
        Prints all of the coordinates guessed for atom locations.
        """
        print("Past Atom Guesses:")
        if len(self._atom_guess_mem) == 0:
            print("None")
        else:
            for coordinate in self._atom_guess_mem:
                print(coordinate)

    def print_ray_mem(self):
        """
        Prints all used ray entry/exit coordinates.
        """
        print("Used Ray squares:")
        if len(self._ray_mem) == 0:
            print("None")
        else:
            for ray_entry in self._ray_mem:
                print(ray_entry)


def main():
    show_atom_locations = False

    # Creates the game with 4 random atom locations
    atom_locations = []
    while len(atom_locations) < 4:
        atom_loc = (random.randint(1, 8), random.randint(1, 8))
        if atom_loc not in atom_locations:
            atom_locations.append(atom_loc)
    game = BlackBoxGame(atom_locations)
    print()
    print("Welcome to Joshua Luo's Black Box game.")
    print()

    # execute the game until the player runs out of points or guesses the position of all the atoms
    while game.get_score() > 0 and game.atoms_left() > 0:
        # displays game state
        game.print_board(show_atom_locations)
        print("         Score:", game.get_score(), "       |  ", "Atoms remaining:", game.atoms_left())
        print()
        game.print_atom_guesses()
        print()

        # shoot a Ray into the Black Box
        shoot = ""
        while shoot != 'y' and shoot != 'n':
            shoot = input("Shoot a Ray? (y/n): ")
            if shoot:
                shoot = shoot[0].lower()
        if shoot == "y":
            ray_res = False
            while ray_res is False:
                row = int(input("Enter a row to shoot a Ray: "))
                column = int(input("Enter a column to shoot a Ray: "))
                ray_res = game.shoot_ray(row, column)
                if ray_res is False:
                    print("Invalid border location! Try again.")
                    print()

            if ray_res is None:
                print("Hit atom")
            else:
                print("Ray exit square: ", ray_res)
            game.print_board(show_atom_locations)
            print("         Score:", game.get_score(), "       |  ", "Atoms remaining:", game.atoms_left())
            print()
            game.print_atom_guesses()
            print()
            print("Score: ", game.get_score())

        # guess Atom location
        print()
        guess = ""
        while guess != 'y' and guess != 'n':
            guess = input("Guess an Atom location? (y/n): ")
            if guess:
                guess = guess[0].lower()

        if guess == "y":
            row = 0
            column = 0
            while not 1 <= row <= 8 or not 1 <= column <= 8:
                row = int(input("Atom guess row (1-8): "))
                column = int(input("Atom guess column (1-8): "))
                if not 1 <= row <= 8 or not 1 <= column <= 8:
                    print("Invalid Atom location! Try again.")
                    print()

            if game.guess_atom(row, column) is True:
                print("Correct!")
            else:
                print("Incorrect!")
                print()
            print("Score: ", game.get_score())

        print()
        input("--Press Enter to continue--")
        print()

        print("---------------------------------------------------------")

    print("Final Score: ", game.get_score())
    if game.get_score() == 0:
        print("Game Over")
    else:
        print("All atoms found")

    print("                      Atom Locations:")
    game.print_board(True)

    print()
    print("Thanks for playing!")


if __name__ == "__main__":
    main()
