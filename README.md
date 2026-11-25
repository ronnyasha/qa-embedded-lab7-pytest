# Лабораторна робота №7. Основи використання фреймворку Pytest для автоматизації тестування

**Дисципліна:** Тестування та контроль якості (QA) вбудованих систем

**Виконала:** Павлюк В.О., група ІА-32 (КПІ ім. Ігоря Сікорського, ФІОТ)

## Оточення

| Вузол | Роль |
|---|---|
| PC1 (server), 10.0.0.1 | iperf3-сервер, OpenSSH-сервер |
| PC2 (client), 10.0.0.10 | iperf3-клієнт, Python 3.12, pytest 7.4.4, paramiko 2.12 |

## Файли

- `parser.py`: парсер виводу iperf3 (Interval, Transfer, Bitrate, Retr, Cwnd)
- `client.py`: частина 1, функція `client()` на `subprocess`
- `conftest.py`: фікстури `server` (SSH, paramiko, iperf3 -s) і `client` (iperf3 -c)
- `iperf_test.py`: тест: кожен інтервал Transfer > 2 МБайт і Bitrate > 20 Мбіт/с
- `ЛР7_Павлюк_ІА-32.docx`: звіт

## Запуск

```bash
# частина 1 (сервер вручну: iperf3 -s на PC1)
python3 client.py

# частина 2
read -s -p "SSH password: " SSH_PASSWORD; export SSH_PASSWORD; echo
pytest -v iperf_test.py                          # позитивний кейс
MIN_BITRATE=5000 pytest -v iperf_test.py         # негативний: значення нижче порогу
IPERF_SERVER_PORT=5555 pytest -v iperf_test.py   # негативний: невдале підключення до сервера
```

## Результати

| Сценарій | Результат |
|---|---|
| Позитивний | PASSED (11,39 с) |
| MIN_BITRATE=5000 | FAILED: Interval 1.00-2.00: Bitrate 4900.0 Mbits/sec <= 5000.0 |
| IPERF_SERVER_PORT=5555 | FAILED: Client error: unable to connect to server, Connection refused |
