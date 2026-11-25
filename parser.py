"""Парсер виводу iperf3-клієнта."""
import re

# [  5]   0.00-1.00   sec   273 MBytes  2.29 Gbits/sec    0   3.04 MBytes
REGEXP = re.compile(
    r'\[\s*\d+\]\s+(?P<Interval>[\d.]+-[\d.]+)\s+sec\s+'
    r'(?P<Transfer>[\d.]+)\s+(?P<tu>[KMG]?)Bytes\s+'
    r'(?P<Bitrate>[\d.]+)\s+(?P<bu>[KMG]?)bits/sec\s+'
    r'(?P<Retr>\d+)\s+'
    r'(?P<Cwnd>[\d.]+)\s+(?P<cu>[KMG]?)Bytes'
)

KEYS = ('Interval', 'Transfer', 'Bitrate', 'Retr', 'Cwnd')

# Переведення в єдині одиниці: Transfer -> МБайт, Bitrate -> Мбіт/с, Cwnd -> КБайт
TO_MBYTES = {'': 1 / 1024 / 1024, 'K': 1 / 1024, 'M': 1, 'G': 1024}
TO_MBITS = {'': 1e-6, 'K': 1e-3, 'M': 1, 'G': 1000}
TO_KBYTES = {'': 1 / 1024, 'K': 1, 'M': 1024, 'G': 1024 * 1024}


def parser(output):
    """Повертає список усіх інтервалів iperf3 у вигляді словників з ключами KEYS."""
    result = []
    for m in REGEXP.finditer(output or ''):
        result.append({
            'Interval': m['Interval'],
            'Transfer': round(float(m['Transfer']) * TO_MBYTES[m['tu']], 2),
            'Bitrate': round(float(m['Bitrate']) * TO_MBITS[m['bu']], 2),
            'Retr': float(m['Retr']),
            'Cwnd': round(float(m['Cwnd']) * TO_KBYTES[m['cu']], 2),
        })
    return result
