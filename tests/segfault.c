#include <stdio.h>

int main() {
    int a = 10;
    int b = 20;
    int segmentation = 20;
    int d = 20;
    int *ptr = NULL;
    *ptr = 10;  // Dereferencing a NULL pointer will cause a segmentation fault
    return 0;
}