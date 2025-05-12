#! /usr/bin/env python3

import os
import re


class Path(str):
    """A standardized class for handling file paths"""

    def __init__(self):
        pass

    def __new__(cls, path):
        # expand environment variables
        path1 = cls._expand_env_var(path)
        path2 = cls._format_path(path1)
        return path2
    
    def _expand_env_var(path):
        """Expands environment variables by regex substitution"""
        # identify all environment variables in the path
        envs = re.findall(r"\$[^/]+", path)
        # replace the environment variables with their values
        for env in envs:
            path = path.replace(env, os.environ[env.replace("$", "")])
        return path.replace("//", "/")

    def _format_path(path):
        """Convert all path types to absolute path with explicit directory ending"""
        if path:
            # expand username
            path = os.path.expanduser(path)
            # only save the directory ending if it is a directory
            if path.endswith("/"):
                if not os.path.isdir(path):
                    path = path[:-1]
            # add the directory ending if it is a directory
            else:
                if os.path.isdir(path):
                    path += "/"
            # make the path absolute
            if not path.startswith("/"):
                path = os.getcwd() + "/" + path
            # replace redundancies
            path = path.replace("/./", "/")
            # trace back to the root directory
            while "/../" in path:
                if path == "/../":
                    raise FileNotFoundError("Path does not exist")
                path = re.sub(r"[^/]+/\.\./(.*)", r"\1", path)
        return path
