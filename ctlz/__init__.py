import os
import re
import sys
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

class Control:
    """Class for managing and executing decorated functions"""

    def __init__(self, name, prompt=None, command=sys.argv[1:]):
        """The constructor method"""

        self.commands = {}
        self.name = name
        self.auto_console = True

        if prompt != None: self.prompt = prompt
        else: self.prompt = name + "> "
        
        self.command = command
        if command != []:
            self.mode = self.command[0]
            self.params = self.command[1:]

    def define(self, mode, params=[]):
        """Adds decorated func to self.modes"""

        def wrapper(func):
            if mode == None: self.auto_console = False
            self.commands[mode] = {"func": func, "params": params}
            return func

        return wrapper

    def run(self):
        """Starts execution"""

        if len(self.command) > 0:
            for mode in list(self.commands.keys()):
                if mode == self.mode:
                    if len(self.commands[mode]["params"]) != len(self.params):
                        word = "was"
                        if len(self.params) > 1: word = "were"
                        print(self.name + ": invalid amount of params; " + self.mode + " takes " + str(len(self.commands[mode]["params"])) + " but " + str(len(self.params)) + " " + word + " provided")
                        exit(1)
                    for param in zip(self.commands[mode]["params"], self.params):
                        if re.match(param[0], param[1]) == None:
                            print(self.name + ": invalid param " + param[1] + " for " + self.mode)
                            exit(1)
                    self.commands[mode]["func"]()
                    exit(0)
            print(self.name + ": unknown command: " + self.mode)
            exit(1)
        else:
            if self.auto_console:
                try:
                    self.make_prompt()
                except (EOFError, KeyboardInterrupt):
                    exit(0)
            else:
                self.commands[None]["func"]()

    def make_prompt(self):

        self.command = input(self.prompt).split()
        self.mode = self.command[0]
        self.params = self.command[1:]

        for mode in list(self.commands.keys()):
            if mode == self.mode:
                if len(self.commands[mode]["params"]) != len(self.params):
                    word = "was"
                    if len(self.params) > 1: word = "were"
                    print(self.name + ": invalid amount of params; " + self.mode + " takes " + str(len(self.commands[mode]["params"])) + " but " + str(len(self.params)) + " " + word + " provided")
                    self.make_prompt()
                for param in zip(self.commands[mode]["params"], self.params):
                    if re.match(param[0], param[1]) == None:
                        print(self.name + ": invalid param " + param[1] + " for " + self.mode)
                        self.make_prompt()
                self.commands[mode]["func"]()
                self.make_prompt()
        print(self.name + ": unknown command " + self.mode)
        self.make_prompt()