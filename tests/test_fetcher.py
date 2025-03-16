import os
import sys

sys.path.append(f'{os.getcwd()}/bristol_mobile_barcode')

import asyncio
import pytest
import aiohttp
from aioresponses import aioresponses
from fetcher import fetch_product_by_barcode
from models import RequestStatus

API_URL = "https://api.mobile.bristol.ru/api/v2/regular/catalog/products/search_by_barcode"
BARCODE = "1234567890123"


@pytest.mark.asyncio
async def test_fetch_product_success():
    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(1)
        products = asyncio.Queue()
        statuses = asyncio.Queue()

        response_data = {
            "promo_product": {"name": "Test Product", "id": "123"}
        }

        with aioresponses() as mock_response:
            mock_response.get(
                f"{API_URL}?barcode={BARCODE}&consumer=mobile&shop_number=7a7ea076-2913-11e4-93fd-2c44fd94a135",
                payload=response_data,
                status=200
            )

            await fetch_product_by_barcode(session, semaphore, BARCODE, products, statuses, API_URL)

            product = await products.get()
            request_status = await statuses.get()

            assert product.barcode == BARCODE
            assert product.id == "123"
            assert product.name == "Test Product"
            assert request_status == 200


@pytest.mark.asyncio
async def test_fetch_product_client_error():
    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(1)
        products = asyncio.Queue()
        statuses = asyncio.Queue()

        with aioresponses() as mock_response:
            mock_response.get(
                f"{API_URL}?barcode={BARCODE}&consumer=mobile&shop_number=7a7ea076-2913-11e4-93fd-2c44fd94a135",
                status=404
            )

            await fetch_product_by_barcode(session, semaphore, BARCODE, products, statuses, API_URL)
            assert products.empty() 
            

@pytest.mark.asyncio
async def test_fetch_product_server_error():
    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(1)
        products = asyncio.Queue()
        statuses = asyncio.Queue()

        with aioresponses() as mock_response:
            for i in range(6):
                mock_response.get(
                    f"{API_URL}?barcode={BARCODE}&consumer=mobile&shop_number=7a7ea076-2913-11e4-93fd-2c44fd94a135",
                    status=503
                )

            await fetch_product_by_barcode(session, semaphore, BARCODE, products, statuses, API_URL)

            request_status = await statuses.get()
            assert isinstance(request_status, RequestStatus)
            assert request_status.barcode == BARCODE
            assert request_status.status == "503"


@pytest.mark.asyncio
async def test_fetch_product_timeout():
    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(1)
        products = asyncio.Queue()
        statuses = asyncio.Queue()

        with aioresponses() as mock_response:
            for i in range(6):
                mock_response.get(
                    f"{API_URL}?barcode={BARCODE}&consumer=mobile&shop_number=7a7ea076-2913-11e4-93fd-2c44fd94a135",
                    exception=asyncio.TimeoutError
                )

            await fetch_product_by_barcode(session, semaphore, BARCODE, products, statuses, API_URL)

            status = await statuses.get()
            assert isinstance(status, RequestStatus)
            assert status.barcode == BARCODE
            assert status.status == "Timeout error"


@pytest.mark.asyncio
async def test_fetch_product_exception():
    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(1)
        products = asyncio.Queue()
        statuses = asyncio.Queue()

        with aioresponses() as mock_response:
            mock_response.get(
                f"{API_URL}?barcode={BARCODE}&consumer=mobile&shop_number=7a7ea076-2913-11e4-93fd-2c44fd94a135",
                exception=Exception("Unexpected Error")
            )

            await fetch_product_by_barcode(session, semaphore, BARCODE, products, statuses, API_URL)

            status = await statuses.get()
            assert isinstance(status, RequestStatus)
            assert status.barcode == BARCODE
            assert status.status == "Unexpected Error"