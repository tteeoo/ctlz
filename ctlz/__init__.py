## init module that contains everything
#
#  Contains all classes and submodules

import os
import json
import configparser
import ctlz.text
import ctlz.exceptions

"""
TODO:
    - Add more config types
"""

## Class for easy management of configuration files
#
#  Currently only deserializes from a list of paths
class Config:

    def __validate_format(self, fmt):
        if fmt not in ["json", "ini"]:
            raise exceptions.InvalidConfigFormat("Invalid config file format, valid formats include 'json' and 'ini'")
        else: self.fmt = fmt

    ## The constructor method
    #
    #  Initializes properties from parameters
    def __init__(self, paths, fmt, default=None):
        self.paths = paths
        self.location = None
        self.default = default
        self.data = default
        self.__validate_format(fmt)

    ## Reads config file at the first valid path in self.paths and return it deserialized
    #
    #  Currently only supports json and ini-style config files
    def deserialize(self):
        good_paths = []
        for path in self.paths:
            if os.path.isfile(path):
                good_paths.append(path)
        if len(good_paths) < 1:
            if self.default != None:
                raise exceptions.NoConfigFileFound("No file found or default provided")
            else:
                return self.default
        else:
            self.location = good_paths[0]

        # json
        if self.fmt == "json":
            if self.default != None:
                try:
                    with open(self.location) as f:
                        self.data = json.load(f.read())
                    return self.data
                except:
                    return self.default
            else:
                with open(self.location) as f:
                    self.data = json.load(f.read())
                return self.data

        # ini
        elif self.fmt == "ini":
            if self.default != None:
                try:
                    self.data = configparser.ConfigParser()
                    self.data.read(self.location)
                    return self.data
                except:
                    return self.default
            else:
                self.data = configparser.ConfigParser()
                self.data.read(self.location)
                return self.data

    ## Writes config to the first valid path in self.paths
    #
    #  Currently only supports json and ini-style config files
    def serialize_safe(self):
        good_paths = []
        for path in self.paths:
            if os.path.isfile(path):
                good_paths.append(path)
        if len(good_paths) < 1:
            raise exceptions.NoConfigFileFound("No file found to write to")
        else:
            self.location = good_paths[0]

        # json
        if self.fmt == "json":
            with open(self.location, "w") as f:
                json.dump(self.data, f.write())

        # ini
        elif self.fmt == "ini":
            with open(self.location, "w") as f:
                self.data.write(f)

    ## Writes config to the specified path
    #
    #  Currently only supports json and ini-style config files
    def serialize(self, path):

        # json
        if self.fmt == "json":
            with open(path, "w") as f:
                json.dump(self.data, f.write())

        # ini
        elif self.fmt == "ini":
            with open(path, "w") as f:
                self.data.write(f)


class Modes:
    pass
