#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stddef.h>
#include <string.h>
#include "pwnable_harness.h"


typedef struct Book Book;
typedef struct BookPage BookPage;

struct BookPage {
	char* text;
	BookPage* prev;
	BookPage* next;
};

struct Book {
	BookPage* current_page;
};


static BookPage g_cover = {
	.text = (char*)"COVER",
	.prev = NULL,
	.next = NULL
};


BookPage* BookPage_create(char* text) {
	BookPage* page = malloc(sizeof(*page));
	page->text = text;
	return page;
}


void BookPage_destroy(BookPage* self) {
	if(!self || self == &g_cover) {
		return;
	}
	
	// Doubly linked list node unlink
	BookPage* prev = self->prev;
	BookPage* next = self->next;
	prev->next = next;
	next->prev = prev;
	
	free(self->text);
	free(self);
}


Book* Book_create(void) {
	Book* book = malloc(sizeof(*book));
	book->current_page = &g_cover;
	return book;
}


void Book_destroy(Book* self) {
	BookPage* page = self->current_page;
	while(!(page == &g_cover && page->next == &g_cover)) {
		BookPage* next = page->next;
		BookPage_destroy(page);
		page = next;
	}
	
	free(self);
}


void publishBook(void) {
	BookPage* page = &g_cover;
	do {
		printf("Page %u:\n\n%s\n\n\n", (unsigned)page, page->text);
		page = page->next;
	} while(page != &g_cover);
}


bool menu_input(Book* book, char* line, size_t line_size) {
	printf("\nPage number %u:\n\n%s\n", (unsigned)book->current_page, book->current_page->text);
	printf(
		"\n"
		"What do you want to do?\n"
		"1. Flip to the previous page\n"
		"2. Flip to the next page\n"
		"3. Insert a new page after this one\n"
		"4. Remove this page\n"
		"5. Publish the book\n"
		"0. Discard changes and quit BookWriter\n"
		"\n"
		"> "
	);
	
	if(!fgets(line, sizeof(line), stdin)) {
		return false;
	}
	
	char* end = strchr(line, '\n');
	if(end) {
		*end = '\0';
	}
	
	return true;
}


void handle_connection(int sock) {
	setenv("IS_THIS_A_NASTY_HACK", "1", 0);
	
	// The cover starts with its previous and next pointers pointing to itself
	// (circular doubly linked list with one element)
	g_cover.prev = g_cover.next = &g_cover;
	
	Book* book = Book_create();
	
	printf(
		"Welcome to BookWriter!\n"
		"\n"
		"A new, blank book has been created for you.\n"
	);
	
	char line[200];
	while(menu_input(book, line, sizeof(line))) {
		unsigned choice;
		if(sscanf(line, "%u", &choice) != 1 || choice > 5) {
			printf("Invalid input, please enter a number [0-5].\n");
			continue;
		}
		
		switch(choice) {
			case 1:
				book->current_page = book->current_page->prev;
				break;
			
			case 2:
				book->current_page = book->current_page->next;
				break;
			
			case 3: {
				char* pageText = NULL;
				size_t pageLength = 0;
				
				printf("Write the contents of this new page. End it with a line containing only END\n\n");
				while(fgets(line, sizeof(line), stdin) && strcmp(line, "END\n")) {
					size_t newSize = pageLength + strlen(line) + 1;
					
					// Enlarge the pageText buffer to fit the new line
					void* bigger = realloc(pageText, newSize);
					if(!bigger) {
						free(pageText);
						printf("Failed to enlarge page text buffer!\n");
						exit(EXIT_FAILURE);
					}
					
					// Copy the new line to the end of the page buffer
					pageText = bigger;
					memcpy(pageText + pageLength, line, newSize - pageLength);
					pageLength = newSize - 1;
				}
				
				// Create new page object
				BookPage* page = BookPage_create(pageText);
				
				// Insert the new page after the current page in the doubly linked list
				page->prev = book->current_page;
				page->next = book->current_page->next;
				
				page->prev->next = page;
				page->next->prev = page;
				
				// Update current page to the new one
				book->current_page = page;
				break;
			}
			
			case 4:
				// Remove this page from the book
				BookPage_destroy(book->current_page);
				break;
			
			case 5:
				// Publish the book by printing it out
				publishBook();
				return;
			
			case 0:
				printf("Are you sure you want to exit? Your changes will be discarded!\n[y/N] ");
				if(fgets(line, sizeof(line), stdin) && strncasecmp(line, "y", 1) == 0) {
					Book_destroy(book);
					return;
				}
				break;
			
			default:
				printf("Invalid choice (%u), please enter a number [0-5].\n", choice);
				break;
		}
	}
}


// Everything below can safely be ignored and is not part of the challenge
int main(int argc, char** argv) {
	server_options opts = {
		.user = "bookwriter",
		.chrooted = true,
		.port = 20002,
		.time_limit_seconds = 30
	};
	
	return server_main(argc, argv, opts, &handle_connection);
}
