import os
import asyncio
from collections import Counter
from models import RequestStatus
from config import py_logger

current_path = os.path.abspath(__file__)
parent_path = os.path.dirname(current_path)
grandparent_path = os.path.dirname(parent_path)


def write_file(lst: list, name_file: str):
    try:    
        with open(f"{grandparent_path}/failed_records/{name_file}.txt", "w", encoding="utf-8") as f:
            for item in lst:
                f.write(f"{item.id};{item.barcode};{item.name}\n")
    except IOError as e:
        py_logger.exception(f"Error writing to file: {e}")


def generate_barcode(country_manufacturer_code: str, num: int) -> str:
    barcode = f"{country_manufacturer_code}{num:05d}"

    odd_sum = sum(int(d) for d in barcode[::2])
    even_sum = sum(int(d) for d in barcode[1::2]) * 3
    last_digit = (10 - (odd_sum + even_sum) %10 ) % 10

    return f"{barcode}{last_digit}"


async def queue_to_list(queue: asyncio.Queue) -> list:
    lst = []
    while True:
        try:
            lst.append(queue.get_nowait())
        except asyncio.QueueEmpty:
            break
    return lst


def log_status(statuses: list):
    status_counts = Counter(statuses)
    for item, count in status_counts.items():
        match item:
            case int(value):
                py_logger.info(f"Status {value}: {count}")
            case RequestStatus(status, url):
                py_logger.info(f"Failed get request. Status: {status}, URL: {url}")