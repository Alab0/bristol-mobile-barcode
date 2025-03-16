import asyncio
import aiohttp
from config import py_logger, HEADERS_TEMPLATE
from models import Product, RequestStatus


async def send_test_barcode(session, API_URL):
    try: 
        async with session.get(
            f"{API_URL}?barcode=9002490250430&consumer=mobile&shop_number=7a7ea076-2913-11e4-93fd-2c44fd94a135",
            headers=HEADERS_TEMPLATE
        ) as response:
            py_logger.info(f"Test request, Barcode: {response.status}")
    except Exception as e:
        py_logger.exception(f"Unexpected error test request. Exception: {e}")


async def fetch_product_by_barcode(
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore,
    barcode: str,
    products: asyncio.Queue,
    statuses: asyncio.Queue,
    API_URL: str
):
    async with semaphore:
        status_failed_request = 0

        # Цикл нескольких попыток в случае неудачного запроса
        for _ in range(6):  
            try:
                async with session.get(
                    f"{API_URL}?barcode={barcode}&consumer=mobile&shop_number=7a7ea076-2913-11e4-93fd-2c44fd94a135",
                    headers=HEADERS_TEMPLATE
                ) as response:
                    py_logger.info(f"Barcode: {barcode}, Status: {response.status}")

                    # 200 - бар код найден, 400-410 - баркода не существует в Бристоле
                    if response.status == 200 or response.status in range(400, 411):
                        if response.status == 200:
                            await statuses.put(response.status)
                            response_json = await response.json()
                            promo_product = response_json.get('promo_product', [])
                            name = promo_product['name']
                            id = promo_product['id']
                            await products.put(Product(barcode, id, name))

                        # Для проверки отправляем существующий баркод (1 запрос из 300)
                        if int(int(barcode) / 10) % 300 == 0:
                            await send_test_barcode(session, API_URL)
                                
                        break # Выходи из цикла нескольких попыток

                    elif response.status in range(500, 511):    
                        status_failed_request = response.status
                    else:
                        await statuses.put(RequestStatus(barcode, str(response.status)))
                        break # Выходи из цикла нескольких попыток

            except asyncio.TimeoutError:
                py_logger.info(f"Timeout error fetching. Barcode: {barcode}")
                status_failed_request = "Timeout error"

            except Exception as e:
                py_logger.exception(f"Unexpected error fetching. Barcode: {barcode}, Exception: {e}")
                await statuses.put(RequestStatus(barcode, str(e)))
                break # Выходи из цикла нескольких попыток

            #Задрежка при 5xx или TimeoutError
            py_logger.info(f"Retrying in 5 sec...")
            await asyncio.sleep(5)

        else:
            py_logger.info(f"Barcode: {barcode}, Status: {status_failed_request}")
            await statuses.put(RequestStatus(barcode, str(status_failed_request)))