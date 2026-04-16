from src.utils.logger import get_logger

logger = get_logger(__name__)


def transform_coins(coins):
    transformed = []
    failed = []

    logger.info(f"Transforming {len(coins)} coins")
    for c in coins:
        try:
            transformed.append({
                "id": c["id"],
                "rank": int(c["rank"]),
                "symbol": c["symbol"],
                "name": c["name"],
                "priceUsd": float(c["priceUsd"]),
            })
        except (KeyError, ValueError, TypeError) as e:
            logger.warning(f"Failed to transform coin {c.get('id')}: {e}")
            failed.append(c.get("id", "unknown"))

    logger.info(f"Transformed {len(transformed)} coins")

    if failed:
        logger.warning(f"Failed to transform {len(failed)} coins: {failed}")

    return transformed
