## init module that contains everything
#
#  Contains all classes and submodules

import os
import json
import ctlz.text
import ctlz.exceptions

## Class for easy management of configuration files
#
#  Currently only reads from a list of paths
class Config:

    ## The constructor method
    #
    #  Initializes properties from parameters
    def __init__(self, paths, fmt, default=None):
        self.paths = paths
        self.fmt = fmt
        self.default = default
        self.data = default

    ## Reads config file at the first valid path in self.paths
    #
    #  Currently only supports json config files
    def read(self):
        good_paths = []
        for path in self.paths:
            if os.path.isfile(path):
                good_paths.append(path)
        if len(good_paths) < 1:
            if self.default != None:
                return self.default
            else:
                raise exceptions.NoConfigFileFound("No file found or default provided")

        # json
        if self.fmt == "json":
            if self.default != None:
                try:
                    with open(good_paths[0]) as f:
                        self.data = json.load(f.read())
                        return self.data
                except:
                    return self.default
            else:
                with open(good_paths[0]) as f:
                    self.data = json.load(f.read())
                    return self.data

        #TODO: add more config formats

class Modes:
    pass
