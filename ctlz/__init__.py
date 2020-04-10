## init module that contains everything
#
#  Contains all classes and submodules

import os
import json
import configparser
import ctlz.text
import ctlz.exceptions

## Class for easy management of configuration files
#
#  Currently only deserializes from a list of paths
class Config:

    ## The constructor method
    #
    #  Initializes properties from parameters
    def __init__(self, paths, fmt, default=None):
        self.paths = paths
        self.fmt = fmt
        self.default = default
        self.data = default
        self.read_location = None

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
                return self.default
            else:
                raise exceptions.NoConfigFileFound("No file found or default provided")
        else:
            self.read_location = good_paths[0]

        # json
        if self.fmt == "json":
            if self.default != None:
                try:
                    with open(self.read_location) as f:
                        self.data = json.load(f.read())
                    return self.data
                except:
                    return self.default
            else:
                with open(self.read_location) as f:
                    self.data = json.load(f.read())
                return self.data

        # ini
        elif self.fmt == "ini":
            if self.default != None:
                try:
                    self.data = configparser.ConfigParser()
                    self.data.read(self.read_location)
                    return self.data
                except:
                    return self.default
            else:
                self.data = configparser.ConfigParser()
                self.data.read(self.read_location)
                return self.data

        else:
            raise exceptions.InvalidConfigFormat("Invalid config file format, valid formats include 'json' and 'ini'")

        #TODO: add more config formats

class Modes:
    pass
