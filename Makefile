UNAME_S := $(shell uname -s)

USERID=$(shell id -u)

ifeq ($(UNAME_S), Darwin)
GROUPID=1000
else
GROUPID=$(shell id -g)
endif

help:
	@echo "Please use \`make <target>\` where <target> is one of"
	@echo "  build                   build the pbest image"
	@echo "  clean                   remove the pbest image from your computer"
	@echo "  "

init:
	mkdir -p ~/.local/bin
	export PATH=$PATH:~/.local/bin
	chmod +x `pwd`/scripts/pbest-test.sh
	ln -sf `pwd`/scripts/pbest-test.sh ~/.local/bin/pbest-test
	chmod +x `pwd`/scripts/pbest.sh
	ln -sf `pwd`/scripts/pbest.sh ~/.local/bin/pbest

build: init
	docker build -t "pbest:Dockerfile" --build-arg USER_ID=${USERID} --build-arg GROUP_ID=${GROUPID} --no-cache .
	@echo "\nReady to start. Try:"
	@echo "\tpbest --help"
	@echo "\tpbest-test --help"

clean:
	docker rmi -f pbest:Dockerfile
