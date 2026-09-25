import logging

levels = {
    "CRITICAL": 50,
    "ERROR": 40,
    "WARNING": 30,
    "INFO": 20,
    "DEBUG": 10,
    "NOTSET": 0,
}


def setup(level: str = "INFO"):
    """Set up logging for the dagda-blender-storyboard module."""
    root = logging.root
    root.setLevel(levels.get(level, levels["INFO"]))

    for handler in root.handlers:
        handler.addFilter(
            lambda record: (
                "dagda-blender-storyboard" in record.name.lower()
            )
        )
