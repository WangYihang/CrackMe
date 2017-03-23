#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void get_password(char *username);

int main(int argc, char *argv[]){
	if (argc != 2){
		printf("Usage : \n\t%s [username]\n", argv[0]);
		exit(1);
	}

	char *username = argv[1];
	get_password(username);

	return 0;
}

void get_password(char *username){
	int length = strlen(username);
	int i;
	int j;
	int password = 0;
	for(i = 0, j = 45; i < length; i++, j++){
		password += username[i] * j;
	}
	printf("Username : [ %s ]\nPassword : [ %d ]\n", username, password);
}
