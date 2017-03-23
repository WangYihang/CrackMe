#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]){
	if (argc != 2){
		printf("Usage : \n\t%s [username]\n", argv[0]);
		exit(1);
	}

	char data[] = {0x0C, 0x0A, 0x13, 0x09, 0x0c, 0x0B, 0x0A, 0x08};
	char *username = argv[1];
	int length = strlen(username);
	int i;
	int j;
	int password = 0;
	for (i = 3, j = 0; i < length; i++, j++){
		password += username[i] * data[j % 8];
	}

	printf("Username : [ %s ]\nPassword : [ %d ]\n", username, password);

	return 0;
}
