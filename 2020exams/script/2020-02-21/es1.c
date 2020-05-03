#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char const* argv[]) {
    if (argc == 2) {
        char *abspath = realpath(argv[1], NULL); 
        int ret = symlink(argv[1], abspath);
        free(abspath);
        if (ret == -1) {
            perror("Something went wrong");
            return EXIT_FAILURE;
        } else {
            return EXIT_SUCCESS;
        }
    } else {
        printf("Usage: abspath FILE");
        return EXIT_FAILURE;
    }
}
