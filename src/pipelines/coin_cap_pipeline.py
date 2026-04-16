from src.extract.extract_coin_cap import fetch_coins
from src.transform.transform_coin_cap import transform_coins
from src.load.load_coin_cap import insert_coins
from src.utils.logger import get_logger

logger = get_logger(__name__)


def run_pipeline(limit: int = 10):
    """
    Run the full ETL pipeline.
    
    Args:
        limit: Number of coins to fetch from API
    """
    logger.info(f"Starting pipeline with limit={limit}")

    try:
        # Extract
        coins = fetch_coins(limit=limit)
        
        # Transform
        coins = transform_coins(coins)
        
        # Load
        insert_coins(coins)
        
        logger.info("Pipeline completed successfully")
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise