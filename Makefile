REGISTRY ?= localhost:5000
NAME ?= app

all: build push

build:
	docker build -t $(REGISTRY)/$(NAME) .
push:
	docker push $(REGISTRY)/$(NAME)
run: build
	docker run -it $(REGISTRY)/$(NAME)
login: build
	docker run -it $(REGISTRY)/$(NAME) /bin/bash
