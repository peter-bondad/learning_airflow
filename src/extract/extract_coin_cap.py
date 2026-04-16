import requests
import os
from src.utils.logger import get_logger

logger = get_logger(__name__)


def fetch_coins(limit: int = 10):
    COIN_CAP_API_KEY = os.getenv("COINCAP_API_KEY")

    COIN_CAP_FIELDS = ["id", "rank", "symbol", "name", "priceUsd"]

    # Validate COIN_CAP_API_KEY
    if not COIN_CAP_API_KEY:
        raise ValueError("COINCAP_API_KEY is not set")

    url = f"https://rest.coincap.io/v3/assets?limit={limit}"

    res = requests.get(
        url,
        headers={"Authorization": f"Bearer {COIN_CAP_API_KEY}"},
        timeout=10,
    )
    res.raise_for_status()

    raw_coin_data = res.json().get("data", [])

    coins = []
    for coin in raw_coin_data:
        missing = [f for f in COIN_CAP_FIELDS if not f in coin]
        if missing:
            logger.warning(
                f"Coin {coin.get('id', 'unknown')} is missing fields: {missing}"
            )
            continue
        coins.append(coin)

    logger.info(f"Fetched {len(coins)} coins")

    return coins
