import logging

def setup_logging(logging_evel):
    logging.basicConfig(
        level=logging_evel,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)
