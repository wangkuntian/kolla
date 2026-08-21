from pathlib import Path


NEUTRON_IPTABLES_SCRIPTS = [
    Path("docker/neutron/neutron-base/extend_start.sh"),
    Path("docker/neutron/neutron-l3-agent/extend_start.sh"),
]


def test_openeuler_neutron_scripts_default_to_iptables_nft():
    for script in NEUTRON_IPTABLES_SCRIPTS:
        content = script.read_text()
        assert '[[ ${KOLLA_BASE_DISTRO} == "openeuler" ]]' in content
        assert "--set iptables /usr/sbin/iptables-nft" in content
        assert "--set ip6tables /usr/sbin/ip6tables-nft" in content
        assert "--set iptables /usr/sbin/iptables-legacy" in content
        assert "--set ip6tables /usr/sbin/ip6tables-legacy" in content


def test_openeuler_neutron_base_installs_iptables_nft():
    content = Path("docker/neutron/neutron-base/Dockerfile.j2").read_text()
    assert "'iptables-nft'" in content
