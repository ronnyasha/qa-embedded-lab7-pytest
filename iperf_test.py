"""Тест пропускної здатності: кожен інтервал iperf3 має Transfer > 2 МБайт і Bitrate > 20 Мбіт/с."""
import os

import parser

MIN_TRANSFER = float(os.environ.get('MIN_TRANSFER', '2'))    # МБайт за інтервал
MIN_BITRATE = float(os.environ.get('MIN_BITRATE', '20'))     # Мбіт/с


class TestSuite():
    def test_iperf3_client_connection(self, client):
        """Перевіряє відсутність помилок і що значення Transfer та Bitrate не менші порогових."""
        assert client['server_error'] == '', f"Server error: {client['server_error']}"
        assert client['error'] == '', f"Client error: {client['error']}"

        intervals = parser.parser(client['output'])
        assert intervals, 'No intervals found in iperf3 output'

        for value in intervals:
            print(value)
            assert value['Transfer'] > MIN_TRANSFER, \
                f"Interval {value['Interval']}: Transfer {value['Transfer']} MBytes <= {MIN_TRANSFER}"
            assert value['Bitrate'] > MIN_BITRATE, \
                f"Interval {value['Interval']}: Bitrate {value['Bitrate']} Mbits/sec <= {MIN_BITRATE}"
