#include <stdio.h>
char* ft_quicksort(char* string) {
    int count = 0;
    while (string[count]) count++;
    int i = 0;
    char temp;
    while (i < count) {
        if (string[i] > string[count - 1]) {
            temp = string[i];
            string[i] = string[count - 1];
            string[count - 1] = temp;
        }
        i++;
    }
    return (string);
}

int main(void) {
    printf("%s\n", ft_quicksort("54321"));
    return 0;
}