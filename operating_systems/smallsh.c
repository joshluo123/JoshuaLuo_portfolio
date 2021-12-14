/*
Joshua Luo
CS 344 Summer 2021
Assignment 3
*/

#define _POSIX_C_SOURCE 200809L

#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <signal.h>
#include "itoa.h"

#define MAX_IN_LEN 2048
#define MAX_ARGS 512
#define CMDPROMPT ": "
#define EXITCMD "exit"
#define CDCMD "cd"
#define STATUSCMD "status"
#define BGCMD "&"
#define VAREXPAND '$'
#define SPACE ' '
#define INPUT_REDIRECT '<'
#define OUTPUT_REDIRECT '>'

int IN_REDIR = 0;               // flag: if argv contain "< ", set to the index
char IN_REDIR_PATH[100];        // buffer to store the path of the redirected input
int OUT_REDIR = 0;              // flag: if argv contain "> ", set to the index
char OUT_REDIR_PATH[100];       // buffer to store the path of the redirected output
int BG_FLAG = 0;                // flag: set if argv ends with "&"
int CHILD_EXIT_FLAG = 1;        // flag: set if last foreground process exited normally, cleared if terminated by signal
int CHILD_EXITSTAT = 0;         // value of exit status of last completed (by exit) foreground process
int CHILD_TERMSIG = 0;          // value of terminating signal of last completed (by terminate) foreground process
int IGN_BGCMD = 0;              // flag: toggles when SIGTSTP sent to parent process, ignores (set) or acknowledges (clear) the background command in input (foreground-only mode)
int SIG_F = 0;                  // flag: set when a SIG is received (prevents execution of input buffer content), cleared before getting the next input;

/*
Parses the user input string (input) into each space-separated argument and puts them in an array in order (argv).
Returns a count of the number of arguments (argc).
Sets flags if arguments contain input redirect (<), output redirect (>), and run in backgroun (&).
*/
int parse_input(char ** argv, char input[]){
    int argc = 0;
    int input_len = strlen(input) - 1; // ignore the last char for the input length (enter key to input the command)

    for(int i = 0; i < input_len; i++){
        // beginning of an argument (not a space)
        if(input[i] != SPACE){
            int j = 0;   // index of string buffer to copy input chars into

            // check for "< " to set IN_REDIR flag
            if(input[i] == INPUT_REDIRECT && i + 1 < input_len && input[i + 1] == SPACE){
                IN_REDIR = 1;
                i++;    // move past '<' char

                while(input[i] == SPACE){
                    i++;    //  inc i until getting to the next argument (file path name)
                }

                // copy this argument into IN_REDIR_PATH
                while(input[i] != SPACE && i < input_len){    // argument ends at a space or end of input
                    // check for variable expansion of "$$" to pid
                    if(input[i] == VAREXPAND && i + 1 < input_len && input[i + 1] == VAREXPAND){
                        pid_t pid = getpid();
                        char pid_buf[11];                  
                        itoa(pid, pid_buf, 10);     // convert pid into a string

                        // copy pid_buf into IN_REDIR_PATH
                        for(int k = 0; k < strlen(pid_buf); k++){
                            IN_REDIR_PATH[j] = pid_buf[k];
                            j++;
                        }
                        i = i + 2;  // move past both char of"$$"
                    } 
                    // normal character, just copy char into IN_REDIR_PATH
                    else {
                        IN_REDIR_PATH[j] = input[i];
                        i++;
                        j++;
                    }
                }
                IN_REDIR_PATH[j] = '\0';    // terminate string
            } 
            // check for "> " to set OUT_REDIR flag
            else if(input[i] == OUTPUT_REDIRECT && i + 1 < input_len && input[i + 1] == SPACE){
                OUT_REDIR = 1;
                i++;    // move past '>' char

                while(input[i] == SPACE){
                    i++;    //  inc i until getting to the next argument (file path name)
                }

                // copy this argument into OUT_REDIR_PATH
                while(input[i] != SPACE && i < input_len){    // argument ends at a space or end of input
                    // check for variable expansion of "$$" to pid
                    if(input[i] == VAREXPAND && i + 1 < input_len && input[i + 1] == VAREXPAND){
                        pid_t pid = getpid();
                        char pid_buf[11];                  
                        itoa(pid, pid_buf, 10);     // convert pid into a string

                        // copy pid_buf into OUT_REDIR_PATH
                        for(int k = 0; k < strlen(pid_buf); k++){
                            OUT_REDIR_PATH[j] = pid_buf[k];
                            j++;
                        }
                        i = i + 2;  // move past both char of"$$"
                    } 
                    // normal character, just copy char into OUT_REDIR_PATH
                    else {
                        OUT_REDIR_PATH[j] = input[i];
                        i++;
                        j++;
                    }
                }
                OUT_REDIR_PATH[j] = '\0';    // terminate string
            } 
            
            // not a redir special char
            else {
                char * arg_buf = (char *) malloc(100);  // holds the argument string, to be pointed to by argv[argc]
                
                // copy this argument into arg_buf
                while(input[i] != SPACE && i < input_len){    // argument ends at a space or end of input
                    // check for variable expansion of "$$" to pid
                    if(input[i] == VAREXPAND && i + 1 < input_len && input[i + 1] == VAREXPAND){
                        pid_t pid = getpid();
                        char pid_buf[11];                  
                        itoa(pid, pid_buf, 10);     // convert pid into a string

                        // copy pid_buf into arg_buf
                        for(int k = 0; k < strlen(pid_buf); k++){
                            arg_buf[j] = pid_buf[k];
                            j++;
                        }
                        i = i + 2;  // move past both char of"$$"
                    } 
                    // normal character, just copy char into arg_buf
                    else {
                        arg_buf[j] = input[i];
                        i++;
                        j++;
                    }
                }

                // end of argument
                arg_buf[j] = '\0';      // terminate argument string
                argv[argc] = arg_buf;   // store arg_buf in argv
                argc++;
            }
        }
    }

    // if at least 2 arguments and if background process (last arg is "&")
    if(argc >= 2 && strcmp(argv[argc - 1], BGCMD) == 0){    
        BG_FLAG = 1;            // set background process flag
        argv[argc - 1] = NULL;  // don't include & in arguments, set that index value to NULL
        argc--;                 // dec argcount
    } else {                                                // foreground process, normal
        argv[argc] = NULL;      // terminate all arguments with NULL
    }

    return argc;
}

/*
Handler function for the 'status' command. Prints the exit value/terminating signal of the last completed foreground command.
Ignores any additional arguments
*/
void status(void){
    // check if last completed foreground command exited or was terminated, and print corresponding value.
    if(CHILD_EXIT_FLAG){
        printf("exit value %d\n", CHILD_EXITSTAT);
    } else {
        printf("terminated by signal %d\n", CHILD_TERMSIG);
    }
    fflush(stdout);
}

/*
Handler function for the 'cd' command. Changes the working directory.
If no file path is given, changes to HOME path.
Searches for first valid file path to change to.
Ignores any special characters (<, >, &).
*/
void cd(char ** argv, int argc){
    if (argc > 1) {    // contains additional arguments
        int index = 1;
        // find the next argument that's not a special char (if supplied)
        while(index < argc){
            // found argument that's not special char
            if(!(strcmp(argv[index], "<") == 0 || strcmp(argv[index], ">") == 0 || strcmp(argv[index], BGCMD) == 0)){   
                // change working directory to first argument path, ignore the remaining arguments
                if(chdir(argv[index]) != 0){
                    printf("Error: could not change working directory to inputted path.\n");
                    fflush(stdout);
                }
                return;
            } else{     // special char, move to next argument
                index ++;
            }
        }
    }

    // no arguments or no supplied file path name (all special char), change wokring directory to HOME env var path
    if(chdir(getenv("HOME")) != 0){
        printf("Error: could not change working directory to HOME path.\n");
        fflush(stdout);
    }
}

/*
Handler for SIGTSTP. Toggles foreground-only mode. Prints an informative message.
*/
void handle_SIGTSTP(int signo){
    SIG_F = 1;      // set flag indicating SIGSTP was handled, stops execution of input command

    // toggles IGN_BGCMD flag and prints a message.
    if(IGN_BGCMD){
        IGN_BGCMD = 0;
        write(STDOUT_FILENO, "\nexiting foreground-only mode\n", 30);
    } else {
        IGN_BGCMD = 1;
        write(STDOUT_FILENO, "\nentering foreground-only mode (& is now ignored)\n", 50);
    }
}

int main(void){
    char input_buf[MAX_IN_LEN]; // buffer to store the user input
    char *argv[MAX_ARGS];       // array to store each user input argument (terminated by NULL)
    int argc;                   // number of arguments (excludes NULL)
    pid_t bg_child_pids[20];    // stores background child process pids
    int bg_child_count = 0;     // stores a count of how many background child processes have not been reaped

    // change action of SIGINT (ignored by parent and background child, terminates (default) foreground child)
    struct sigaction SIGINT_action = {0};
    SIGINT_action.sa_handler = SIG_IGN;
    sigaction(SIGINT, &SIGINT_action, NULL);       

    // change action of SIGTSTP (toggles foreground-only mode by parent, ignored by all children)
    struct sigaction SIGTSTP_action = {0};
    SIGTSTP_action.sa_handler = handle_SIGTSTP;
    sigfillset(&SIGTSTP_action.sa_mask);
    SIGTSTP_action.sa_flags = 0;
    sigaction(SIGTSTP, &SIGTSTP_action, NULL);

    while(1){
        // check if any background processes have finished to print a message
        int bg_childStatus;
        int removed_pids_count = 0;     // counts how many child processes have been completed and needs to be removed from the array
        for(int i = 0; i < bg_child_count; i++){
            // status status of child process
            int check_pid = waitpid(bg_child_pids[i], &bg_childStatus, WNOHANG);

            if(check_pid > 0){
                // child process has finished, print message
                printf("background pid %d is done: ", bg_child_pids[i]);
                fflush(stdout);

                // print exit status or terminating signal
                if(WIFEXITED(bg_childStatus)){
                    printf("exit value %d\n", WEXITSTATUS(bg_childStatus));
                    fflush(stdout);
                } else {
                    printf("terminated by signal %d\n", WTERMSIG(bg_childStatus));
                    fflush(stdout);
                }

                // set entry value to -1 for removal from the array
                bg_child_pids[i] = -1;
                removed_pids_count++;
            }
        }

        // clean up the array of background process pids if needed
        if(removed_pids_count > 0){
            int next_avail_index;   // track the index to shift subsequent pids to
            int index = 0;

            // find the index of the first removed (-1) pid for next_avail_index
            while(bg_child_pids[index] != -1){
                index++;
            }
            next_avail_index = index;
            index++;    // increment to next index to begin checking to shift

            // shift remaining pids to replace removed pids
            while(index < bg_child_count){
                if(bg_child_pids[index] != -1){
                    // move next remaining pid to next_avail_index
                    bg_child_pids[next_avail_index] = bg_child_pids[index];
                    next_avail_index++;
                }
                index++;
            }
            bg_child_count -= removed_pids_count;   // update number of background process pids
        }

        // print command prompt and get/parse input
        printf("%s", CMDPROMPT);
        fflush(stdout);
        fgets(input_buf, MAX_IN_LEN, stdin);
        argc = parse_input(argv, input_buf);
        
        if(!SIG_F){ //  prevents executing the input if a signal flag went off
            if(argc > 0 && strcmp(argv[0], EXITCMD) == 0){      // 'exit' command, end the smallsh
                exit(0);
            } else if(argc != 0 && argv[0][0] != '#'){          // non-empty command and not a comment
                if(strcmp(argv[0], STATUSCMD) == 0){    // 'status' command
                    status();
                } else if(strcmp(argv[0], CDCMD) == 0){ // 'cd' command
                    cd(argv, argc);
                } else {                                        // other non-built-in commands
                    int in_fd;              // fd for input redirection file (if needed)
                    int out_fd;             // fd for output redirection file (if needed)
                    pid_t spawnPid;         // pid for fork child process (if needed)
                    int childStatus;        // child status for fork child process (if needed)

                    spawnPid = fork();      // fork a process to execute the command
                    switch(spawnPid){
                        case -1:    // fork fail
                            perror("fork");
                            fflush(stdout);
                            break;
                            
                        case 0:     // child process, execute the command
                            if(!BG_FLAG){   // foreground child process, set SIGINT handler to default (terminates)
                                SIGINT_action.sa_handler = SIG_DFL;
                                sigaction(SIGINT, &SIGINT_action, NULL);
                            }

                            // all child processes ignore SIGTSTP
                            SIGTSTP_action.sa_handler = SIG_IGN;
                            sigaction(SIGTSTP, &SIGTSTP_action, NULL);
                            
                            if(IN_REDIR) {                      // redirect input
                                // change input path to the named file
                                in_fd = open(IN_REDIR_PATH, O_RDONLY);
                                if(in_fd < 0){
                                    printf("Error: unable to access input file.\n");
                                    fflush(stdout);
                                    exit(1);
                                }
                                dup2(in_fd, STDIN_FILENO);
                            } else if(BG_FLAG && !IGN_BGCMD){   // no redirect input and is a bg process
                                in_fd = open("/dev/null", O_RDONLY);
                                dup2(in_fd, STDIN_FILENO);
                            }

                            if(OUT_REDIR){                      // redirect output
                                // change output path to the named file
                                out_fd = open(OUT_REDIR_PATH, O_WRONLY | O_TRUNC | O_CREAT, 0666);
                                if(out_fd < 0){
                                    printf("Error: unable to access input file.\n");
                                    fflush(stdout);
                                    exit(1);
                                }
                                dup2(out_fd, STDOUT_FILENO);
                            } else if (BG_FLAG && !IGN_BGCMD){  // no redirect output and is a bg process
                                out_fd = open("/dev/null", O_WRONLY);
                                dup2(out_fd, STDOUT_FILENO);
                            }

                            execvp(argv[0], argv);      // execute bash command
                            
                            // execvp error
                            perror("execvp()");
                            fflush(stdout);
                            exit(1);
                            break;

                        default:    // parent process
                            if(BG_FLAG && !IGN_BGCMD){  // background child process (not ignoring &)
                                // when child process starts, print child's pid
                                printf("background pid is %d\n", spawnPid);
                                fflush(stdout);

                                // store background process pid and increment counter 
                                bg_child_pids[bg_child_count] = spawnPid;
                                bg_child_count++;
                            } else{                     // foreground child process
                                // wait for complete, do not return to command line
                                spawnPid = waitpid(spawnPid, &childStatus, 0);

                                // set child process exit status or terminating signals and flags
                                if(WIFEXITED(childStatus)){
                                    // exit: store status value and set flag
                                    CHILD_EXITSTAT = WEXITSTATUS(childStatus);
                                    CHILD_EXIT_FLAG = 1;    // set because child exited normally
                                } else {
                                    // terminated: store term signal value and set flag
                                    CHILD_TERMSIG = WTERMSIG(childStatus);
                                    CHILD_EXIT_FLAG = 0;    // cleared because child was terminated by a signal
                                    status();    // if child is killed by signal, immediately prints out the terminating signal
                                }
                            }
                    }
                }
            }
        }
        // reset flags for next input
        SIG_F = 0;
        IN_REDIR = 0;
        OUT_REDIR = 0;
        BG_FLAG = 0;
    }

    return 0;
}
