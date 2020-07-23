AUTHOR?=dairlair
APP=facekeeper

GIT_COMMIT:=$(shell git rev-parse --short HEAD)
GIT_UNTRACKED_CHANGES:=$(shell git status --porcelain --untracked-files=no)
ifneq ($(GIT_UNTRACKED_CHANGES),)
	GIT_COMMIT := $(GIT_COMMIT)-dirty
endif

RELEASE=$(GIT_COMMIT)

# Docker settings
DOCKER_REGISTRY?=docker.io
DOCKER_IMAGE?=${AUTHOR}/${APP}
DOCKER_REGISTRY_IMAGE=${DOCKER_REGISTRY}/${DOCKER_IMAGE}

.PHONY: image
image:
	docker build -t $(DOCKER_IMAGE):$(RELEASE) .
	docker tag $(DOCKER_IMAGE):$(RELEASE) $(DOCKER_IMAGE):latest

.PHONY: run
run: image
	docker run --rm --name=$(APP) -p "80:80" $(DOCKER_IMAGE):latest

.PHONY: publish
publish: image
	docker push $(DOCKER_REGISTRY_IMAGE):$(RELEASE)
	docker push $(DOCKER_REGISTRY_IMAGE):latest