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
# Alex 20090524
# eLyXer list postprocessing

from gen.container import *
from util.trace import Trace
from gen.structure import *
from gen.layout import *
from gen.inset import *
from ref.link import *
from post.postprocess import *


class PendingList(object):
  "A pending list"

  def __init__(self):
    self.contents = []
    self.type = None

  def additem(self, item):
    "Add a list item"
    self.contents += item.contents
    if not self.type:
      self.type = item.type

  def adddeeper(self, deeper):
    "Add a deeper list item"
    if self.empty():
      self.insertfake()
    item = self.contents[-1]
    self.contents[-1].contents += deeper.contents

  def generate(self):
    "Get the resulting list"
    if not self.type:
      tag = 'ul'
    else:
      tag = TagConfig.listitems[self.type]
    text = TaggedText().complete(self.contents, tag, True)
    self.__init__()
    return text

  def isduewithitem(self, item):
    "Decide whether the pending list must be generated before the given item"
    if not self.type:
      return False
    if self.type != item.type:
      return True
    return False

  def isduewithnext(self, next):
    "Applies only if the list is finished with next item."
    if not next:
      return True
    if not isinstance(next, ListItem) and not isinstance(next, DeeperList):
      return True
    return False

  def empty(self):
    return len(self.contents) == 0

  def insertfake(self):
    "Insert a fake item"
    item = TaggedText().constant('', 'li class="nested"', True)
    self.contents = [item]
    self.type = 'Itemize'

  def __unicode__(self):
    result = 'pending ' + unicode(self.type) + ': ['
    for element in self.contents:
      result += unicode(element) + ', '
    if len(self.contents) > 0:
      result = result[:-2]
    return result + ']'

class PostListItem(object):
  "Postprocess a list item"

  processedclass = ListItem

  def postprocess(self, last, item, next):
    "Add the item to pending and return an empty item"
    if not hasattr(self.postprocessor, 'list'):
      self.postprocessor.list = PendingList()
    self.postprocessor.list.additem(item)
    if self.postprocessor.list.isduewithnext(next):
      return self.postprocessor.list.generate()
    if isinstance(next, ListItem) and self.postprocessor.list.isduewithitem(next):
      return self.postprocessor.list.generate()
    return BlackBox()

class PostDeeperList(object):
  "Postprocess a deeper list"

  processedclass = DeeperList

  def postprocess(self, last, deeper, next):
    "Append to the list in the postprocessor"
    if not hasattr(self.postprocessor, 'list'):
      self.postprocessor.list = PendingList()
    self.postprocessor.list.adddeeper(deeper)
    if self.postprocessor.list.isduewithnext(next):
      return self.postprocessor.list.generate()
    return BlackBox()

Postprocessor.stages += [PostListItem, PostDeeperList]

