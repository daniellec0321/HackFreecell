TARGETS=	lib/hackFreecell.dll

all:	$(TARGETS)

lib/hackFreecell.o: lib/hackFreecell.c
	gcc -Wall -c -fpic -o $@ $^

lib/hackFreecell.dll: lib/hackFreecell.o
	gcc -shared -o $@ $^

clean:
	rm -rf lib/*.o lib/*.dll