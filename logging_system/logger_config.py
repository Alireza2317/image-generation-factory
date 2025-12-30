import sys
import loguru
from settings import settings


def setup_logger() -> loguru.Logger:
	# Create a "log" directory if it doesn't exist
	log_path = settings.log_path
	log_path.mkdir(parents=True, exist_ok=True)

	# Remove the default handler to prevent duplicate logs
	loguru.logger.remove()

	# Console logger for interactive use
	loguru.logger.add(
		sys.stderr,
		level="INFO",
		format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
		colorize=True,
	)

	# File logger for storing logs
	loguru.logger.add(
		log_path / "app.log",
		level="DEBUG",
		format="{time} {level} {message}",
		rotation="10 MB",
		retention="10 days",
		catch=True,
		enqueue=True,  # Make logging asynchronous
		backtrace=True,
		diagnose=True,
	)
	return loguru.logger


app_logger = setup_logger()
