import os
import logging
from decouple import config

current_path = os.path.abspath(__file__)
parent_path = os.path.dirname(current_path)
grandparent_path = os.path.dirname(parent_path)


DB_CONFIG = {
    "host": config("DB_HOST"),
    "database": config("DB_NAME"),
    "user": config("DB_USER"),
    "password": config("DB_PASSWORD"),
    "port": config("DB_PORT"),
}

HEADERS_TEMPLATE = {
    'user-agent': 'Dart/3.5 (dart:io)',
    'appinfo': 'eyJhcHBfdmVyc2lvbiI6IjcuNC4yKzY2NCIsImRldmljZSI6ImFuZHJvaWQiLCJkZXZpY2VfaWQiOiJUUTJCLjIzMDUwNS4wMDUuQTEiLCJvc192ZXJzaW9uIjoic2RrOjMzIiwibW9kZWwiOiJQaXhlbCIsInNpZ25hdHVyZSI6IjE5YWU0YTg4OTBlZmMxODQ0MzRiNmM1ODkzZjVkZDU4NGI2OTU5ZjQxYTFhYWZjYzMyZWEyOGEzNzU2ZTBiNjUifQ==',
    'appversion': '7.4.2+664',
    'bristolapitoken': 'token',
    'userguid': '23fa8238cb72c3587f267d20a1dd6219958e6092c70ec2ec82cd557d84f3e2dc',
    'accept-encoding': 'gzip',
    'buildnumber': '664',
    'host': 'api.mobile.bristol.ru',
    'hash': '3cf0768cfb87283de903f340ee0286bd',
    'timestamp': '1741695982470',
    'anontoken': '23fa8238cb72c3587f267d20a1dd6219958e6092c70ec2ec82cd557d84f3e2dc'
}

py_logger = logging.getLogger("bristol_mobile_barcode")
py_logger.setLevel(logging.INFO)

# Обработчик для записи в файл
py_handler = logging.FileHandler(f"{grandparent_path}/logs/bristol_mobile_barcode.log", mode='w', encoding="utf-8")
py_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
py_handler.setFormatter(py_formatter)

# Обработчик для вывода в консоль
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
console_handler.setFormatter(console_formatter)

# Добавляем оба обработчика к логгеру
py_logger.addHandler(py_handler)
py_logger.addHandler(console_handler)
