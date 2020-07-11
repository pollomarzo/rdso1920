/*
gcc -o giovanni es2.c
./giovanni 2 sleep 5 // ls -l // sleep 5 // ps // sleep 2
*/

#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

#define MAX_LENGTH 20
#define MAX_COMMANDS 10
#define MAX_ARGS 10

static char *commands[MAX_COMMANDS][MAX_ARGS];
static int total_proc = 0;
static int next_to_run = -1;
static int completed = 0;

void start_proc() {
  if (next_to_run < total_proc) {
    next_to_run++;
    if (fork() == 0) {
      if (execvp(commands[next_to_run][0], commands[next_to_run]) < 0)
        perror("exec error");
    }
  }
}

void sigchld_handler(int sig, siginfo_t *info, void *ucontext) {
  if (info->si_code == CLD_EXITED) {
    waitpid(info->si_pid, NULL, 0);
    completed++;
    start_proc();
  }
}

int main(int argc, char *argv[]) {
  if (argc < 3) {
    printf("usage:...\n");
    exit(EXIT_FAILURE);
  }

  int max_concurrent_proc = atoi(argv[1]);
  if (max_concurrent_proc < 1) {
    printf("At least 1\n");
    exit(EXIT_FAILURE);
  }

  struct sigaction action = {.sa_sigaction = sigchld_handler,
                             .sa_flags = SA_SIGINFO};
  sigaction(SIGCHLD, &action, NULL);

  int command_index = 0, arg_index = 0;
  for (int i = 2; i < argc; i++) {
    if (strcmp(argv[i], "//") != 0) {
      commands[command_index][arg_index] = malloc(MAX_LENGTH * sizeof(char));
      strncpy(commands[command_index][arg_index++], argv[i], MAX_LENGTH);
    } else {
      commands[command_index][arg_index] = NULL;
      command_index++;
      arg_index = 0;
    }
  }
  command_index++;

  total_proc = command_index;
  int active_process = 0;
  for (; active_process < max_concurrent_proc; active_process++) {
    start_proc();
  }

  while (completed < total_proc)
    ;

  return 0;
}