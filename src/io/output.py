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
# Alex 20090203
# eLyXer html outputters

import codecs
import datetime
from util.trace import Trace
from util.options import *


class EmptyOutput(object):
  "The output for some container"

  def gethtml(self, container):
    "Return empty HTML code"
    return []

class FixedOutput(object):
  "Fixed output"

  def gethtml(self, container):
    "Return constant HTML code"
    return container.html

class ContentsOutput(object):
  "Outputs the contents converted to HTML"

  def gethtml(self, container):
    "Return the HTML code"
    html = []
    if container.contents == None:
      return html
    for element in container.contents:
      if not hasattr(element, 'gethtml'):
        Trace.error('No html in ' + element.__class__.__name__ + ': ' + unicode(element))
        return html
      html += element.gethtml()
    return html

class TaggedOutput(ContentsOutput):
  "Outputs an HTML tag surrounding the contents"

  def __init__(self):
    self.breaklines = False

  def settag(self, tag, breaklines=False):
    "Set the value for the tag"
    self.tag = tag
    self.breaklines = breaklines
    return self

  def setbreaklines(self, breaklines):
    "Set the value for breaklines"
    self.breaklines = breaklines
    return self

  def gethtml(self, container):
    "Return the HTML code"
    if hasattr(container, 'breaklines'):
      self.breaklines = container.breaklines
    if hasattr(container, 'tag'):
      self.tag = container.tag
    html = [self.getopen(container)]
    html += ContentsOutput.gethtml(self, container)
    html.append(self.getclose(container))
    return html

  def getopen(self, container):
    "Get opening line"
    if self.tag == '':
      return ''
    open = '<' + self.tag + '>'
    if self.breaklines:
      return open + '\n'
    return open

  def getclose(self, container):
    "Get closing line"
    if self.tag == '':
      return ''
    close = '</' + self.tag.split()[0] + '>'
    if self.breaklines:
      return '\n' + close + '\n'
    return close

class MirrorOutput(object):
  "Returns as output whatever comes along"

  def gethtml(self, container):
    "Return what is put in"
    return container.contents

class HeaderOutput(object):
  "Returns the HTML headers"

  def gethtml(self, container):
    "Return a constant header"
    if not Options.html:
      html = [u'<?xml version="1.0" encoding="UTF-8"?>\n']
      html.append(u'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n')
      html.append(u'<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n')
    else:
      html = [u'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\n']
      html.append(u'<html lang="en">\n')
    html.append(u'<head>\n')
    html.append(u'<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>\n')
    html.append(u'<meta name="generator" content="http://www.nongnu.org/elyxer/"/>\n')
    html.append(u'<meta name="create-date" content="' + datetime.date.today().isoformat() + '"/>\n')
    html.append(u'<link rel="stylesheet" href="' + Options.css + '" type="text/css" media="screen"/>\n')
    html.append(u'<title>' + Options.title + '</title>\n')
    html.append('</head>\n')
    html.append('<body>\n')
    html.append('<div id="globalWrapper">\n')
    return html

class FooterOutput(object):
  "Return the HTML code for the footer"

  author = None

  def gethtml(self, container):
    "Footer HTML"
    html = []
    if FooterOutput.author and not Options.nocopy:
      html.append('<hr/>\n')
      year = datetime.date.today().year
      html.append('<p>Copyright (C) ' + str(year) + ' ' + FooterOutput.author
          + '</p>\n')
    html.append('</div>\n')
    html.append('</body>\n')
    html.append('</html>\n')
    return html

