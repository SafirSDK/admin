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

def log(*args, **kwargs):
    print(*args, **kwargs)
    sys.stdout.flush()


xml = """<table sorttable="yes">
  <tr>
    <td value="Table title" bgcolor="red" fontcolor="black" fontattribute="bold" href="report.xls" align="center" width="200"/>
    <td value="Column 1" bgcolor="white" fontcolor="black" fontattribute="normal" href="" align="center" width="200"/>
  </tr>
  <tr>
    <td value="Line 1" bgcolor="white" fontcolor="black" fontattribute="normal" href="" align="left" width="200"/>
    <td value="Value 1" bgcolor="white" fontcolor="black" fontattribute="normal" href="" align="none" width="200"/>
  </tr>
</table>"""

with open("test.xml","w") as f:
    f.write(xml)
