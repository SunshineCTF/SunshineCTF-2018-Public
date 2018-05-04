#include <stdio.h>
#include <string.h>
#include "pwnable_harness.h"


void give_flag(void) {
	FILE* fp = fopen("flag.txt", "r");
	char flag[20];
	
	if(!fp) {
		return;
	}
	
	fgets(flag, sizeof(flag), fp);
	printf("%s\n", flag);
}

void handle_connection(int sock)
{
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
}

int main(int argc, char** argv) {
	server_options opts = {
		.user = "hacker-name",
		.chrooted = true,
		.port = 20007,
		.time_limit_seconds = 30
	};
	
	return server_main(argc, argv, opts, &handle_connection);
}
