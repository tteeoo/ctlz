import os
import json
import configparser

import ctlz.text
import ctlz.exceptions

class Config:
    """Class for easy managment of config files"""

    def __validate_format(self, fmt):
        if fmt not in ["json", "ini"]:
            raise ctlz.exceptions.InvalidConfigFormat("Invalid config file format, valid formats include 'json' and 'ini'")
        else: self.fmt = fmt

    def __init__(self, paths, fmt, default=None):
        """The constuctor method"""

        self.paths = paths
        self.location = None
        self.default = default
        self.data = default
        self.__validate_format(fmt)

    def deserialize(self):
        """Reads config file at the first valid path in self.paths and return it deserialized"""

        good_paths = []
        for path in self.paths:
            if os.path.isfile(path):
                good_paths.append(path)
        if len(good_paths) < 1:
            if self.default == None:
                raise ctlz.exceptions.NoConfigFileFound("No file found or default provided")
            else:
                return self.default
        else:
            self.location = good_paths[0]

        # json
        if self.fmt == "json":
            if self.default == None:
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
            if self.default == None:
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

    def serialize_safe(self):
        """Writes config to the first valid path in self.paths"""

        good_paths = []
        for path in self.paths:
            if os.path.isfile(path):
                good_paths.append(path)
        if len(good_paths) < 1:
            raise ctlz.exceptions.NoConfigFileFound("No file found to write to")
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

    def serialize(self, path):
        """Writes config to the specified path"""

        # json
        if self.fmt == "json":
            with open(path, "w") as f:
                json.dump(self.data, f.write())

        # ini
        elif self.fmt == "ini":
            with open(path, "w") as f:
                self.data.write(f)