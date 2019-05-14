run_webserver:
	setarch i386 -3R ./webserver 9264

build_webserver:
	gcc -m32 -z execstack -fno-stack-protector webserver.c -o webserver

