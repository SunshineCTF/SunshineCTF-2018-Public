#include <stdio.h>
#include <string.h>
#include <stddef.h>
#include <stdint.h>
#include <ctype.h>
#include "pwnable_harness.h"


static void handle_connection(int sock) {
	char line[1024];
	
	puts("Welcome to Hackersoft Rot13 Encrypter Home and Student Edition 2018.");
	puts("  \"Because rot13 is the best encryption (tm)\" ~Eve");
	puts("");
	puts("Note: Hackersoft Rot13 Encrypter Home and Student Edition can only");
	puts("encrypt data. In order to decrypt rot13-encrypted data, you must");
	puts("purchase Hackersoft Rot13 Decrypter Professional 2018.");
	
	do {
		puts("\nEnter some text to be rot13 encrypted:");
		if(fgets(line, sizeof(line), stdin) == NULL) {
			break;
		}
		size_t datalen = strlen(line);
		
		int i;
		for(i = 0; i < datalen; i++) {
			char c = line[i];
			if(islower(c)) {
				c = ((c - 'a') + 13) % 26 + 'a';
			}
			else if(isupper(c)) {
				c = ((c - 'A') + 13) % 26 + 'A';
			}
			
			line[i] = c;
		}
		
		printf("Rot13 encrypted data: ");
		printf(line);
	} while(!feof(stdin));
	
	puts("Thank you for using Hackersoft Rot13 Encrypter Home and Student Edition 2018!");
}

int main(int argc, char** argv) {
	server_options opts = {
		.user = "rot13",
		.chrooted = true,
		.port = 20006,
		.time_limit_seconds = 30
	};
	
	return server_main(argc, argv, opts, &handle_connection);
}
