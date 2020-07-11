#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/prctl.h>
#include <sys/wait.h>
#include <unistd.h>

pid_t parent_pid;

void sigchld_handler(int sig, siginfo_t *info, void *ucontext) {
  waitpid(info->si_pid, NULL, 0);

  if (info->si_pid != parent_pid && info->si_code == CLD_EXITED) {
    printf("Child process %d terminated, now exit grandparent %d\n",
           info->si_pid, getpid());
    exit(EXIT_SUCCESS);
  }
}

int main(void) {
  if (parent_pid = fork()) {
    /* grandparent */
    printf("grandparent pid is %d\n", getpid());
    prctl(PR_SET_CHILD_SUBREAPER, getpid());

    struct sigaction action = {.sa_sigaction = sigchld_handler,
                               .sa_flags = SA_SIGINFO};
    sigaction(SIGCHLD, &action, NULL);
  } else {
    /* parent */
    if (fork()) {
      /* parent */
      exit(EXIT_SUCCESS);
    } else {
      /* grandson */
      printf("i'm the grandson! my pid is %d\n", getpid());
      printf("and my parent is now %d\n", getppid());
      exit(EXIT_SUCCESS);
    }
  }

  while (1)
    ;

  return 0;
}

/*
SIMPLER BUT STUPID

int main(void) {
  if (parent_pid = fork()) {
    // grandparent
    printf("grandparent pid is %d\n", getpid());
    prctl(PR_SET_CHILD_SUBREAPER, getpid());
    wait(NULL)
  } else {
    // parent
    if (fork()) {
      // parent
      exit(EXIT_SUCCESS);
    } else {
      // grandson
      sleep(2);
      printf("i'm the grandson! my pid is %d\n", getpid());
      printf("and my parent is now %d\n", getppid());
      exit(EXIT_SUCCESS);
    }
  }

  wait(NULL)

  return 0;
}
*/