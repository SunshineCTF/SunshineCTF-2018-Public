#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stddef.h>
#include <stdbool.h>
#include <inttypes.h>
#include "pwnable_harness.h"


typedef struct IntArray IntArray;
struct IntArray {
	size_t intCount;
	int* ints;
};


bool menu(char* line, size_t line_size) {
	printf(
		"What do you want to do?\n"
		"1) Create array of integers\n"
		"2) Create text string\n"
		"3) Edit array of integers\n"
		"4) Display array of integers\n"
		"5) Display text string\n"
		"6) Delete array of integers\n"
		"7) Delete text string\n"
		"0) Quit\n"
		"\n"
		"(>) "
	);
	
	if(!fgets(line, line_size, stdin)) {
		return false;
	}
	
	char* end = strchr(line, '\n');
	if(end) {
		*end = '\0';
	}
	
	return true;
}


IntArray* makeIntArray(unsigned intCount) {
	IntArray* arr = malloc(sizeof(*arr));
	
	arr->intCount = intCount;
	arr->ints = calloc(intCount, sizeof(int));
	
	return arr;
}


bool objectExists(uintptr_t find, uintptr_t* objects, size_t object_count) {
	size_t i;
	for(i = 0; i < object_count; i++) {
		if(objects[i] == find) {
			return true;
		}
	}
	
	return false;
}


void* readObject(uintptr_t* objects, size_t object_count, char* line, size_t line_size) {
	printf("Enter object ID:\n");
	if(!fgets(line, line_size, stdin)) {
		printf("Failed to read input\n");
		exit(EXIT_FAILURE);
	}
	
	uintptr_t ptr;
	if(sscanf(line, "%"SCNuPTR, &ptr) != 1) {
		printf("Failed to read input\n");
		exit(EXIT_FAILURE);
	}
	
	if(!objectExists(ptr, objects, object_count)) {
		printf("No object exists with ID %"PRIuPTR"!\n", ptr);
		return NULL;
	}
	
	return (void*)ptr;
}


void handle_connection(int sock) {
	char line[200];
	uintptr_t intArrs[20] = {};
	size_t intArr_count = 0;
	uintptr_t textStrs[20] = {};
	size_t textStr_count = 0;
	
	while(menu(line, sizeof(line))) {
		unsigned choice;
		if(sscanf(line, "%u", &choice) != 1 || choice > 7) {
			printf("Invalid choice, please enter a number [0-7].\n");
			continue;
		}
		
		switch(choice) {
			case 1: {
				if(intArr_count >= 20) {
					printf("Too many integer arrays!\n");
					break;
				}
				
				unsigned intCount;
				printf("How many integers?\n");
				if(!fgets(line, sizeof(line), stdin) || sscanf(line, "%u", &intCount) != 1) {
					printf("Failed to read input\n");
					exit(EXIT_FAILURE);
				}
				
				IntArray* intArr = makeIntArray(intCount);
				
				for(unsigned i = 0; i < intCount;) {
					printf("Enter %u integers:\n", intCount - i);
					if(!fgets(line, sizeof(line), stdin)) {
						printf("Failed to read input\n");
						exit(EXIT_FAILURE);
					}
					
					char* p = line + strspn(line, " \t,");
					while(i < intCount) {
						char* next;
						int cur = strtol(p, &next, 10);
						if(next == p) {
							break;
						}
						
						intArr->ints[i++] = cur;
						
						p = next + strspn(next, " \t,");
					}
				}
				
				intArrs[intArr_count++] = (uintptr_t)intArr;
				
				printf("ID of integer array: %"PRIuPTR"\n", (uintptr_t)intArr);
				break;
			}
			
			case 2: {
				if(textStr_count >= 20) {
					printf("Too many text strings!\n");
					break;
				}
				
				printf("Enter a text string:\n");
				if(!fgets(line, sizeof(line), stdin)) {
					printf("Failed to read input\n");
					exit(EXIT_FAILURE);
				}
				
				char* end = strchr(line, '\n');
				if(end) {
					*end = '\0';
				}
				
				char* textString = strdup(line);
				
				textStrs[textStr_count++] = (uintptr_t)textString;
				
				printf("ID of text string: %"PRIuPTR"\n", (uintptr_t)textString);
				break;
			}
			
			case 3: {
				IntArray* intArr = readObject(intArrs, intArr_count, line, sizeof(line));
				if(!intArr) {
					break;
				}
				
				printf("Enter index to change:\n");
				if(!fgets(line, sizeof(line), stdin)) {
					printf("Failed to read input\n");
					exit(EXIT_FAILURE);
				}
				
				unsigned index;
				if(sscanf(line, "%u", &index) != 1) {
					printf("Invalid input\n");
					break;
				}
				
				if(index >= intArr->intCount) {
					printf("Index out of bounds\n");
					break;
				}
				
				printf("Enter new value:\n");
				if(!fgets(line, sizeof(line), stdin)) {
					printf("Failed to read input\n");
					exit(EXIT_FAILURE);
				}
				
				int value;
				if(sscanf(line, "%d", &value) != 1) {
					printf("Invalid input\n");
					break;
				}
				
				intArr->ints[index] = value;
				printf("Value changed!\n");
				break;
			}
			
			case 4: {
				IntArray* intArr = readObject(intArrs, intArr_count, line, sizeof(line));
				if(!intArr) {
					break;
				}
				
				printf("Integer array:\n[");
				size_t i;
				for(i = 0; i < intArr->intCount; i++) {
					if(i > 0) {
						printf(", ");
					}
					printf("%d", intArr->ints[i]);
				}
				printf("]\n");
				break;
			}
			
			case 5: {
				char* textStr = readObject(textStrs, textStr_count, line, sizeof(line));
				if(!textStr) {
					break;
				}
				
				printf("Text string:\n\"%s\"\n", textStr);
				break;
			}
			
			case 6: {
				IntArray* intArr = readObject(intArrs, intArr_count, line, sizeof(line));
				if(!intArr) {
					break;
				}
				
				free(intArr->ints);
				free(intArr);
				
				printf("Deleted integer array!\n");
				break;
			}
			
			case 7: {
				char* textStr = readObject(textStrs, textStr_count, line, sizeof(line));
				if(!textStr) {
					break;
				}
				
				free(textStr);
				
				printf("Deleted text string!\n");
				break;
			}
			
			case 0:
				printf("Good bye!\n");
				return;
		}
		
		printf("\n");
	}
}


// Everything below can safely be ignored and is not part of the challenge
int main(int argc, char** argv) {
	server_options opts = {
		.user = "uaf",
		.chrooted = true,
		.port = 20001,
		.time_limit_seconds = 30
	};
	
	return server_main(argc, argv, opts, &handle_connection);
}
