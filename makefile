CC = clang
CFLAGS = -Wall -std=c99 -pedantic

all: libmol.so mol.o molecule_wrap.c molecule.py molecule_wrap.o _molecule.so

_molecule.so: molecule_wrap.o libmol.so
	$(CC) -shared molecule_wrap.o -L. -L/usr/include/python3.7/config-3.7m-x86_64-linux-gnu -dynamiclib -lmol -lpython3.7m -o _molecule.so

molecule_wrap.o: molecule_wrap.c
	$(CC) $(CFLAGS) -c -fPIC -I/usr/include/python3.7m molecule_wrap.c -o molecule_wrap.o

molecule_wrap.c molecule.py: molecule.i
	swig3.0 -python molecule.i

libmol.so: mol.o
	$(CC) $(CFLAGS) mol.o -shared -o libmol.so

mol.o: mol.c mol.h
	$(CC) $(CFLAGS) -c -fPIC mol.c

clean:
	rm -f *.o *.so *.svg molecule_wrap.c molecule.py 