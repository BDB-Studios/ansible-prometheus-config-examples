import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_prometheus_user_exists(host):
    user = host.user('prometheus')
    assert user.exists
    assert 'prometheus' in user.groups


def test_prometheus_common_dir_exists(host):
    path = '/opt/prometheus/exporters'
    assert host.file(path).exists
    assert host.file(path).is_directory


def test_prometheus_log_dir_exists(host):
    path = '/var/log/prometheus'
    assert host.file(path).exists
    assert host.file(path).is_directory


def test_prometheus_conf_dir_exists(host):
    path = '/etc/prometheus/exporters'
    assert host.file(path).exists
    assert host.file(path).is_directory


def test_prometheus_home_dir_exists(host):
    path = '/var/lib/prometheus'
    assert host.file(path).exists
    assert host.file(path).is_directory
