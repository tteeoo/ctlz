import os
import json
import ctlz.colors
import ctlz.exceptions

## Class for easy managment of configuration files
class Config:
    def __init__(self, paths, fmt, default=None):
        self.paths = paths
        self.fmt = fmt
        self.default = default
        self.data = default

    ## Reads the the first valid path in self.paths
    #
    # Currently only supports json configuration files
    def read(self):
        # check paths
        good_paths = []
        for path in self.paths:
            if os.path.isfile(path):
                good_paths.append(path)
        if len(good_paths) < 1:
            if self.default != None:
                return self.default
            else:
                raise exceptions.NoConfigFileFound("No file found or default provided")

        # read file
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
