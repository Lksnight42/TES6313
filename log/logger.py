import logging
from pathlib import Path
LEVELS = ["TRACE", "DEBUG", "INFO", "WARN", "ERROR"]


LOG_DIR = Path("log")
LOG_DIR.mkdir(exist_ok=True)


TRACE = 5
logging.addLevelName(TRACE, "TRACE")

logger = logging.getLogger("logger")


class SourceFilter(logging.Filter):
    def __init__(self, allowed_sources):
        super().__init__()
        self.allowed_sources = set(allowed_sources)

    def filter(self, record):
        return getattr(record, "source", None) in self.allowed_sources


def trace(self, message, *args, **kwargs):
    if self.isEnabledFor(TRACE):
        self._log(TRACE, message, args, **kwargs)


logging.Logger.trace = trace


def setup_logging():
    logger.setLevel(logging.DEBUG)
    logger.setLevel(TRACE)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "[%(levelname)s] %(asctime)s %(message)s"
    )

    # global logger
    system_handler = logging.FileHandler(LOG_DIR / "system.log")
    system_handler.setLevel(logging.DEBUG)
    system_handler.setFormatter(formatter)

    # initialize logger
    init_handler = logging.FileHandler(LOG_DIR / "initialize.log")
    init_handler.setLevel(TRACE)
    init_handler.setFormatter(formatter)
    init_handler.addFilter(SourceFilter({
        "loader", "init", "station-service", "transfer", "metric"
    }))

    # route logger
    route_handler = logging.FileHandler(LOG_DIR / "route.log")
    route_handler.setLevel(logging.INFO)
    route_handler.setFormatter(formatter)
    # route_handler.addFilter(SourceFilter({
    #     "route", "rule", "evaluation", "Best"
    # }))

    logger.addHandler(system_handler)
    logger.addHandler(init_handler)
    logger.addHandler(route_handler)

    return logger


def dump_logs(env, min_level="DEBUG"):
    min_idx = LEVELS.index(min_level)

    for fact in env.facts():
        if fact.template.name != "delog":
            continue

        # if fact.template.name == "delog":
        level = fact["level"]
        message = fact["message"]
        ref_id = fact["ref-id"]
        source = fact["source"]

        if LEVELS.index(level) >= min_idx:
            print(f"[{level}]({source}) {message} :: {ref_id}")

        extra = {"source": source}

        if level == "TRACE":
            logger.trace(f"{message} :: {ref_id}", extra=extra)
        elif level == "INFO":
            logger.info(f"{message} :: {ref_id}", extra=extra)
        elif level == "DEBUG":
            logger.debug(f"{message} :: {ref_id}", extra=extra)
        elif level == "ERROR":
            logger.error(f"{message} :: {ref_id}", extra=extra)
        elif level == "WARN":
            logger.warning(f"{message} :: {ref_id}", extra=extra)
