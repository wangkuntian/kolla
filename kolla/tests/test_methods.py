# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from kolla.template import methods
from kolla.tests import base


class MethodsTest(base.TestCase):

    def test_debian_package_install(self):
        packages = ['https://packages.debian.org/package1.deb', 'package2.deb']
        result = methods.debian_package_install(packages)
        expectCmd = 'apt-get -y install --no-install-recommends package2.deb'
        self.assertEqual(expectCmd, result.split("&&")[1].strip())

    def test_enable_repos_centos_baseurl(self):
        template_vars = {
            'base_arch': 'x86_64',
            'base_distro': 'centos',
            'base_package_type': 'rpm',
        }

        result = methods.handle_repos(template_vars, ["grafana"], "enable")
        expectCmd = "RUN echo '[grafana]' "
        expectCmd += ">/etc/yum.repos.d/grafana.repo && "
        expectCmd += "echo 'name=grafana' "
        expectCmd += ">>/etc/yum.repos.d/grafana.repo && "
        expectCmd += "echo 'enabled=1' "
        expectCmd += ">>/etc/yum.repos.d/grafana.repo && "
        expectCmd += "echo 'gpgkey=https://rpm.grafana.com/gpg.key' "
        expectCmd += ">>/etc/yum.repos.d/grafana.repo && "
        expectCmd += "echo 'baseurl=https://rpm.grafana.com' "
        expectCmd += ">>/etc/yum.repos.d/grafana.repo"
        self.assertEqual(expectCmd, result)

    def test_enable_repos_centos_metalink(self):
        template_vars = {
            'base_arch': 'x86_64',
            'base_distro': 'centos',
            'base_package_type': 'rpm',
        }

        result = methods.handle_repos(template_vars, ["ceph"], "enable")
        expectCmd = "RUN echo '[centos-ceph-squid]' "
        expectCmd += ">/etc/yum.repos.d/ceph.repo && "
        expectCmd += "echo 'name=centos-ceph-squid' "
        expectCmd += ">>/etc/yum.repos.d/ceph.repo && "
        expectCmd += "echo 'enabled=1' "
        expectCmd += ">>/etc/yum.repos.d/ceph.repo && "
        expectCmd += "echo 'gpgkey=https://www.centos.org/keys/RPM-GPG-KEY-CentOS-SIG-Storage' "  # noqa: E501
        expectCmd += ">>/etc/yum.repos.d/ceph.repo && "
        expectCmd += "echo 'metalink=https://mirrors.centos.org/metalink?repo=centos-storage-sig-ceph-squid-10-stream&arch=$basearch' "  # noqa: E501
        expectCmd += ">>/etc/yum.repos.d/ceph.repo"
        self.assertEqual(expectCmd, result)

    def test_enable_repos_centos_arch(self):
        template_vars = {
            "base_arch": "aarch64",
            "base_distro": "centos",
            "base_package_type": "rpm",
        }

        result = methods.handle_repos(template_vars, ["grafana"], "enable")
        expectCmd = "RUN echo '[grafana]' "
        expectCmd += ">/etc/yum.repos.d/grafana.repo && "
        expectCmd += "echo 'name=grafana' "
        expectCmd += ">>/etc/yum.repos.d/grafana.repo && "
        expectCmd += "echo 'enabled=1' "
        expectCmd += ">>/etc/yum.repos.d/grafana.repo && "
        expectCmd += "echo 'gpgkey=https://rpm.grafana.com/gpg.key' "
        expectCmd += ">>/etc/yum.repos.d/grafana.repo && "
        expectCmd += "echo 'baseurl=https://rpm.grafana.com' "
        expectCmd += ">>/etc/yum.repos.d/grafana.repo"
        self.assertEqual(expectCmd, result)

    def test_enable_repos_missing_distro_repo_data(self):
        template_vars = {
            'base_arch': 'x86_64',
            'base_distro': 'missingdistro',
            'base_package_type': 'rpm',
        }

        result = methods.handle_repos(template_vars, ['influxdb'],
                                      'enable')
        expectCmd = ''
        self.assertEqual(expectCmd, result)

    def test_enable_repos_openeuler_influxdb(self):
        template_vars = {
            'base_arch': 'x86_64',
            'base_distro': 'openeuler',
            'base_package_type': 'rpm',
        }

        result = methods.handle_repos(template_vars, ['influxdb'],
                                      'enable')
        expectCmd = 'RUN dnf config-manager --enable influxdb || true'
        self.assertEqual(expectCmd, result)

    def test_enable_repos_openeuler_epel_skipped(self):
        template_vars = {
            'base_arch': 'x86_64',
            'base_distro': 'openeuler',
            'base_package_type': 'rpm',
        }

        result = methods.handle_repos(template_vars, ['epel'], 'enable')
        expectCmd = ''
        self.assertEqual(expectCmd, result)

    def test_enable_repos_openeuler_docker_ce(self):
        template_vars = {
            'base_arch': 'x86_64',
            'base_distro': 'openeuler',
            'base_package_type': 'rpm',
        }

        result = methods.handle_repos(template_vars, ['docker-ce'], 'enable')
        self.assertIn('https://download.docker.com/linux/centos/9/'
                      '$basearch/stable', result)
        self.assertNotIn('$releasever', result)

    def test_enable_repos_openeuler_epel_skipped_without_trailing_and(self):
        template_vars = {
            'base_arch': 'x86_64',
            'base_distro': 'openeuler',
            'base_package_type': 'rpm',
        }

        result = methods.handle_repos(template_vars, ['crb', 'epel'],
                                      'enable')
        expectCmd = 'RUN dnf config-manager --enable crb || true'
        self.assertEqual(expectCmd, result)

    def test_enable_repos_openeuler_mariadb_skipped(self):
        template_vars = {
            'base_arch': 'x86_64',
            'base_distro': 'openeuler',
            'base_package_type': 'rpm',
        }

        result = methods.handle_repos(template_vars, ['mariadb'], 'enable')
        expectCmd = ''
        self.assertEqual(expectCmd, result)

    def test_enable_repos_openeuler_proxysql(self):
        template_vars = {
            'base_arch': 'x86_64',
            'base_distro': 'openeuler',
            'base_package_type': 'rpm',
        }

        result = methods.handle_repos(template_vars, ['proxysql'], 'enable')
        expectCmd = "RUN echo '[proxysql]' >/etc/yum.repos.d/proxysql.repo"
        expectCmd += " && echo 'name=proxysql' "
        expectCmd += ">>/etc/yum.repos.d/proxysql.repo && "
        expectCmd += "echo 'enabled=1' >>/etc/yum.repos.d/proxysql.repo && "
        expectCmd += "echo 'gpgkey=https://repo.proxysql.com/ProxySQL/"
        expectCmd += "proxysql-3.0.x/repo_pub_key' "
        expectCmd += ">>/etc/yum.repos.d/proxysql.repo && "
        expectCmd += "echo 'baseurl=https://repo.proxysql.com/ProxySQL/"
        expectCmd += "proxysql-3.0.x/almalinux/9' "
        expectCmd += ">>/etc/yum.repos.d/proxysql.repo"
        self.assertEqual(expectCmd, result)

    def test_enable_repos_openeuler_opensearch_dashboards(self):
        template_vars = {
            'base_arch': 'x86_64',
            'base_distro': 'openeuler',
            'base_package_type': 'rpm',
        }

        result = methods.handle_repos(template_vars,
                                      ['opensearch-dashboards'],
                                      'enable')
        self.assertIn('opensearch-dashboards-3.x', result)
        self.assertIn('https://artifacts.opensearch.org/releases/bundle/'
                      'opensearch-dashboards/3.x/yum', result)

    def test_enable_repos_openeuler_opensearch(self):
        template_vars = {
            'base_arch': 'x86_64',
            'base_distro': 'openeuler',
            'base_package_type': 'rpm',
        }

        result = methods.handle_repos(template_vars, ['opensearch'],
                                      'enable')
        self.assertIn('opensearch-3.x', result)
        self.assertIn('https://artifacts.opensearch.org/releases/bundle/'
                      'opensearch/3.x/yum', result)

    def test_enable_repos_openeuler_openstack_antelope(self):
        template_vars = {
            'base_arch': 'x86_64',
            'base_distro': 'openeuler',
            'base_package_type': 'rpm',
        }

        result = methods.handle_repos(template_vars,
                                      ['openstack-antelope'],
                                      'enable')
        self.assertIn('openstack-antelope', result)
        self.assertIn('EPOL/multi_version/OpenStack/Antelope/$basearch',
                      result)

    def test_enable_repos_centos_multiple(self):
        template_vars = {
            "base_arch": "x86_64",
            "base_distro": "centos",
            "base_package_type": "rpm",
        }

        result = methods.handle_repos(template_vars,
                                      ["grafana", "rabbitmq"], "enable")
        expectCmd = "RUN echo '[grafana]' "
        expectCmd += ">/etc/yum.repos.d/grafana.repo && "
        expectCmd += "echo 'name=grafana' "
        expectCmd += ">>/etc/yum.repos.d/grafana.repo && "
        expectCmd += "echo 'enabled=1' "
        expectCmd += ">>/etc/yum.repos.d/grafana.repo && "
        expectCmd += "echo 'gpgkey=https://rpm.grafana.com/gpg.key' "
        expectCmd += ">>/etc/yum.repos.d/grafana.repo && "
        expectCmd += "echo 'baseurl=https://rpm.grafana.com' "
        expectCmd += ">>/etc/yum.repos.d/grafana.repo && "

        expectCmd += "echo '[rabbitmq_rabbitmq-server]' "
        expectCmd += ">/etc/yum.repos.d/rabbitmq.repo && "
        expectCmd += "echo 'name=rabbitmq_rabbitmq-server' "
        expectCmd += ">>/etc/yum.repos.d/rabbitmq.repo && "
        expectCmd += "echo 'enabled=1' "
        expectCmd += ">>/etc/yum.repos.d/rabbitmq.repo && "
        expectCmd += "echo 'gpgkey=https://github.com/rabbitmq/signing-keys/releases/download/3.0/cloudsmith.rabbitmq-server.9F4587F226208342.key' " # noqa
        expectCmd += ">>/etc/yum.repos.d/rabbitmq.repo && "
        expectCmd += "echo '       https://github.com/rabbitmq/signing-keys/releases/download/3.0/rabbitmq-release-signing-key.asc' " # noqa
        expectCmd += ">>/etc/yum.repos.d/rabbitmq.repo && "
        expectCmd += "echo 'baseurl=https://yum1.rabbitmq.com/rabbitmq/el/9/noarch' " # noqa
        expectCmd += ">>/etc/yum.repos.d/rabbitmq.repo && "
        expectCmd += "echo 'baseurl=https://yum2.rabbitmq.com/rabbitmq/el/9/noarch' " # noqa
        expectCmd += ">>/etc/yum.repos.d/rabbitmq.repo"
        self.assertEqual(expectCmd, result)

    def test_enable_repos_centos_distro_enable(self):
        template_vars = {
            "base_arch": "x86_64",
            "base_distro": "centos",
            "base_package_type": "rpm",
        }

        result = methods.handle_repos(template_vars,
                                      ['crb'], 'enable')
        expectCmd = "RUN dnf config-manager --enable crb || true"
        self.assertEqual(expectCmd, result)

    def test_enable_repos_centos_distro_disable(self):
        template_vars = {
            "base_arch": "x86_64",
            "base_distro": "centos",
            "base_package_type": "rpm",
        }

        result = methods.handle_repos(template_vars, ['crb'], 'disable')
        expectCmd = "RUN dnf config-manager --disable crb || true"
        self.assertEqual(expectCmd, result)

    def test_enable_repos_centos_distro_enable_multiple(self):
        template_vars = {
            "base_arch": "x86_64",
            "base_distro": "centos",
            "base_package_type": "rpm",
        }

        result = methods.handle_repos(template_vars,
                                      ['crb', 'grafana'], 'enable')
        expectCmd = "RUN dnf config-manager --enable crb || true && "
        expectCmd += "echo '[grafana]' "
        expectCmd += ">/etc/yum.repos.d/grafana.repo && "
        expectCmd += "echo 'name=grafana' "
        expectCmd += ">>/etc/yum.repos.d/grafana.repo && "
        expectCmd += "echo 'enabled=1' "
        expectCmd += ">>/etc/yum.repos.d/grafana.repo && "
        expectCmd += "echo 'gpgkey=https://rpm.grafana.com/gpg.key' "
        expectCmd += ">>/etc/yum.repos.d/grafana.repo && "
        expectCmd += "echo 'baseurl=https://rpm.grafana.com' "
        expectCmd += ">>/etc/yum.repos.d/grafana.repo"
        self.assertEqual(expectCmd, result)

    def test_enable_repos_debian(self):
        template_vars = {
            "base_arch": "x86_64",
            "base_distro": "debian",
            "base_package_type": "deb",
        }

        result = methods.handle_repos(template_vars, ["grafana"], "enable")
        expectCmd = "RUN echo 'Uris: https://apt.grafana.com' "
        expectCmd += ">/etc/apt/sources.list.d/grafana.sources && "
        expectCmd += "echo 'Components: main' "
        expectCmd += ">>/etc/apt/sources.list.d/grafana.sources && "
        expectCmd += "echo 'Types: deb' "
        expectCmd += ">>/etc/apt/sources.list.d/grafana.sources && "
        expectCmd += "echo 'Suites: stable' "
        expectCmd += ">>/etc/apt/sources.list.d/grafana.sources && "
        expectCmd += "echo 'Signed-By: /etc/kolla/apt-keys/grafana.asc' "
        expectCmd += ">>/etc/apt/sources.list.d/grafana.sources"
        self.assertEqual(expectCmd, result)

    def test_enable_repos_debian_arch(self):
        template_vars = {
            'base_arch': 'aarch64',
            'base_distro': 'debian',
            'base_package_type': 'deb',
        }

        result = methods.handle_repos(template_vars, ["rabbitmq"], "enable")
        expectCmd = "RUN echo 'Uris: https://deb1.rabbitmq.com/rabbitmq-server/debian/trixie' "  # noqa: E501
        expectCmd += ">/etc/apt/sources.list.d/rabbitmq.sources && "
        expectCmd += "echo 'Components: main' "
        expectCmd += ">>/etc/apt/sources.list.d/rabbitmq.sources && "
        expectCmd += "echo 'Types: deb' "
        expectCmd += ">>/etc/apt/sources.list.d/rabbitmq.sources && "
        expectCmd += "echo 'Suites: trixie' "
        expectCmd += ">>/etc/apt/sources.list.d/rabbitmq.sources && "
        expectCmd += "echo 'Signed-By: /etc/kolla/apt-keys/rabbitmq.gpg' "
        expectCmd += ">>/etc/apt/sources.list.d/rabbitmq.sources && "
        expectCmd += "echo 'Architectures: amd64' "
        expectCmd += ">>/etc/apt/sources.list.d/rabbitmq.sources"
        self.assertEqual(expectCmd, result)

    def test_enable_repos_debian_missing_repo(self):
        template_vars = {
            'base_arch': 'x86_64',
            'base_distro': 'debian',
            'base_package_type': 'deb',
        }

        self.assertRaises(KeyError, methods.handle_repos, template_vars,
                          ['missing_repo'], 'enable')

    def test_enable_repos_debian_multiple(self):
        template_vars = {
            'base_arch': 'x86_64',
            'base_distro': 'debian',
            'base_package_type': 'deb',
        }

        result = methods.handle_repos(template_vars,
                                      ['grafana', 'rabbitmq'], 'enable')
        expectCmd = "RUN echo 'Uris: https://apt.grafana.com' "
        expectCmd += ">/etc/apt/sources.list.d/grafana.sources && "
        expectCmd += "echo 'Components: main' "
        expectCmd += ">>/etc/apt/sources.list.d/grafana.sources && "
        expectCmd += "echo 'Types: deb' "
        expectCmd += ">>/etc/apt/sources.list.d/grafana.sources && "
        expectCmd += "echo 'Suites: stable' "
        expectCmd += ">>/etc/apt/sources.list.d/grafana.sources && "
        expectCmd += "echo 'Signed-By: /etc/kolla/apt-keys/grafana.asc' "
        expectCmd += ">>/etc/apt/sources.list.d/grafana.sources && "

        expectCmd += "echo 'Uris: "
        expectCmd += "https://deb1.rabbitmq.com/rabbitmq-server/debian/trixie/' "  # noqa: E501
        expectCmd += ">/etc/apt/sources.list.d/rabbitmq.sources && "
        expectCmd += "echo 'Components: main' "
        expectCmd += ">>/etc/apt/sources.list.d/rabbitmq.sources && "
        expectCmd += "echo 'Types: deb' "
        expectCmd += ">>/etc/apt/sources.list.d/rabbitmq.sources && "
        expectCmd += "echo 'Suites: trixie' "
        expectCmd += ">>/etc/apt/sources.list.d/rabbitmq.sources && "
        expectCmd += "echo 'Signed-By: /etc/kolla/apt-keys/rabbitmq.gpg' "
        expectCmd += ">>/etc/apt/sources.list.d/rabbitmq.sources"

        self.assertEqual(expectCmd, result)

    # NOTE(hrw): there is no disabling of repos for Debian/Ubuntu
    def test_disable_repos_debian(self):
        template_vars = {
            'base_arch': 'x86_64',
            'base_distro': 'debian',
            'base_package_type': 'deb',
        }

        result = methods.handle_repos(template_vars, ["grafana"], "disable")
        expectCmd = ""
        self.assertEqual(expectCmd, result)

    def test_handle_repos_string(self):
        template_vars = {
            'base_arch': 'x86_64',
            'base_distro': 'debian',
            'base_package_type': 'deb',
        }

        self.assertRaisesRegex(TypeError,
                               r'First argument should be a list of '
                               r'repositories',
                               methods.handle_repos, template_vars, 'grafana',
                               'disable')
