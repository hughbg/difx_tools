#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <error.h>
#include <errno.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#define FRAME_HEADER_SIZE 32
#define FRAME_SIZE 8032

typedef unsigned char byte;

int main(int argc, char *argv[]) {
    int fd1, fd2, fd3, num1, num2;
    byte buffer1[FRAME_SIZE], buffer2[FRAME_SIZE];

    printf("Aligning %s to %s and writing to %s\n", argv[2], argv[1], argv[3]);
    if ( (fd1=open(argv[1], O_RDONLY)) == -1 )
        error(errno, errno, "open: %s", argv[1]);
    if ( (fd2=open(argv[2], O_RDONLY)) == -1 )
        error(errno, errno, "open: %s", argv[2]);
    if ( (fd3=open(argv[3], O_WRONLY|O_CREAT|O_TRUNC, S_IRUSR|S_IWUSR)) == -1 )
        error(errno, errno, "open: %s", argv[3]);


    while ( (num1=read(fd1, buffer1, FRAME_SIZE)) > 0 ) {
        if ( (num2=read(fd2, buffer2, FRAME_SIZE)) != num1 ) {
            fprintf(stderr, "Run out of frames in file %s\n", argv[2]);
            exit(1);
        }


        // Copy the header of file 1 to file 2
        memcpy(buffer2, buffer1, FRAME_HEADER_SIZE);

        // write file 2 to file 3
        if ( write(fd3, buffer2, FRAME_SIZE) == -1 )
            error(errno, errno, "write");


    }


}

