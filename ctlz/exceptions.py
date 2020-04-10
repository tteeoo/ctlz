class NoConfigFileFound(Exception):
    """Raised when no configuration file is found"""

class InvalidColor(Exception):
    """Raised when an invalid color is provided in text.color()"""

class InvalidConfigFormat(Exception):
    """Raised when an invalid config format is provided in Config.deserialize()"""

class InvalidCommand(Exception):
    """Raised when an invalid command is ran and not invalid command message is provided"""