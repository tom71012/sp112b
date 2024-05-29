#include <unistd.h>
#include <stdlib.h>
#include <stdio.h> 

void print_george() {   
  while (1) {    
    printf("George\n");    
    sleep(1);    
  }    
}    

void print_mary() {    
  while (1) {    
    printf("Mary\n");    
    sleep(2);    
  }    
}    

int main() {    
  pid_t pid1, pid2;    
  pid1 = fork();   
  if (pid1 == 0) {  
    print_george();
    exit(0);
  }
  
  pid2 = fork();   
  if (pid2 == 0) {   
    print_mary();
    exit(0);
  }
  
  while (1) {   
    printf("----------------\n"); 
    sleep(1);  
  }    
  return 0;    
}
