smallsh
Operating Systems
by Joshua Luo

An simplified version of a shell implemented in C with a subset of features of some well-known shells, such as bash.

Implemented functionality:
- the symbol ":" indicates an input prompt
- the symbol "#" at the beignning of a command indicates a commented line, and will not execute anything
- the symbol "&" at the end of a command indicates that the command is to be executed in the background
- the symbols "<" and ">" redirects the input or output of the command
- the symbol "$$" expands to the process ID of smallsh. No other symbol expansion is performed
- the commands "exit", "cd", and "status" are handled directly by smallsh
    - exit: kills all processes and terminates smallsh
    - cd: changes the working directory of smallsh. Accepts absolute and relative paths
    - status: prints the exit status or terminating signal of the last completed foreground process
- other commands are run from the /bin/ directory by forking a child process


Instructions to Run (UNIX):
- download the files into a directory
- navigate to the directory in a terminal
- from the command line, run the following commands to compile and run smallsh

compile:
    gcc -std=c11 -Wall -Werror -g3 -O0 smallsh.c itoa.c -o smallsh
run:
    smallsh

syntax within smallsh:
    command [arg1 arg2 ...] [< input file] [> output file] [&]

notes:
    - items in square brackets are optional
    - the input file and output file may be in any order
    - to run as a background process, the [&] argument must be the last argument
    - 'exit' command will ignore any subsequent arguments
    - 'cd' command will ignore any special characters (<, >, &) and attempt to change to the first found file path, if inputted
    - 'status' command will ignore any subsequent arguments
    - any other commands will run the same as bash

File Descriptions:
itoa.c: included file for converting a string of digits into an integer.
itoa.h: header file for including itoa.c in smallsh.c.
smallsh.c: executable file for running smallsh/