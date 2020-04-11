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

    def __init__(self, name, global_flags=[], prompt=None, auto_help=False, help_header=None, extra_help=None, command=sys.argv[1:]):
        """The constructor method"""

        self.commands = {}
        self.global_flags = global_flags
        self.flags = []
        self.name = name
        self.help_header = help_header
        self.extra_help = extra_help
        self.auto_console = True
        self.auto_help = auto_help

        if prompt != None: self.prompt = prompt
        else: self.prompt = name + "> "
        
        self.command = command
        if command != []:
            self.mode = self.command[0]
            self.params = self.command[1:]

    def define(self, mode, params=[], flags=[]):
        """Adds decorated func to self.modes"""

        def wrapper(func):
            if mode == None: self.auto_console = False
            self.commands[mode] = {"func": func, "params": params, "flags": flags + self.global_flags}
            return func

        return wrapper

    def run(self):
        """Starts execution"""

        if self.auto_help:
            @self.define("-h")
            @self.define("--help")
            def help_message():
                """Prints this help message"""

                info = {}
                for mode in list(self.commands.keys()):
                    info[mode] = {"doc": self.commands[mode]["func"].__doc__, "alias": []}

                known = []
                for mode in list(info.keys()):
                    found = False
                    for pair in known:
                        if info[mode]["doc"] == pair[1]:
                            info[pair[0]]["alias"].append(mode)
                            del info[mode]
                            found = True
                            break
                    if not found:
                        if [mode, info[mode]["doc"]] not in known: known.append([mode, info[mode]["doc"]])
                if self.help_header != None: print(self.help_header)
                print("USAGE: ")
                print("\t" + self.name + " [MODE [FLAGS] <PARAMS>]\n")
                print("MODES: ")
                for mode in list(info.keys()):
                    if info[mode]["doc"] == None:
                        raise ctlz.exceptions.NoDocString("mode " + mode + " does not have a docstring to create help message from")
                    info[mode]["alias"].append(mode)

                    list_params = ", takes no params"
                    if len(self.commands[mode]["params"]) == 1:
                        list_params = ", takes param: " + self.commands[mode]["params"][0]
                    if len(self.commands[mode]["params"]) > 1:
                        list_params = ", takes params: " + " ".join(self.commands[mode]["params"])
                    print("\t" + ", ".join(info[mode]["alias"]) + ": " + info[mode]["doc"] + list_params + "\n")
                if self.auto_console: print("Run without any arguments to enter console mode.")
                if self.extra_help != None: print(self.extra_help)

        if len(self.command) > 0:
            for mode in list(self.commands.keys()):
                if mode == self.mode:
                    flags_to_del = []
                    for i in range(len(self.params)):
                        if self.params[i] in self.commands[mode]["flags"]:
                            self.flags.append(self.params[i])
                            flags_to_del.append(i)
                    for i in flags_to_del:
                        del self.params[i]
                    if len(self.commands[mode]["params"]) != len(self.params):
                        word = "was"
                        if len(self.params) != 1: word = "were"
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
        """Makes program enter console mode"""

        self.command = input(self.prompt).split()
        self.mode = self.command[0]
        self.params = self.command[1:]
        self.flags = []

        for mode in list(self.commands.keys()):
            if mode == self.mode:
                flags_to_del = []
                for i in range(len(self.params)):
                    if self.params[i] in self.commands[mode]["flags"]:
                        self.flags.append(self.params[i])
                        flags_to_del.append(i)
                for i in flags_to_del:
                    del self.params[i]
                if len(self.commands[mode]["params"]) != len(self.params):
                    word = "was"
                    if len(self.params) != 1: word = "were"
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