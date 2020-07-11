// heads up this one doesn't die so that you can see processes with ps -Leo

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
  }
}

int main(void) {
  char nonno[] = "nonno";
  char figlio[] = "figlio";
  char nipote[] = "nipote";
  if (parent_pid = fork()) {
    /* grandparent */
    printf("grandparent pid is %d\n", getpid());
    prctl(PR_SET_CHILD_SUBREAPER, getpid());

    struct sigaction action = {.sa_sigaction = sigchld_handler,
                               .sa_flags = SA_SIGINFO};
    sigaction(SIGCHLD, &action, NULL);
    prctl(PR_SET_NAME, nonno);
  } else {
    /* parent */
    if (fork()) {
      /* parent */
      prctl(PR_SET_NAME, figlio);
    } else {
      /* grandson */
      prctl(PR_SET_NAME, nipote);
      printf("i'm the grandson! my pid is %d\n", getpid());
      printf("and my parent is now %d\n", getppid());
    }
  }

  while (1)
    ;

  return 0;
}