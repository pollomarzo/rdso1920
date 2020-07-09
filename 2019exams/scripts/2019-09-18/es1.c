#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

#define MAX_LENGTH 20
#define MAX_COMMANDS 10
#define MAX_ARGS 10

int main(int argc, char *argv[]) {
  if (argc < 2) {
    printf("usage:...\n");
    exit(EXIT_FAILURE);
  }

  int command_index = 0, arg_index = 0;
  char *commands[MAX_COMMANDS][MAX_ARGS] = {0};
  for (int i = 1; i < argc; i++) {
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

  pid_t pid;
  pid_t children[command_index];
  for (int i = 0; i < command_index; i++) {
    if ((pid = fork())) {
      children[i] = pid;
    } else {
      if (execvp(commands[i][0], commands[i]) < 0)
        perror("exec error");
    }
  }

  for (int i = 0; i < command_index; i++)
    waitpid(children[i], NULL, 0);

  return 0;
}