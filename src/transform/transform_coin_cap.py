from src.utils.logger import get_logger
from pydantic import BaseModel, Field, ValidationError

logger = get_logger(__name__)

class CoinCapSchema(BaseModel):
    id: str
    rank: int
    symbol: str
    name: str
    priceUsd: float = Field(alias="price_usd")

    model_config = {
        "extra": "ignore",
        "populate_by_name": True
    }

def transform_coins(coins):
    transformed = []
    failed = []

    logger.info(f"Transforming {len(coins)} coins")
    for c in coins:
        try:
            coin = CoinCapSchema.model_validate(c, strict=True)
            transformed.append(coin.model_dump())
        except ValidationError as e:
            logger.warning(f"Invalid coin {c.get('id', 'unknown')}: {e.errors()}")
            failed.append(c.get("id", "unknown"))

    logger.info(f"Transformed {len(transformed)} coins")

    if failed:
        logger.warning(f"Failed to transform {len(failed)} coins: {failed}")

    return transformed
