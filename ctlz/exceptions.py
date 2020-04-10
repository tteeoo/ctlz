## Contains basic classes to be used for exceptions
#
#  Exists just to provide nice, more specific exception names

## Raised when no configuration file is found
#
#  Only raised if there is no default provided to the Config class
class NoConfigFileFound(Exception):
    pass

## Raised when an invalid color is provided in text.color()
class InvalidColor(Exception):
    pass

## Raised when an invalid config format is provided in Config.deserialize()
class InvalidConfigFormat(Exception):
    pass