import logging
import threading

# ANSI escape sequences for colors
COLORS = {
    'DEBUG': '\033[90m',  # Gray
    'INFO': '\033[97m',  # White
    'WARNING': '\033[93m',  # Yellow
    'ERROR': '\033[91m',  # Red
    'CRITICAL': '\033[95m',  # Magenta
    'RESET': '\033[0m'  # Reset to default color
}


class ColoredFormatter(logging.Formatter):
    """Custom logging formatter to add colors to different log levels."""

    def format(self, record):
        # Apply color to log level names
        log_color = COLORS.get(record.levelname, COLORS['RESET'])
        message = super().format(record)
        return f"{log_color}{message}{COLORS['RESET']}"


def get_colored_logger():
    # Create a logger
    logger = logging.getLogger('acc')
    logger.setLevel(logging.DEBUG)

    # Create a console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Create a colored formatter
    formatter = ColoredFormatter('%(asctime)s %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(ch)

    # Ensure thread safety by adding a lock
    logger_lock = threading.Lock()

    # Use a lock around the logger's handlers
    def thread_safe_emit(self, record):
        with logger_lock:
            original_emit(self, record)

    # Store the original emit function
    original_emit = logging.StreamHandler.emit

    # Override the emit method with the thread-safe version
    logging.StreamHandler.emit = thread_safe_emit

    return logger


# Example usage
if __name__ == "__main__":
    logger = get_colored_logger()
    logger.debug("This is a DEBUG message")
    logger.info("This is an INFO message")
    logger.warning("This is a WARNING message")
    logger.error("This is an ERROR message")
    logger.critical("This is a CRITICAL message")
