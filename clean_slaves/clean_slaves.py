#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright Saab AB, 2012 (http://www.safirsdk.com)
#
# Created by: Lars Hagstrom (lars@foldspace.nu)
#
###############################################################################
#
# This file is part of Safir SDK Core.
#
# Safir SDK Core is free software: you can redistribute it and/or modify
# it under the terms of version 3 of the GNU General Public License as
# published by the Free Software Foundation.
#
# Safir SDK Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Safir SDK Core.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from __future__ import print_function
import os, sys, shutil, stat

def onerror(function, path, excinfo):
    try:
        # path contains the path of the file that couldn't be removed
        # let's just assume that it's read-only and unlink it.
        os.chmod( path, stat.S_IWRITE )
        os.unlink( path )
        return
    except:
        pass

    #hmm, maybe the path is very long and we're on windows
    if sys.platform == "win32":
        newpath = os.path.join("\\\\?\\",os.getcwd(),os.path.normpath(path))
        print("Will try to delete",newpath)

    print("Failed to delete",path, ":", excinfo)

BASE = os.environ.get("BASE")
if BASE is None:
    print("Failed to find Jenkins base directory, trying $HOME/jenkins")
    HOME = os.environ.get("HOME")
    if HOME is None:
        print("HOME environment variable is not set")
        sys.exit(1)
    BASE=os.path.join(HOME,"jenkins")

if not os.path.isdir(BASE):
    print(BASE, "does not appear to be a directory")
    sys.exit(1)
print("Changing directory to", BASE)
os.chdir(BASE)
contents = os.listdir(".")
print (contents)
if not os.path.isdir("workspace"):
    print("Could not find 'workspace' dir in", BASE)
    sys.exit(1)

print("Deleting directory 'workspace' in", BASE)
shutil.rmtree("workspace",onerror=onerror)
#for root, dirs, files in os.walk("workspace", topdown=False):
#    for name in files:
#        filename = os.path.join(root, name)
#        os.chmod(filename, stat.S_IWRITE)
#        os.remove(filename)
#    for name in dirs:
#b        os.rmdir(os.path.join(root, name))
print("Completed")
sys.exit(0)
