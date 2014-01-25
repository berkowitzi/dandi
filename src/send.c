#include <linux/soundcard.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
//static unsigned char gethex(const char *s, char **endptr) {
//	assert(s);
//	while( isspace(*s)) s++;
//	assert(*s);
//	return stroul(s,endptr,16);
//}
//unsigned char *convert(const char *s, int *length) {
//	unsigned char *answer = malloc((strlen(s) + 1) / 3);
//	unsigned char *p;
//	for (p = answer; *s; p++)
//		*p = gethex(s, (char **)&s);
//	*length = p - answer;
//	return answer;
//}
int main(int argc, char** argv) {
	char* device = "/dev/midi1";
//	unsigned char data[] = {0xF0, 0x7F, deviceID, 0x02, 0x01, GO, 0x31, 0x30, 0x00, stack, 0xF7};
	unsigned char data[] = convert(argv[1],strlen(argv[1]));
	int fd = open(device, O_WRONLY, 0);
	if (fd < 0) {
		printf("Error opening MIDI device");
		exit(1);
	}
	write(fd,data,sizeof(data));
	close(fd);
	printf("DONE!");
	return 0;
}
