import asyncpg
from utils import write_file
from config import py_logger, DB_CONFIG


def handle_exception(products, message):
    py_logger.exception(f"{message}")
    write_file(products, "products")


async def insert_products(products: list):
    conn = None

    try:
        conn = await asyncpg.connect(**DB_CONFIG)
        data = [(int(p.barcode), int(p.id) , p.name) for p in products]
        sql = """
        INSERT INTO product (barcode, id, name) 
        VALUES ($1, $2, $3)
        ON CONFLICT (barcode) DO UPDATE 
        SET 
            id = EXCLUDED.id,
            name = EXCLUDED.name;
        """

        async with conn.transaction():
            await conn.executemany(sql, data)
            py_logger.info(f"Inserting into the database {len(data)} product")

    except asyncpg.exceptions.InterfaceError as e:
        handle_exception(products, f"Error connecting to database: {e}")
    except asyncpg.exceptions.PostgresError as e:
        handle_exception(products, f"Error executing SQL query: {e}")
    except Exception as e:
        handle_exception(products, f"Unexpected error: {e}")
    finally:
        if conn:
            await conn.close()


async def fetch_ids_by_table(table_name: str) -> list:
    conn = None
    rows = []

    try:
        conn = await asyncpg.connect(**DB_CONFIG)

        query = f"SELECT id FROM {table_name}"
        rows = await conn.fetch(query)

    except asyncpg.exceptions.InterfaceError as e:
        py_logger.exception(f"Error connecting to database: {e}")
    except asyncpg.exceptions.PostgresError as e:
        py_logger.exception(f"Error executing SQL query: {e}")
    except Exception as e:
        py_logger.exception(f"Unexpected error: {e}")
    finally:
        if conn:
            await conn.close()

    return [row[0] for row in rows]