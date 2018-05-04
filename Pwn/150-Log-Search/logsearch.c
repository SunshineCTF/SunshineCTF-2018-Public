#include <stdio.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "pwnable_harness.h"

char hint[] = ".data";
char search_file[] = "logs.txt";

void search_logs(const char* filename, const char* search_phrase) {
	char line[256];
	bool foundMatch = false;
	
	// Display the query for debug purposes
	printf("Searching for: ");
	printf(search_phrase);
	printf("\n");
	
	// Open the file to search through
	FILE* fp = fopen(filename, "r");
	if(!fp) {
		perror(filename);
		exit(EXIT_FAILURE);
	}
	
	// Search each line of the file for the search string
	while(fgets(line, sizeof(line), fp)) {
		if(strstr(line, search_phrase)) {
			printf("Found match: %s", line);
			foundMatch = true;
		}
	}
	
	// Did we find a match?
	if(!foundMatch) {
		printf("No results found!\n");
	}
	
	// Close IRC log file
	fclose(fp);
}

void handle_connection(int sock) {
	char search[256];
	
	printf("Searchable IRC logs!\n");
	
	// Get a query from the user
	printf("Enter a search phrase: ");
	fgets(search, sizeof(search), stdin);
	
	// Strip newline
	char* end = strchr(search, '\n');
	if(end != NULL) {
		*end = '\0';
	}
	
	// Search for matching IRC messages
	search_logs(search_file, search);
}


/* Everything below can safely be ignored and is not part of the challenge. */
int main(int argc, char** argv) {
	server_options opts = {
		.user = "logsearch",
		.chrooted = true,
		.port = 20008,
		.time_limit_seconds = 30
	};
	
	return server_main(argc, argv, opts, &handle_connection);
}

