
SYSPATH = /usr/local/bin
LOCALPATH = $(HOME)/git-project/bin
EXE = git-project

.PHONY: all help install uninstall tests reinstall

all: help

help:
	@echo 'Usage: make COMMAND'
	@echo
	@echo 'Commands:'
	@echo '    help:       Display this message'
	@echo '    install:    Install git-project'
	@echo '    uninstall:  Uninstall git-project'
	@echo '    tests:      Run automated tests'
	@echo

install:
	@if touch $(SYSPATH)/$(EXE) 2>/dev/null; then \
		cp $(EXE) $(SYSPATH)/; \
		chmod +x $(SYSPATH)/$(EXE); \
	else \
		mkdir -p $(LOCALPATH); \
		cp $(EXE) $(LOCALPATH)/; \
		chmod +x $(LOCALPATH)/$(EXE); \
	fi

uninstall:
	@if touch $(SYSPATH)/$(EXE); then \
		rm $(SYSPATH)/$(EXE); \
	else \
	    rm $(LOCALPATH)/$(EXE); \
	fi

reinstall: uninstall install

tests:
	nosetests
