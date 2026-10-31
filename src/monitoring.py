
import logging
import uuid
import time
import tracemalloc
from datetime import datetime, timezone


def create_run_id():
    """Generate a unique pipeline run ID."""
    return str(uuid.uuid4())


def get_timestamp():
    """Return current UTC timestamp."""
    return datetime.now(timezone.utc).isoformat()


def setup_logging():
    """Configure pipeline logging."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    return logging.getLogger("data_pipeline")


def start_monitoring():
    """Start execution-time and memory monitoring."""

    tracemalloc.start()
    start_time = time.perf_counter()

    return start_time


def stop_monitoring(start_time):
    """Calculate execution time and peak memory usage."""

    execution_time = time.perf_counter() - start_time

    current_memory, peak_memory = tracemalloc.get_traced_memory()

    tracemalloc.stop()

    peak_memory_mb = peak_memory / (1024 * 1024)

    return {
        "execution_time_seconds": round(execution_time, 4),
        "peak_memory_mb": round(peak_memory_mb, 2)
    }
