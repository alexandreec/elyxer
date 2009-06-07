#! /usr/bin/env python
# -*- coding: utf-8 -*-

#   eLyXer -- convert LyX source files to HTML output.
#
#   Copyright (C) 2009 Alex Fernández
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

# --end--
# Alex 20090314
# Modifies the license of a Python source file

import os
import sys
import codecs
from io.fileline import *
from io.bulk import *
from util.trace import Trace


mark = '# --end--'

def process(reader, writer, license):
  "Conflate all Python files used in filein to fileout"
  for line in license:
    writer.writestring(line)
  while not reader.currentline().startswith(mark):
    reader.nextline()
  while not reader.finished():
    line = reader.currentline()
    writer.writestring(line)
    reader.nextline()
  reader.close()

def processall(args):
  "Process all arguments"
  del args[0]
  if len(args == 0):
    Trace.error('Usage: licensify.py licensefile [file...]')
    return
  licensefile = args[0]
  license = readall(licensefile)
  del args[0]
  while len(args) > 0:
    filename = args[0]
    reader, writer = getfiles(filename)
    del args[0]
    process(reader, writer, license)
    os.rename(filename + '.temp', filename)

processall(sys.argv)

