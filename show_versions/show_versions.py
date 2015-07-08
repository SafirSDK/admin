#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright Saab AB, 2015 (http://safir.sourceforge.net)
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
import sys, subprocess, re

def log(*args, **kwargs):
    print(*args, **kwargs)
    sys.stdout.flush()

def python(f):
    f.write("Python: {0}.{1}.{2}\n".format(*sys.version_info))

def cmake(f):
    try:
        output = subprocess.check_output(("cmake","--version")).decode("utf-8")
        f.write("CMake: " + re.search(r"cmake version (.*)",output).group(1).strip() + "\n")
    except:
        f.write("CMake: N/A\n")

def subversion(f):
    try:
        output = subprocess.check_output(("svn","--version")).decode("utf-8")
        f.write("Subversion: " + re.search(r"svn, version ([\.0-9]*)",output).group(1).strip() + "\n")
    except:
        f.write("Subversion: N/A\n")

def ninja(f):
    try:
        output = subprocess.check_output(("ninja","--version")).decode("utf-8").strip()
        f.write("Ninja: " + output + "\n")
    except:
        f.write("Ninja: N/A\n")


def java(f):
    try:
        output = subprocess.check_output(("java","-version"),stderr=subprocess.STDOUT).decode("utf-8")
        f.write("Java: " + re.search(r"java version \"(.*)\"",output).group(1).strip() + "\n")
    except:
        f.write("Java: N/A\n")



def gcc(f):
    try:
        output = subprocess.check_output(("gcc","-dumpversion"),stderr=subprocess.STDOUT).decode("utf-8")
        f.write("GCC: " + output.strip() + "\n")
    except:
        f.write("GCC: N/A\n")



with open("versions.txt","w") as f:
    python(f)
    cmake(f)
    subversion(f)
    ninja(f)
    java(f)
    gcc(f)

#studio incl sp
#mono
#boost
#qt
