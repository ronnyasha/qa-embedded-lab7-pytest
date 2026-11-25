"""Частина 1: підключення до iperf3-сервера через subprocess і аналіз результату."""
import subprocess
import sys

import parser

# IP-адреса iperf3-сервера (PC1). У цій частині сервер піднімаємо вручну: iperf3 -s
server_ip = '10.0.0.1'


def client(server_ip):
    """Запускає iperf3-клієнт і повертає (вивід, помилка)."""
    proc = subprocess.Popen(
        ['iperf3', '-c', server_ip, '-t', '10', '-i', '1'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        out, err = proc.communicate(timeout=30)
    except subprocess.TimeoutExpired:
        proc.kill()
        return '', 'iperf3: timeout'
    if proc.returncode != 0 and not err:
        err = out.strip().splitlines()[-1] if out.strip() else f'iperf3 exited with code {proc.returncode}'
    return out, err


if __name__ == '__main__':
    ip = sys.argv[1] if len(sys.argv) > 1 else server_ip
    result, error = client(ip)
    if error:
        print('ERROR:', error)
        sys.exit(1)
    result_list = parser.parser(result)
    print(f'Отримано інтервалів: {len(result_list)}')
    for value in result_list:
        if value['Transfer'] > 2 and value['Bitrate'] > 20:
            print(value)
