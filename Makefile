
build-image:
	uv run kolla-build \
	--cache \
	--debug \
	--base openeuler \
	--openstack-release 2023.1 \
	--base-image openeuler-24.03-lts \
	--base-tag latest \
	--tag 2023.1 \
	--nopull

build-all:
	uv run kolla-build \
	--cache \
	--debug \
	--base openeuler \
	--openstack-release 2023.1 \
	--base-image openeuler-24.03-lts \
	--base-tag latest \
	--nopull \
	--tag 2023.1