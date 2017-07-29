#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {

	FILE *asm_file = fopen(argv[1], "r");

	char line[100];

	while(fgets(line, 100, asm_file) != 0) {

		printf("%s", line);
	}
	
	return 0;
}