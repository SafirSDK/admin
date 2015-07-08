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
import sys, re, os

def log(*args, **kwargs):
    print(*args, **kwargs)
    sys.stdout.flush()


def main():
    info = dict()
    for dir in os.listdir("."):
        if not os.path.isdir(dir):
            continue
        #skip non-build machines for the time being
        if dir.find("-build") == -1:
            continue
        match = re.match(r"label=(.*)",dir)
        if match is None:
            log("Skipping",dir)
            continue
        name = match.group(1)
        info[name] = dict()
        with open(os.path.join(dir,"versions.txt")) as f:
            for line in f:
                match = re.match(r"(.*): *(.*)",line)
                info[name][match.group(1)] = match.group(2)
    log (info)

    with open("version_summary.xml","w") as f:
        f.write("<table><tr>\n  <td value=''/>\n")
        try: #get first key in both py2 and 3
            firstkey = next(info.iterkeys())
        except:
            firstkey = next(iter(info.keys()))

        for sw in info[firstkey]:
            f.write("  <td value='" + sw + "'/>\n")
        f.write("</tr>")

        for slave in info:
            f.write("<tr>\n")
            f.write("  <td value='" + slave + "'/>\n")
            for sw in info[slave]:
                f.write("  <td value='" + info[slave][sw] + "'/>\n")
            f.write("</tr>\n")

        f.write("</table>")

if __name__ == "__main__":
    sys.exit(main())
