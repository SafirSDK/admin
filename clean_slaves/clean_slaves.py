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
import os, sys, shutil, stat, traceback, subprocess, time

reboot_needed = False

def write_test_result(expr, name, output):
    with open(name + ".junit.xml","w") as junitfile:
        junitfile.write("<?xml version=\"1.0\"?>\n<testsuite>\n  <testcase name=\"" + name + "\" classname=\"dose_test\"")
        if expr:
            """success"""
            junitfile.write("/>\n")
        else:
            """failure"""
            junitfile.write(">\n    <error message=\"Failed\">" +
                            output +
                            "\n</error>\n  </testcase>\n")
        junitfile.write("</testsuite>")
    return expr


def delete_workspace():
    def onerror(function, path, excinfo):
        try:
            # path contains the path of the file that couldn't be removed
            # let's just assume that it's read-only and unlink it.
            if os.path.isfile(path):
                os.chmod(path, stat.S_IWUSR|stat.S_IRUSR)
            os.unlink( path )
            return
        except Exception as e:
            exc = e

        #hmm, maybe the path is very long and we're on windows
        try:
            if sys.platform == "win32":
                newpath = "\\\\?\\" + os.path.join(os.getcwd(),path)
                os.chmod(newpath, stat.S_IWRITE)
                os.unlink(newpath)
                return
        except Exception as ex:
            exc = e

        print("Failed to delete",path))
        write_test_result(False, "delete " + path.replace("/","_"), traceback.format_exc(exc))

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
    os.chdir(BASE)
    contents = os.listdir(".")
    if not os.path.isdir("workspace"):
        print("Could not find 'workspace' dir in", BASE)
        sys.exit(1)

    print("Deleting directory 'workspace' in", BASE)
    shutil.rmtree("workspace",onerror=onerror)

def linux_checks():
    lsof = subprocess.check_output(("lsof"))
    if lsof.find("LLL_") != -1:
        reboot_needed = True
    if lsof.find("SAFIR_") != -1:
        reboot_needed = True

    if platform.linux_distribution()[0] in ("debian", "Ubuntu"):
        cmd = ["sudo", "--non-interactive", "apt-get", "--yes", "purge"]
        cache = apt.cache.Cache()
        uninstall = False
        for p in ("safir-sdk-core", "safir-sdk-core-dev", "safir-sdk-core-testsuite"):
            if cache.has_key(p) and cache[p].is_installed:
                cmd.append(pkg)
                uninstall = True

        if uninstall:
            subprocess.call(cmd)


def reboot():
    if sys.platform == "win32":
        subprocess.call(("shutdown", "-r"))
    else:
        subprocess.call(("sudo", "reboot"))
    time.sleep(60000)

def main():
    delete_workspace()

    if sys.platform == "win32":
        pass
    else:
        linux_checks()

    if reboot_needed:
        reboot()
    return 0

sys.exit(main())
