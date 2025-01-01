.PHONY: all docker start

DOCKER_CONTEXT=.
IMAGE_NAME=hellcash
DOCKERFILE=docker/Dockerfile

all: build

build:
	docker build -t $(IMAGE_NAME) -f $(DOCKERFILE) $(DOCKER_CONTEXT)

start:
	# requires image to be already built
	docker run -it --net=host hellcash poetry run src/manage.py runserver
