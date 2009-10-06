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
# Alex 20091006
# eLyXer indexer: creates a TOC just like elyxer.py --toc
# http://www.nongnu.org/elyxer/


from io.convert import *
from util.trace import Trace
from util.options import *


class Indexer(eLyXerConverter):
  "Creates a TOC from an already processed eLyXer HTML output."

  def index(self):
    "Create the index (TOC)."
    while not self.reader.finished():
      line = self.reader.currentline()
      tag, part = self.readtag(line)
      if tag:
        Trace.message('Tag: ' + tag + ' for part ' + part)
        self.writer.write(['<', tag, '>', '\n'])
        self.writer.write(self.readcontents(tag))
      self.reader.nextline()
    self.reader.close()
    self.writer.close()

  def readtag(self, line):
    "Read the tag and the part name, from something like:"
    """<tag class="part">"""
    if not line.startswith('<') or not line.endswith('>'):
      return None, None
    words = line[1:-1].split()
    if len(words) != 2 or not words[1].startswith('class="'):
      return None, None
    return words[0], words[1].split('"')[1]

  def readcontents(self, tag):
    "Read the contents of a tag"
    return []

def convertdoc(args):
  "Read a whole document and write it"
  ioparser = InOutParser().parse(args)
  indexer = Indexer(ioparser)
  indexer.index()

def main():
  "Main function, called if invoked from the command line"
  args = list(sys.argv)
  del args[0]
  Options().parseoptions(args)
  convertdoc(args)

if __name__ == '__main__':
  main()

