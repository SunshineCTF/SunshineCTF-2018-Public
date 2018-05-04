//
//  hexalicous.c
//
//  Created by hackucf_kcolley on 09/28/16
//  Copyright (c) 2016 hackucf_kcolley. All rights reserved.
//

#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <stdint.h>
#include <string.h>
#include "pwnable_harness.h"


static char flag[100];
static void read_flag(void) {
	FILE* fp = fopen("flag.txt", "rb");
	if(!fp) {
		perror("flag.txt");
		exit(EXIT_FAILURE);
	}
	
	if(!fgets(flag, sizeof(flag), fp)) {
		exit(EXIT_FAILURE);
	}
	
	fclose(fp);
}


static char* next_line(char* line, size_t line_size) {
	if(!fgets(line, line_size, stdin)) {
		return NULL;
	}
	
	char* end = strchr(line, '\n');
	if(end) {
		*end = '\0';
	}
	
	return line;
}


static bool menu_input(unsigned* choice) {
	do {
		printf(
			"What type of value do you want to see in hex?\n"
			"[1] char\n"
			"[2] short\n"
			"[3] unsigned short\n"
			"[4] int\n"
			"[5] unsigned int\n"
			"[6] long long\n"
			"[7] unsigned long long\n"
			"[8] float\n"
			"[9] double\n"
			"[10] small string (8 chars)\n"
			"[11] Quit hexalicious\n"
			"\n"
			"[>] "
		);
		
		char line[10];
		if(!next_line(line, sizeof(line))) {
			return false;
		}
		
		char* end = NULL;
		*choice = strtoul(line, &end, 10);
		if(!(end == line || *choice > 11)) {
			break;
		}
		
		printf("Invalid input, please enter a number [1-11].\n");
	} while(true);
	
	return true;
}


typedef union {
	char c;
	short hd;
	unsigned short hu;
	int d;
	unsigned int u;
	long long lld;
	unsigned long long llu;
	float f;
	double lf;
	char str[8];
	uint64_t raw;
} data_types;

data_types* data;

#define NAME_SIZE 100

void handle_connection(int sock) {
	char input[64];
	
	// Local variables need to be in a specific order
	struct {
		char* name; // assert(&name == &formats[-1])
		const char* formats[10];
	} locals;
	
	unsigned choice;
	
	// Read in flag to a global variable
	read_flag();
	
	locals.formats[0] = "%c";
	locals.formats[1] = "%hd";
	locals.formats[2] = "%hu";
	locals.formats[3] = "%d";
	locals.formats[4] = "%u";
	locals.formats[5] = "%lld";
	locals.formats[6] = "%llu";
	locals.formats[7] = "%f";
	locals.formats[8] = "%lf";
	locals.formats[9] = "%8c";
	
	// locals.name is malloc-ed so it's a pointer (for scanf format) rather than an array
	locals.name = malloc(NAME_SIZE);
	
	printf("Hello random stranger, what shall I call you?\n");
	next_line(locals.name, NAME_SIZE);
	
	printf("Welcome, %s, to my wonderfully delicious, hexalicous data converter!\n", locals.name);
	printf("Input data, any type of data, and see what it looks like as hex!\n");
	
	while(menu_input(&choice)) {
		if(choice == 11) {
			break;
		}
		
		// If initially set (or user-corrupted) to NULL, reallocate and zero-fill
		if(data == NULL) {
			data = calloc(1, sizeof(*data));
		}
		
		printf("Enter your data:\n[>] ");
		if(!next_line(input, sizeof(input))) {
			break;
		}
		
		// Scanf with potentially user-controllable format string.
		// By corrupting data to point elsewhere, the player can write-what-where
		if(sscanf(input, locals.formats[choice - 1], (void*)data) != 1) {
			// If the player used a format string with more or fewer than one matched input,
			// don't dereference data
			printf("Failed to read input data as chosen type (%u)!\n", choice);
			continue;
		}
		
		// The player can overwrite data to point somewhere else to read-anywhere
		printf("As hex, your data looks like this: 0x%llx\n\n", data->raw);
	}
	
	printf("Goodbye, %s! Hopefully now you're more enlightened about how data is stored by computers!\n", locals.name);
}


int main(int argc, char** argv) {
	server_options defaults = {
		.user = "hexalicous",
		.chrooted = true,
		.port = 20003,
		.time_limit_seconds = 30
	};
	
	return server_main(argc, argv, defaults, &handle_connection);
}
