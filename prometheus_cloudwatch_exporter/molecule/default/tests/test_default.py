import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


path = '/opt/prometheus/exporters/dist/cloudwatch_exporter'
filename = 'cloudwatch_exporter-0.6.0-jar-with-dependencies.jar'


def test_config_file(host):
    file = host.file('{}/config.yml'.format(path))

    assert file.exists
    assert file.user == 'prometheus'
    assert file.group == 'prometheus'


def test_stats_file(host):
    file = host.file('{}/stats'.format(path))

    assert file.exists
    assert file.user == 'prometheus'
    assert file.group == 'prometheus'


def test_exporter_symlink(host):
    file = host.file('/opt/prometheus/exporters/cloudwatch_exporter_current')

    assert file.exists
    assert file.is_symlink
    assert file.linked_to == '{}/{}'.format(path, filename)
    assert file.user == 'root'
    assert file.group == 'root'


def test_prometheus_user_exists(host):
    user = host.user('prometheus')
    assert user.exists
    assert 'prometheus' in user.groups


def test_exporter_installed(host):
    file_name = '/opt/prometheus/exporters/cloudwatch_exporter_current'
    file = host.file(file_name)

    assert file.exists
    assert file.user == 'root'
    assert file.group == 'root'


def test_exporter_is_running(host):
    s_name = 'prometheus-cloudwatch-exporter.service'
    service = host.service(s_name)

    assert service.is_enabled
    assert service.is_running


def test_exporter_is_listenin(host):
    sock = "tcp://127.0.0.1:9106"
    listener = host.socket(sock)

    assert listener.is_listening
