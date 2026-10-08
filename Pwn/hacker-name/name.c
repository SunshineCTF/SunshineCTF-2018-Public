#include <stdio.h>
#include <string.h>


void give_flag(void) {
	FILE* fp = fopen("flag.txt", "r");
	char flag[20];
	
	if(!fp) {
		return;
	}
	
	fgets(flag, sizeof(flag), fp);
	printf("%s\n", flag);
}

int main(int argc, char** argv) {
	(void)argc; (void)argv;
	char buffer[10] = {};
	char name[7];
	
	printf("What's your code name?\n");
	scanf("%s", name);
	
	if(strcmp(buffer, "hacker") == 0)
	{
		give_flag();
	}
	else
	{
		printf("Lol that name sucks.\n");
	}
	return 0;
}
