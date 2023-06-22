
# Build environment can be configured the following
# environment variables:
#   CC : Specify the C compiler to use
#   CFLAGS : Specify compiler options to use

CC = g++

# Required compiler parameters
CFLAGS += -I/usr/local/include

LDFLAGS = -L/usr/local/lib
LDLIBS = -lmseed

all: msview msrepack read

read: read.o
	$(CC) $(CFLAGS) -o $@ read.o $(LDFLAGS) $(LDLIBS)

msview: msview.o
	$(CC) $(CFLAGS) -o $@ msview.o $(LDFLAGS) $(LDLIBS)

msrepack: msrepack.o
	$(CC) $(CFLAGS) -o $@ msrepack.o $(LDFLAGS) $(LDLIBS)

clean:
	rm -f msview.o msview msrepack.o msrepack

install:
	@echo
	@echo "No install target, copy the executable(s) as needed"
	@echo
