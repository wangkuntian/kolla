from pathlib import Path


DOCKERFILE = Path("docker/ironic/ironic-pxe/Dockerfile.j2")
EXTEND_START = Path("docker/ironic/ironic-pxe/extend_start.sh")


def test_openeuler_ironic_pxe_keeps_esp_and_pxelinux_dependencies():
    dockerfile = DOCKERFILE.read_text()

    openeuler = dockerfile.split("{% if base_distro == 'openeuler' %}", 1)[1]
    openeuler = openeuler.split("{{ macros.install_packages", 1)[0]

    assert "'dosfstools'" in openeuler
    assert "'mtools'" in openeuler
    assert "'syslinux-tftpboot'" in openeuler


def test_openeuler_esp_image_uses_open_euler_efi_directory():
    script = EXTEND_START.read_text()

    esp_setup = script.split("function prepare_esp_image", 1)[1]
    esp_setup = esp_setup.split("if [[ \"${KOLLA_BASE_ARCH}\"", 1)[0]

    assert '${KOLLA_BASE_DISTRO}" == "openeuler"' in esp_setup
    assert 'efi_distro="openEuler"' in esp_setup


def test_openeuler_pxelinux_uses_installed_syslinux_directory():
    script = EXTEND_START.read_text()

    pxelinux = script.split("function prepare_pxe_pxelinux", 1)[1]
    pxelinux = pxelinux.split("# For UEFI boot mode", 1)[0]

    assert 'KOLLA_BASE_DISTRO}" =~ centos|rocky|openeuler' in pxelinux
    assert "/tftpboot/{pxelinux.0,chain.c32,ldlinux.c32}" in pxelinux
