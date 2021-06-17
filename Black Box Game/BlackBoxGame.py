# Author: Joshua Luo
# Date: 7/31/2020
# Description - Portfolio Project - implementation of the Black Box game

import random


class BlackBoxGame:
    """
    Class for implementing the Black Box board game. Used with the Ray class to shoot rays through the black box.
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

        # guest must be incorrect
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
            print(board[row])

    def print_atom_guesses(self):
        """
        Prints all of the coordinates guessed for atom locations.
        """
        print("Past Guesses:")
        for coordinate in self._atom_guess_mem:
            print(coordinate)

    def print_ray_mem(self):
        """
        Prints all of the used ray entry/exit coordinates.
        """
        print("Used ray squares:")
        for ray_entry in self._ray_mem:
            print(ray_entry)


class Ray:
    """
    Class for representing a ray to be used with the BlackBoxGame class.
    """

    def __init__(self, entry_square):
        """
        Initializes a ray to be shot from the given entry square coordinates.
            Parameters: entry_row, entry_column tuple coordinates of the entry square
        """
        self._entry_square = entry_square

        # set the movement direction - list of how the row/column change when moved forward
        self._move_dir = []
        if self._entry_square[0] == 0:  # entry square from top row
            self._move_dir = [1, 0]  # moves down (increase row)
        elif self._entry_square[0] == 9:  # entry square from bottom row
            self._move_dir = [-1, 0]  # moves up (decrease row)
        elif self._entry_square[1] == 0:  # entry square from left column
            self._move_dir = [0, 1]  # moves right (increase column)
        else:  # entry square from right column
            self._move_dir = [0, -1]  # moves left (decrease column)

        self._exit_square = []

    def shoot_ray(self, atom_pos):
        """
        Shoots the ray into the black box.
            Parameters: atom_pos list of tuple coordinates of atom locations.
        """
        self.check_edge_atom(atom_pos)

        if self._exit_square == []:  # check_edge_atom did not change exit_square (not a hit or reflection)
            pos = [self._entry_square[0], self._entry_square[1]]

            # move the ray into the black box   (check_edge_atom guarantees initial forward movement)
            pos[0] += self._move_dir[0]
            pos[1] += self._move_dir[1]

            # ray position is not a border square and is not going to hit an atom
            while pos[0] != 0 and pos[0] != 9 and pos[1] != 0 and pos[1] != 9 and self._exit_square is not None:
                if (pos[0] + self._move_dir[0], pos[1] + self._move_dir[1]) in atom_pos:  # forward square is an atom
                    self._exit_square = None  # hit, no exit square

                # check for deflections
                elif self.check_deflect(pos, atom_pos) is False:  # no deflections (or hit from above)
                    # move forward
                    pos[0] += self._move_dir[0]
                    pos[1] += self._move_dir[1]

            # not a hit, reached an exit square
            if self._exit_square is not None:
                self._exit_square = (pos[0], pos[1])

    def check_edge_atom(self, atom_pos):
        """
        Checks for atoms placed on the edge in front of the entry square, resulting in immediate hits or reflections.
            Parameters: atom_pos list of tuple coordinates of atom locations.
        """
        # check if atom directly in front of entry square - hit, no exit square)
        if (self._entry_square[0] + self._move_dir[0], self._entry_square[1] + self._move_dir[1]) in atom_pos:
            self._exit_square = None

        # check for reflection cases - exit square is same as entry square
        # based on entry square, check forward diagonal squares for atoms
        elif self._entry_square[0] == 0:
            if (1, self._entry_square[1] + 1) in atom_pos or (1, self._entry_square[1] - 1) in atom_pos:
                self._exit_square = self._entry_square
        elif self._entry_square[0] == 9:
            if (8, self._entry_square[1] + 1) in atom_pos or (8, self._entry_square[1] - 1) in atom_pos:
                self._exit_square = self._entry_square
        elif self._entry_square[1] == 0:
            if (self._entry_square[0] + 1, 1) in atom_pos or (self._entry_square[0] - 1, 1) in atom_pos:
                self._exit_square = self._entry_square
        elif self._entry_square[1] == 9:
            if (self._entry_square[0] + 1, 8) in atom_pos or (self._entry_square[0] - 1, 8) in atom_pos:
                self._exit_square = self._entry_square

    def check_deflect(self, pos, atom_pos):
        """
        Determines if a ray at a given position and movement direction will be deflected and updates the ray's move_dir.
            Parameters: pos coordinates of the ray's current positions
                        atom_pos list of tuple coordinates of atom locations.
            Returns True if there's a deflection and move_dir was changed
            Returns False is there's no deflection
        """
        # moving down, check row + 1 and column +- 1
        if self._move_dir == [1, 0] and (pos[0] + 1, pos[1] + 1) in atom_pos:
            self.turn_right()
            return True
        elif self._move_dir == [1, 0] and (pos[0] + 1, pos[1] - 1) in atom_pos:
            self.turn_left()
            return True

        # moving up, check row - 1 and column +- 1
        elif self._move_dir == [-1, 0] and (pos[0] - 1, pos[1] - 1) in atom_pos:
            self.turn_right()
            return True
        elif self._move_dir == [-1, 0] and (pos[0] - 1, pos[1] + 1) in atom_pos:
            self.turn_left()
            return True

        # moving right, check row +- 1 and column + 1
        elif self._move_dir == [0, 1] and (pos[0] + 1, pos[1] + 1) in atom_pos:
            self.turn_left()
            return True
        elif self._move_dir == [0, 1] and (pos[0] - 1, pos[1] + 1) in atom_pos:
            self.turn_right()
            return True

        # moving left, check row += 1 and column - 1
        elif self._move_dir == [0, -1] and (pos[0] - 1, pos[1] - 1) in atom_pos:
            self.turn_left()
            return True
        elif self._move_dir == [0, -1] and (pos[0] + 1, pos[1] - 1) in atom_pos:
            self.turn_right()
            return True

        # no deflection
        return False

    def turn_right(self):
        """
        Changes the movement direction of the ray to turn right.
        """
        if self._move_dir == [1, 0]:  # originally moving down
            self._move_dir = [0, -1]  # now moving left

        elif self._move_dir == [-1, 0]:  # originally moving up
            self._move_dir = [0, 1]  # now moving right

        elif self._move_dir == [0, 1]:  # originally moving right
            self._move_dir = [1, 0]  # now moving down

        elif self._move_dir == [0, -1]:  # originally moving left
            self._move_dir = [-1, 0]  # now moving up

    def turn_left(self):
        """
        Changes the movement direction of the ray to turn left.
        """
        if self._move_dir == [1, 0]:  # originally moving down
            self._move_dir = [0, 1]  # now moving right

        elif self._move_dir == [-1, 0]:  # originally moving up
            self._move_dir = [0, -1]  # now moving left

        elif self._move_dir == [0, 1]:  # originally moving right
            self._move_dir = [-1, 0]  # now moving up

        elif self._move_dir == [0, -1]:  # originally moving left
            self._move_dir = [1, 0]  # now moving down

    def get_entry(self):
        """
        Returns a tuple of coordinates of the entry square of the ray.
        """
        return self._entry_square

    def get_exit(self):
        """
        Returns a tuple of coordinates of the exit square of the ray.
        Returns None if ray hits an atom (no exit coordinate).
        """
        return self._exit_square

    def set_exit(self, exit_square):
        """
        Sets the exit square at the given coordinate tuple.
        Should only be used when a shooting a ray results in an exit square, as entry/exit are interchangeable.
        """
        self._exit_square = exit_square


def main():
    # randomly create 4 atom locations
    atom_locations = []
    while len(atom_locations) < 4:
        atom_loc = (random.randint(1, 8), random.randint(1, 8))
        if atom_loc not in atom_locations:
            atom_locations.append(atom_loc)

    game = BlackBoxGame(atom_locations)
    print("Score: ", game.get_score())
    print("Atoms remaining: ", game.atoms_left())

    while game.get_score() > 0 and game.atoms_left() > 0:
        print("Board:")
        game.print_board(False)

        shoot = input("Shoot Ray? (y/n): ")
        if shoot == "y":
            row = int(input("Shoot Ray row: "))
            column = int(input("Shoot Ray column: "))
            ray_res = game.shoot_ray(row, column)
            while ray_res is False:
                print("Invalid row/column")
                print()
                row = int(input("Shoot Ray row: "))
                column = int(input("Shoot Ray column: "))
                ray_res = game.shoot_ray(row, column)
            if ray_res is None:
                print("Hit atom")
            else:
                print("Ray exit square: ", ray_res)
            print("Score: ", game.get_score())

        print()

        print("Atoms remaining: ", game.atoms_left())
        guess = input("Guess Atom? (y/n): ")
        if guess == "y":
            row = int(input("Atom guess row (1-8): "))
            column = int(input("Atom guess column (1-8): "))
            if game.guess_atom(row, column) is True:
                print("Correct guess")
            else:
                print("Incorrect guess")
            print("Score: ", game.get_score())

        print()
        game.print_ray_mem()
        print()
        game.print_atom_guesses()
        print()

    print("Score: ", game.get_score())
    if game.get_score() == 0:
        print("Game Over")
    else:
        print("All atoms found")

    print("Complete Board:")
    game.print_board(True)


if __name__ == "__main__":
    main()
