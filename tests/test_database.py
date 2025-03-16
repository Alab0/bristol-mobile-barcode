import os
import sys

sys.path.append(f'{os.getcwd()}/bristol_mobile_barcode')

import pytest
import asyncpg
from unittest.mock import AsyncMock, MagicMock, patch
from database import fetch_ids_by_table, insert_products
from models import Product


@pytest.mark.asyncio
async def test_fetch_ids_by_table_success():
    mock_conn = AsyncMock()
    mock_conn.fetch.return_value = [[1], [2], [3]]
    
    with patch("asyncpg.connect", return_value=mock_conn):
        result = await fetch_ids_by_table("test_table")
    
    assert result == [1, 2, 3]
    mock_conn.fetch.assert_called_once_with("SELECT id FROM test_table")
    mock_conn.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_fetch_ids_by_table_connection_error():
    mock_conn = AsyncMock()
    mock_conn.fetch.side_effect = asyncpg.exceptions.InterfaceError("Connection failed")
    
    with patch("asyncpg.connect", return_value=mock_conn):
        result = await fetch_ids_by_table("test_table")
    
    assert result == []
    mock_conn.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_fetch_ids_by_table_query_error():
    mock_conn = AsyncMock()
    mock_conn.fetch.side_effect = asyncpg.exceptions.PostgresError("Query failed")
    
    with patch("asyncpg.connect", return_value=mock_conn):
        result = await fetch_ids_by_table("test_table")
    
    assert result == []
    mock_conn.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_insert_products_success():
    mock_conn = AsyncMock()
    
    mock_conn.transaction = MagicMock()
    mock_conn.transaction.return_value.__aenter__.return_value = mock_conn
    mock_conn.transaction.return_value.__aexit__.return_value = None

    mock_conn.executemany = AsyncMock()
    mock_conn.close = AsyncMock()

    products = [
        Product(
            barcode = "1234567891011", id = 11, name = "Product1"
        ),
        Product(
            barcode = "1234567891012", id = 12, name = "Product2"
        ),
    ]

    with patch("asyncpg.connect", return_value=mock_conn):
        await insert_products(products)

    # Проверяем, что executemany был вызван
    assert mock_conn.executemany.call_count > 0

    mock_conn.executemany.assert_any_call(
        """
        INSERT INTO product (barcode, id, name) 
        VALUES ($1, $2, $3)
        ON CONFLICT (barcode) DO UPDATE 
        SET 
            id = EXCLUDED.id,
            name = EXCLUDED.name;
        """,
        [(1234567891011, 11, "Product1"),
         (1234567891012, 12, "Product2")]
    )

    mock_conn.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_insert_products_connection_error():
    mock_conn = AsyncMock()
    
    mock_conn.transaction = MagicMock()
    mock_conn.transaction.return_value.__aenter__.return_value = mock_conn
    mock_conn.transaction.return_value.__aexit__.return_value = None

    mock_conn.executemany.side_effect = asyncpg.exceptions.InterfaceError("Connection failed")

    with patch("asyncpg.connect", return_value=mock_conn):
        await insert_products([])

    mock_conn.close.assert_awaited_once()
    

@pytest.mark.asyncio
async def test_insert_products_query_error():
    mock_conn = AsyncMock()
    
    mock_conn.transaction = MagicMock()
    mock_conn.transaction.return_value.__aenter__.return_value = mock_conn
    mock_conn.transaction.return_value.__aexit__.return_value = None

    mock_conn.executemany.side_effect = asyncpg.exceptions.PostgresError("Query failed")

    with patch("asyncpg.connect", return_value=mock_conn):
        await insert_products([])

    mock_conn.close.assert_awaited_once()