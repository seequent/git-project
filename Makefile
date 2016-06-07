
.PHONY: all help install uninstall test

all: help 

help:
	@echo 'Usage: make COMMAND'
	@echo
	@echo 'Commands:'
	@echo '    help:       Display this message'
	@echo '    install:    Install git-project'
	@echo '    uninstall:  Uninstall git-project'
	@echo

install: 
	@chmod 755 git-project
	cp git-project /usr/local/bin

install-local:
	@mkdir -p ~/git-project/bin
	cp git-project ~/git-project/bin

uninstall:
	rm /usr/local/bin/git-project

