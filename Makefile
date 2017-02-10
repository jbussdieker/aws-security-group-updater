REGISTRY ?= localhost:5000
NAME ?= app

all: run

build:
	docker build -t $(REGISTRY)/$(NAME) .
push:
	docker push $(REGISTRY)/$(NAME)
run: build
	docker run -e "OLD_CIDR=$(OLD_CIDR)" -e "NEW_CIDR=$(NEW_CIDR)" -e "AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID)" -e "AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY)" -it $(REGISTRY)/$(NAME)
login: build
	docker run -it $(REGISTRY)/$(NAME) /bin/bash
