import asyncio
import aiohttp
import time
from config import py_logger
from decouple import config
from utils import generate_barcode, queue_to_list, log_status
from fetcher import fetch_product_by_barcode
from database import fetch_ids_by_table, insert_products


async def main():   
    API_URL =  config("API")
    
    country_manufacturer_codes = await fetch_ids_by_table("country_and_manufacturer")
    if not country_manufacturer_codes:
        return
    
    #Посик по списку стран и производителей
    for code in country_manufacturer_codes:
        start_time = time.perf_counter()


        products_queue = asyncio.Queue()
        statuses_queue = asyncio.Queue()
        barcodes = [
            generate_barcode(code, num)
            for num in range(0, 100_000)
        ]

        # Сбор товаров по баркоду
        semaphore = asyncio.Semaphore(1)
        async with aiohttp.ClientSession() as session:
            tasks = [
                fetch_product_by_barcode(session, semaphore, barcode, products_queue, statuses_queue, API_URL)
                for barcode in barcodes
            ]

            await asyncio.gather(*tasks, return_exceptions=True)
        py_logger.info(f"Execution time fetch products: {time.perf_counter() - start_time:.2f} seconds")
        start_time = time.perf_counter()
        log_status(await queue_to_list(statuses_queue))

        if products_queue.empty():
            return
            
        # Запись в базу данных
        products = await queue_to_list(products_queue)
        await insert_products(products)
        py_logger.info(f"Execution time insert products: {time.perf_counter() - start_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())