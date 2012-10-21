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
import os, sys, shutil

def onerror(function, path, excinfo):
    print("Failed to delete",path, ":", excinfo)

BASE = os.environ.get("BASE")
if BASE is None:
    print("Failed to find Jenkins base directory, exiting")
    sys.exit(1)
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
shutil.rmtree("workspace",onerror)
print("Completed")
sys.exit(0)
