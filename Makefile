all: install build

build:
	# build image, setting fenics uid to match jupyterhub
	docker build -t singleuser --build-arg UID=$(shell id -u jupyterhub) --build-arg GID=$(shell id -g jupyterhub) docker

install:
	./install.sh

start:
	supervisorctl start juptyerhub

restart:
	supervisorctl restart jupyterhub

clean-containers:
	-docker rm -f $(shell docker ps -a | grep 'jupyter-' | awk '{print $$1}')

clean-all: clean-containers
	rm -f jupyterhub_cookie_secret jupyterhub.sqlite
