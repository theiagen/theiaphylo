#! /usr/bin/env python3

import os
import re

class Path(str):
    """A standardized class for handling file paths"""
    def __init__(self, path):
        self.path = path
        self.format_path()

    def expand_env_var(self):
        """Expands environment variables by regex substitution"""
        # identify all environment variables in the self.path
        envs = re.findall(r'\$[^/]+', self.path)
        # replace the environment variables with their values
        for env in envs:
            self.path = self.path.replace(env, os.environ[env.replace('$','')])
        self.path.replace('//','/')
    
    def format_path(self):
        """Convert all self.path types to absolute self.path with explicit directory ending"""
        if self.path:
            # expand username
            self.path = os.path.expanduser(self.path)
            # expand environment variables
            self.expand_env_var()
            # only save the directory ending if it is a directory
            if self.path.endswith('/'):
                if not os.self.path.isdir(self.path):
                    self.path = self.path[:-1]
            # add the directory ending if it is a directory
            else:
                if os.path.isdir(self.path):
                    self.path += '/'
            # make the self.path absolute
            if not self.path.startswith('/'):
                self.path = os.getcwd() + '/' + self.path
            # replace redundancies
            self.path = self.path.replace('/./', '/')
            # trace back to the root directory
            while '/../' in self.path:
                self.path = re.sub(r'[^/]+/\.\./(.*)', r'\1', self.path)
        return self.path
    
 