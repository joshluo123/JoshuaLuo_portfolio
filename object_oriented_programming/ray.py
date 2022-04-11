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

        if not self._exit_square:  # check_edge_atom did not change exit_square (not a hit or reflection)
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