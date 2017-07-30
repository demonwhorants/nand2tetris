#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* C Commands : create lists for JMP and ALU CODES, iterate through
and call strstr on each line of assembly

Files for dicts: better to have a list of pointers?
*/

void a_command(char *asm_line) {

	puts("A command");
	return;
}

void c_command(char *asm_line) {

	puts("C command");
	return;
}
	

void prepare_asm(char *filename) {

	FILE *original_file = fopen(filename, "r");
	FILE *sanitised_file = fopen("sanitised_file", "a");
	
	char line[100];
	char IGNORE_LINE[] = { '\0', '\n', '\r', '/' };
	char EOL_CHARS[] = { 10, 13, 9, 32 };

	//remove comments, empty lines and trailing whitespace

	while(fgets(line, 100, original_file) != 0) {

		// ignore comment lines and empty lines
		if (line[0] == '/') {
			continue;		
		}
		else if (line[0] == '\r') {
			continue;		
		}
		else if (line[0] == '\n') {
			continue;		
		}
		else if (line[0] == '\0') {
			continue;		
		}
		else {

			
			char new_line[100]= {0};
			
			/* remove trailing & leading whitespace and inline
			comments before writing each asm command to a
			new file */

			for(int i = 0; i < strlen(line); i++) {
			

				if(line[i] == ' '){
					
					//ignore whitespace
					continue;
				}
				else if(line[i] == 10){

					//ignore cr etc 
					continue;
				}
				else if(line[i] == '/'){

					//ignore inline comments 
					break;
				}
				else {
					
					char *c = &line[i];	
					fputc(*c, sanitised_file);
					
				}

			}	

		fputs("\n", sanitised_file);

		}
	
	}

	fclose(sanitised_file);
	fclose(original_file);

}

void label_pass(char *s_file) {

	char line[100];

	FILE *sanitised_file = fopen(s_file, "r");
	FILE *label_dict = fopen("label_dict", "a");
	FILE *post_label_file = fopen("post_label_file", "a");

	while(fgets(line, 100, sanitised_file) != 0) {
		
		if(line[0] == '('){
			
			// remove first and last characters (brackets) from the line
			// https://stackoverflow.com/questions/1726298/strip-first-and-last-character-from-c-string
			char *label = line;			
			label++[strlen(label)-1] = 0;

			for(int i = 0; i < strlen(label); i++) {

				char *c = &label[i];	
				fputc(*c, label_dict);	// use this file like a dictionary key:value == line_num:line
				
			}

			fputs("\n", label_dict);

		}

		if(line[0] != '('){
			
			fputs(line, post_label_file);

			// 

		}

	}

	fclose(sanitised_file);
	fclose(label_dict);
	fclose(post_label_file);

}

void parse_asm(char *post_label_f) {

	FILE *post_label_file = fopen(post_label_f, "r");

	char line[100];

	while(fgets(line, 100, post_label_file) != 0) {

		char *asm_line = &line[0];

	    if (line[0] == '@') {
	        a_command(asm_line);
	    }
	    else {
	        c_command(asm_line);
	    }
		
	}

}



int main(int argc, char **argv) {

	char *filename = argv[1];
	char *sanitised_file = "sanitised_file";
	char *labels = "labels";
	char *post_label_file = "post_label_file";

	// delete old instances of files

	remove(sanitised_file);
	remove(labels);
	remove(post_label_file);



	prepare_asm(filename);

	label_pass(sanitised_file);
	
	parse_asm(post_label_file);
	
	return 0;
}