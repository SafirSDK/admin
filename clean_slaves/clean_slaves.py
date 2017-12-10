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
import os, sys, shutil, stat, traceback, subprocess, time, platform

#try to import a package that we need for the debian installer
#this will fail quietly on all other platforms, which is all right.
try:
    import apt
except:
    pass

def log(*args, **kwargs):
    print(*args, **kwargs)
    sys.stdout.flush()


reboot_needed = False
exitcode = 0

def delete_workspace():
    def onerror(function, path, excinfo):
        global reboot_needed
        global exitcode

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
        except Exception as e:
            exc = e

        #ok, if we're on windows we can try to mark it for removal and reboot
        if sys.platform == "win32":
            log("Marking file for deletion on reboot:",path)
            import ctypes
            MOVEFILE_DELAY_UNTIL_REBOOT = 4
            newpath = "\\\\?\\" + os.path.join(os.getcwd(),path)
            ctypes.windll.kernel32.MoveFileExA(newpath, None,
                                               MOVEFILE_DELAY_UNTIL_REBOOT)
            reboot_needed = True
            return
        log("Failed to delete",path)
        exitcode = 1

    #kill some processes..
    if sys.platform == "win32":
        subprocess.call("taskkill /f /im cl.exe")

    BASE = os.environ.get("BASE")
    if BASE is None:
        log("Failed to find Jenkins base directory, trying $HOME/jenkins")
        HOME = os.environ.get("HOME")
        if HOME is None:
            log("HOME environment variable is not set")
            sys.exit(1)
        BASE=os.path.join(HOME,"jenkins")

    if not os.path.isdir(BASE):
        log(BASE, "does not appear to be a directory")
        sys.exit(1)
    os.chdir(BASE)
    contents = os.listdir(".")
    if not os.path.isdir("workspace"):
        log("Could not find 'workspace' dir in", BASE)
        sys.exit(1)

    log("Deleting directory 'workspace' in", BASE)
    shutil.rmtree("workspace",onerror=onerror)

def linux_checks():
    global reboot_needed
    global exitcode

    lsof = subprocess.check_output(("lsof"))

    if lsof.find("LLL_") != -1:
        log("Found LLL_ in lsof output")
        reboot_needed = True
    if lsof.find("SAFIR_") != -1:
        log("Found SAFIR_ in lsof output")
        reboot_needed = True
    if lsof.find("DOSE_") != -1:
        log("Found DOSE_ in lsof output")
        reboot_needed = True
    if lsof.find("DOB_") != -1:
        log("Found DOB_ in lsof output")
        reboot_needed = True
    if lsof.find("INITIALIZATION_") != -1:
        log("Found INITIALIZATION_ in lsof output")
        reboot_needed = True

    if platform.linux_distribution()[0] in ("debian", "Ubuntu"):
        cmd = ["sudo", "--non-interactive", "apt-get", "--yes", "purge"]
        cache = apt.cache.Cache()
        uninstall = False
        for p in ("safir-sdk-core", "safir-sdk-core-dev", "safir-sdk-core-testsuite"):
            if cache.has_key(p) and cache[p].is_installed:
                log(p,"is installed")
                cmd.append(p)
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
    global reboot_needed
    global exitcode

    delete_workspace()

    if sys.platform == "win32":
        pass
    else:
        linux_checks()

    if reboot_needed:
        reboot()
    return

main()
sys.exit(exitcode)
