from psycopg2.extras import execute_values

from src.db.connection import db_connect
from src.utils.logger import get_logger

logger = get_logger(__name__)


def insert_coins(coins, conn=None):
    if not coins:
        logger.warning("No coins data to insert.")
        return

    conn = conn or db_connect()
    should_close = False

    if conn is None:
        conn = db_connect()
        should_close = True

    logger.info("Inserting coins data into staging.coin_cap table...")

    try:
        with conn.cursor() as cur:
            values = [
                (
                    c["id"],
                    c["rank"],
                    c["symbol"],
                    c["name"],
                    c["price_usd"],
                )
                for c in coins
            ]

            execute_values(
                cur,
                """
                INSERT INTO staging.coin_cap (id, rank, symbol, name, price_usd)
                VALUES %s
                ON CONFLICT (id) DO UPDATE SET
                    rank = EXCLUDED.rank,
                    symbol = EXCLUDED.symbol,
                    name = EXCLUDED.name,
                    price_usd = EXCLUDED.price_usd,
                    ingested_at = NOW()
                """,
                values,
            )
        conn.commit()
        logger.info(f"Inserted {len(coins)} coins into staging.coin_cap table.")
    except Exception:
        conn.rollback()
        raise
    finally:
        if should_close:
            conn.close()
