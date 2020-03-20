import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_exporter_installed(host):
    path = '/usr/bin/process-exporter'
    file = host.file(path)
    assert file.exists


def test_exporter_is_running(host):
    s_name = 'process-exporter.service'
    service = host.service(s_name)
    assert service.is_enabled
    assert service.is_running


def test_exporter_is_listening(host):
    sock = "tcp://127.0.0.1:9256"
    listener = host.socket(sock)
    assert listener.is_listening
