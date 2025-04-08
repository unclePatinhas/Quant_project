import logging

def setup_logger(log_file: str = "app.log") -> logging.Logger:
    # Create a custom logger
    logger = logging.getLogger("tweet_logger")
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers
    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # File handler for errors
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.ERROR)

        # Formatter
        formatter = logging.Formatter("@%(asctime)s %(levelname)s %(message)s")

        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Add handlers
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


# def setup_logger():
#     logging.basicConfig(
#         level=logging.INFO,
#         format="@(asctime)s %(levelname)s %(message)s"
#     )
