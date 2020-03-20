import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


path = '/opt/prometheus/exporters/dist/graphite_exporter-0.6.2.linux-amd64'
filename = 'graphite_exporter'


def test_exporter_symlink(host):
    file = host.file('/opt/prometheus/exporters/graphite_exporter_current')

    assert file.exists
    assert file.is_symlink
    assert file.linked_to == '{}'.format(path)
    assert file.user == 'root'
    assert file.group == 'root'


def test_prometheus_user_exists(host):
    user = host.user('prometheus')
    assert user.exists
    assert 'prometheus' in user.groups


def test_exporter_installed(host):
    path = '/opt/prometheus/exporters/graphite_exporter_current'
    file = host.file('{}/{}'.format(path, filename))

    assert file.exists
    assert file.user == 'prometheus'
    assert file.group == 'prometheus'


def test_exporter_is_running(host):
    s_name = 'prometheus-graphite-exporter.service'
    service = host.service(s_name)

    assert service.is_enabled
    assert service.is_running


def test_exporter_is_listenin(host):
    sock = "tcp://127.0.0.1:9109"
    listener = host.socket(sock)

    assert listener.is_listening
