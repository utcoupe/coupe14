#include <stdio.h>
#include <termios.h>
#include <unistd.h>
#include <string.h>
#include <time.h>
#include <sys/time.h>
#include <fcntl.h>

#include "compat.h"

int serial;

long timeMillis() {
        struct timeval tv;       
        if(gettimeofday(&tv, NULL) != 0) return 0;
        return (unsigned long)((tv.tv_sec * 1000ul) + (tv.tv_usec / 1000ul));        
}

void serial_send(char c){
	int n = write (serial, &c, 1);           // send 7 character greeting
}

unsigned char generic_serial_read() {
	char data;
	int nbr = 0;
	do {
		nbr = read (serial, &data, 1);
		usleep(100000);
	} while (nbr <= 0);
	data &= 0xFF;
	return data;
}

int nonblocking_read(char *data) {
	set_blocking(serial, 0);
	int n = read (serial, data, 1);
	set_blocking(serial, 1);
	return n;
}

int
set_interface_attribs (int fd, int speed, int parity)
{
        struct termios tty;
        memset (&tty, 0, sizeof tty);
        if (tcgetattr (fd, &tty) != 0)
        {
                return -1;
        }

        cfsetospeed (&tty, speed);
	cfsetispeed (&tty, speed);

        tty.c_cflag = (tty.c_cflag & ~CSIZE) | CS8;     // 8-bit chars
	tty.c_iflag &= ~(IGNBRK | INLCR | IGNCR | ICRNL);         // ignore break signal
	tty.c_lflag = 0;                // no signaling chars, no echo, no canonical processing
	tty.c_oflag = 0;                // no remapping, no delays
	tty.c_cc[VMIN]  = 0;            // read doesn't block
	tty.c_cc[VTIME] = 5;            // 0.5 seconds read timeout

	tty.c_iflag &= ~(IXON | IXOFF | IXANY); // shut off xon/xoff ctrl

        tty.c_cflag |= (CLOCAL | CREAD);// ignore modem controls, enable reading
        tty.c_cflag &= ~(PARENB | PARODD);      // shut off parity
	tty.c_cflag |= parity;
        tty.c_cflag &= ~CSTOPB;

        if (tcsetattr (fd, TCSANOW, &tty) != 0)
        {
                return -1;
        }
        return 0;
}

void
set_blocking (int fd, int should_block)
{
	struct termios tty;
        memset (&tty, 0, sizeof tty);
        if (tcgetattr (fd, &tty) != 0)
        {
                return;
        }

        tty.c_cc[VMIN]  = should_block ? 1 : 0;
        tty.c_cc[VTIME] = 5;            // 5 seconds read timeout

        if (tcsetattr (fd, TCSANOW, &tty) != 0);
}

/*
...
char *portname = SERIAL_PATH
 ...
 int fd = open (portname, O_RDWR | O_NOCTTY | O_SYNC);
 if (fd < 0)
{
	        error_message ("error %d opening %s: %s", errno, portname, strerror (errno));
		        return;
}

set_interface_attribs (fd, B115200, 0);  // set speed to 115,200 bps, 8n1 (no parity)
set_blocking (fd, 0);                // set no blocking

write (fd, "hello!\n", 7);           // send 7 character greeting
char buf [100];
int n = read (fd, buf, sizeof buf); 

The values for speed are B115200, B230400, B9600, B19200, B38400, B57600, B1200, B2400, B4800, etc. The values for parity are 0 (meaning no parity), PARENB|PARODD (enable parity and use odd), PARENB (enable parity and use even), PARENB|PARODD|CMSPAR (mark parity), and PARENB|CMSPAR (space parity).
*/
