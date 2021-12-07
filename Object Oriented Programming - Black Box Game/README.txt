Object-Oriented Programming
Black Box Game
by Joshua Luo

An object-oriented implementation of the 'Black Box' board game. This implementation is an 8x8 board with at least one atom and the player starts with 25 points.

Rules and Description: https://en.wikipedia.org/wiki/Black_Box_(game)
Online Implementation: http://www.pythononline.co.uk/blackbox/

A BlackBoxGame class represents the board and game for the players. It is initialized with a list of tuples corresponding to the positions of the atoms, and tracks the results of "firing" a ray into the box and the player's remaining points.

A Ray class is used by the BlackBoxGame class to represent a ray that is shot into the box according to the user's input. Its position as it is "fired" into the box is determined based on the positions of Atoms.

A user interface is provided to run the program. It randomly places 4 Atoms

- the printed board includes a "border" that is off the board (i.e. not valid inputs for Ray shots and Atom guesses) for representing results of previously shot rays
- Ray shot location: assumes user inputs an integer
- Atom guess location: assume user inputs an integer