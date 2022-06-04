#include <stdlib.h>
#include <stdio.h>

int itoa(int number, char * buf, int buf_length){
    int digits_remain = number;
    int digit;
    int digit_count = 0;

    // count the number of digits
    while(digits_remain){
        digit_count += 1;
        digits_remain /= 10;
    }

    // check for enough space in string buffer to fit all the digits
    if (digit_count > buf_length){
        printf("Error: not enough buffer space allocated to convert integer into string.\n");
        exit(1);
    }

    digits_remain = number;     // restore digits_remain for conversion to string

    // convert each digit (starting from the least significant) to char and place in buf
    for(int i = digit_count - 1; i >= 0; i--){
        digit = digits_remain % 10;     // get the least significant digit
        buf[i] = (char) digit + 48;     // cast as a character and add 48 to get the ascii char value, store into buffer
        digits_remain /= 10;            // drop the smallest digit
    }
    buf[digit_count] = '\0';    // write terminating character
    
    return digit_count;
}