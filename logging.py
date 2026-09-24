import logging


def setup():
    """Set up logging for the storyboard_editing module."""
    root = logging.root
    root.setLevel(logging.INFO)

    for handler in root.handlers:
        handler.addFilter(
            lambda record: (
                "storyboard_editing" in record.name
            )
        )
