"""Фікстури для сервера (через SSH/paramiko) і клієнта (через subprocess)."""
import os
import subprocess
import time

import paramiko
import pytest

# Дані сервера для підключення по SSH. Пароль не зберігаємо в коді:
# перед запуском виконати  export SSH_PASSWORD='...'
server_ip = os.environ.get('SERVER_IP', '10.0.0.1')
username = os.environ.get('SSH_USER', 'veronika_pavliuk')
password = os.environ.get('SSH_PASSWORD', '')

# Порт, на якому піднімається сервер, і порт, до якого підключається клієнт.
# Різні значення дозволяють змоделювати невдалий запуск/підключення до сервера.
server_port = int(os.environ.get('IPERF_SERVER_PORT', '5201'))
client_port = int(os.environ.get('IPERF_CLIENT_PORT', '5201'))
duration = int(os.environ.get('IPERF_TIME', '10'))


@pytest.fixture(scope='function')
def server():
    """Підключається до сервера по SSH і піднімає iperf3-сервер.
    Після тесту (teardown після yield) зупиняє iperf3 і закриває SSH-з'єднання.
    :return: повідомлення про помилку від сервера (порожній рядок, якщо помилки немає)
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server_ip, username=username, password=password, timeout=10)

    ssh.exec_command('pkill -x iperf3')[1].channel.recv_exit_status()
    _, out, err = ssh.exec_command(f'iperf3 -s -1 -D -p {server_port}')
    out.channel.recv_exit_status()
    error = err.read().decode().strip()
    time.sleep(1)
    _, out, _ = ssh.exec_command('pgrep -x iperf3')
    if not out.read().decode().strip() and not error:
        error = 'iperf3 server is not running'

    yield error

    ssh.exec_command('pkill -x iperf3')[1].channel.recv_exit_status()
    ssh.close()


@pytest.fixture(scope='function')
def client(server):
    """Запускає iperf3-клієнт і повертає вивід, помилку клієнта та помилку сервера."""
    proc = subprocess.Popen(
        ['iperf3', '-c', server_ip, '-p', str(client_port), '-t', str(duration), '-i', '1'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = proc.communicate(timeout=duration + 30)
    if proc.returncode != 0 and not err:
        err = out.strip().splitlines()[-1] if out.strip() else f'iperf3 exited with code {proc.returncode}'
    return {'output': out, 'error': err.strip(), 'server_error': server}
