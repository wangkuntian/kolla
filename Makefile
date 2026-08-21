MAKEFILE_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

KOLLA_BUILD ?= kolla-build
KOLLA_BUILD_CONF ?= $(MAKEFILE_DIR)kolla-build.conf

BASE_DISTRO ?= openeuler
OPENSTACK_RELEASE ?= 2026.1
BASE_IMAGE ?= openeuler/openeuler
BASE_TAG ?= 24.03-lts-sp4
IMAGE_TAG ?= $(OPENSTACK_RELEASE)-$(BASE_DISTRO)-$(BASE_TAG)
REGISTRY ?= localhost:4000
REGISTRY_API ?= http://$(REGISTRY)

BUILD_FLAGS ?= --cache --debug \
	--config-file $(KOLLA_BUILD_CONF) \
	--base $(BASE_DISTRO) \
	--openstack-release $(OPENSTACK_RELEASE) \
	--base-image $(BASE_IMAGE) \
	--base-tag $(BASE_TAG) \
	--skip-existing \
	--nopull

IMAGE ?=
IMAGE_NAMESPACE ?= kolla
IMAGE_PREFIX ?=

.PHONY: help build-all build-image build-% start-registry push-image push-all registry-list registry-clear

help:
	@printf '%s\n' \
		'make build-all                     Build all images with the current defaults' \
		'make build-image IMAGE=nova        Build one or more named images' \
		'make push-image IMAGE=nova         Push one or more existing images to the local registry' \
		'make push-all                      Push all built images for the current tag to the local registry' \
		'make start-registry                Start the local Docker registry on localhost:4000' \
		'make registry-list                 Show the image list in the local Docker registry' \
		'make registry-clear                Remove the local registry container and image store' \
		'make build-nova                    Shortcut for a single image' \
		'make BASE_DISTRO=openeuler build-all'

build-all:
	$(KOLLA_BUILD) $(BUILD_FLAGS) --tag $(IMAGE_TAG)

ifeq ($(strip $(IMAGE)),)
build-image:
	@echo "Set IMAGE=<name> or use make build-all"; exit 1
else
build-image:
	$(KOLLA_BUILD) $(BUILD_FLAGS) --tag $(IMAGE_TAG) $(IMAGE)
endif

start-registry:
	./tools/start-registry

ifeq ($(strip $(IMAGE)),)
push-image:
	@echo "Set IMAGE=<name> or use make build-all"; exit 1
else
push-image:
	@set -e; \
	for image in $(IMAGE); do \
		src="$(IMAGE_NAMESPACE)/$(IMAGE_PREFIX)$$image:$(IMAGE_TAG)"; \
		dst="$(REGISTRY)/$(IMAGE_NAMESPACE)/$(IMAGE_PREFIX)$$image:$(IMAGE_TAG)"; \
		docker image tag "$$src" "$$dst"; \
		docker push "$$dst"; \
	done
endif

push-all:
	@set -e; \
	for image in $$(docker image ls --format '{{.Repository}}:{{.Tag}}' | awk -v ns="$(IMAGE_NAMESPACE)/$(IMAGE_PREFIX)" -v tag=":$(IMAGE_TAG)" '$$0 ~ "^" ns && $$0 ~ tag "$$" { sub("^" ns, "", $$0); sub(tag "$$", "", $$0); print }'); do \
		src="$(IMAGE_NAMESPACE)/$(IMAGE_PREFIX)$$image:$(IMAGE_TAG)"; \
		dst="$(REGISTRY)/$(IMAGE_NAMESPACE)/$(IMAGE_PREFIX)$$image:$(IMAGE_TAG)"; \
		docker image tag "$$src" "$$dst"; \
		docker push "$$dst"; \
	done

registry-list:
	curl -fsSL $(REGISTRY_API)/v2/_catalog | python3 -m json.tool

registry-clear:
	-docker rm -f registry
	-docker volume rm registry

build-%:
	$(KOLLA_BUILD) $(BUILD_FLAGS) --tag $(IMAGE_TAG) $*
