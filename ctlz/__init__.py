import os
import json

class Config:
    def __init__(self, paths, fmt, default=None):
        self.paths = paths
        self.fmt = fmt
        self.default = default

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
                raise AssertionError("ctlz: no valid config files found, and no default config was provided")

        # read file
        if self.fmt == "json":
            if self.default != None:
                try:
                    with open(good_paths[0]) as f:
                        return json.load(f.read())
                except:
                    return self.default
            else:
                with open(good_paths[0]) as f:
                    return json.load(f.read())