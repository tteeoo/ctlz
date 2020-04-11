class NoConfigFileFound(Exception):
    """Raised when no configuration file is found"""

class InvalidColor(Exception):
    """Raised when an invalid color is provided in text.color()"""

class InvalidConfigFormat(Exception):
    """Raised when an invalid config format is provided in Config.deserialize()"""

class NoDocString(Exception):
    """Raised when auto_help is true, but a mode doesn't have a docstring"""