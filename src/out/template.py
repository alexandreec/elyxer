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
# Alex 20100620
# eLyXer HTML templates

import datetime
from io.bulk import *
from parse.position import *
from util.trace import Trace
from util.options import *


class HTMLTemplate(object):
  "A template for HTML generation."

  current = None

  def getheader(self):
    "Get the header (before content) of the template."
    return []

  def convertheader(self):
    "Convert the header and all variables."
    return self.convert(self.getheader())

  def convertfooter(self):
    "Convert the footer and all variables."
    return self.convert(self.getfooter())

  def convert(self, html):
    "Convert a bit of HTML replacing all variables."
    varmap = VariableMap()
    for index, line in enumerate(html):
      if '<!--$' in line:
        html[index] = varmap.replace(line)
    return html

  def getfooter(self):
    "Get the footer (after content) of the template."
    return []

  def get(cls):
    "Choose the right HTML template."
    if not cls.current:
      if Options.raw:
        cls.current = RawTemplate()
      elif Options.template:
        cls.current = FileTemplate().read()
      else:
        cls.current = DefaultTemplate()
    return cls.current

  get = classmethod(get)

class RawTemplate(HTMLTemplate):
  "The template for raw output."

  def getheader(self):
    "Get the raw header."
    return ['<!--starthtml-->\n']

  def getfooter(self):
    "Get the raw footer."
    return ['\n\n<!--endhtml-->']

class FileTemplate(HTMLTemplate):
  "A template read from a file."

  divider = '<!--$content-->'

  def read(self):
    "Read the file, separate header and footer."
    self.header = []
    lines = []
    for line in self.templatelines():
      if FileTemplate.divider == line:
        self.header = lines
        lines = []
      else:
        lines.append(line)
    if self.header == []:
      Trace.error('No ' + FileTemplate.divider + ' in template')
      self.header = lines
      lines = []
    self.footer = lines
    return self

  def templatelines(self):
    "Read all lines in the template, separate content into its own line."
    template = BulkFile(Options.template).readall()
    for line in template:
      if not FileTemplate.divider in line:
        yield line
      else:
        split = line.split(FileTemplate.divider)
        for part in split[:-1]:
          yield part
          yield FileTemplate.divider
        yield split[-1]

  def getheader(self):
    "Return the header (before content)."
    return self.header

  def getfooter(self):
    "Return the footer (after the content)."
    return self.footer

class DefaultTemplate(HTMLTemplate):
  "The default HTML template when not configured."

  def getheader(self):
    "Get the default header (before content)."
    html = []
    if not Options.html:
      html.append(u'<?xml version="1.0" encoding="<!--$encoding-->"?>\n')
      html.append(u'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n')
      html.append(u'<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n')
    else:
      html.append(u'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\n')
      html.append(u'<html lang="en">\n')
    html.append(u'<head>\n')
    html.append(u'<meta http-equiv="Content-Type" content="text/html; charset=<!--$encoding-->"/>\n')
    html.append(u'<meta name="generator" content="http://www.nongnu.org/elyxer/"/>\n')
    html.append(u'<meta name="create-date" content="<!--$date-->"/>\n')
    html.append(u'<link rel="stylesheet" href="<!--$css-->" type="text/css" media="screen"/>\n')
    html.append(u'<title><!--$title--></title>\n')
    if Options.jsmath:
      html.append(u'<script type="text/javascript" src="<!--$jsmath-->/plugins/noImageFonts.js"></script>\n')
      html.append(u'<script type="text/javascript" src="<!--$jsmath-->/easy/load.js"></script>\n')
    if Options.mathjax:
      html.append(u'<script type="text/javascript" src="<!--$mathjax-->/MathJax.js">\n')
      html.append(u'  //  Load MathJax and get it running\n')
      html.append(u'  MathJax.Hub.Config({ jax: ["input/TeX"],\n') # output/HTML-CSS
      html.append(u'  config: ["MMLorHTML.js"],\n')
      html.append(u'  extensions: ["TeX/AMSmath.js","TeX/AMSsymbols.js"],\n')
      html.append(u'  "HTML-CSS": { imageFont: null }\n')
      html.append(u'  });\n')
      html.append(u'</script>\n')
    html.append('</head>\n')
    html.append('<body>\n')
    html.append('<div id="globalWrapper">\n')
    if Options.jsmath or Options.mathjax:
      if Options.mathjax:
        html.append(u'<script type="math/tex">\n')
        html.append(u'\\newcommand{\\lyxlock}{}\n')
        html.append(u'</script>\n')
      html.append(u'<noscript>\n')
      html.append(u'<div class="warning">\n')
      html.append(TranslationConfig.constants['jsmath-warning'])
      if Options.jsmath:
        html.append(u'<a href="http://www.math.union.edu/locate/jsMath">jsMath</a>')
      if Options.mathjax:
        html.append(u'<a href="http://www.mathjax.org/">MathJax</a>')
      html.append(TranslationConfig.constants['jsmath-requires'])
      html.append(TranslationConfig.constants['jsmath-enable'] + '\n')
      html.append(u'</div><hr/>\n')
      html.append(u'</noscript>\n')
    return html

  def getfooter(self):
    "Get the default footer (after content)."
    html = []
    html.append('\n\n')
    footer = self.createfooter()
    if len(footer) > 0:
      html.append('<hr class="footer"/>\n')
      html += footer
    html.append('</div>\n')
    html.append('</body>\n')
    html.append('</html>\n')
    return html

  def createfooter(self):
    "Create the footer proper."
    html = []
    if Options.copyright:
      html.append('<div class="footer">\nCopyright (C) <!--$year--> <!--$author-->\n</div>\n')
    if Options.nofooter:
      return html
    html.append('<div class="footer" id="generated-by">\n')
    html.append(Translator.translate('generated-by'))
    html.append('<a href="http://elyxer.nongnu.org/">eLyXer <!--$version--></a>')
    html.append(Translator.translate('generated-on'))
    html.append('<span class="create-date"><!--$datetime--></span>\n')
    html.append('</div>\n')
    return html

class VariableMap(object):
  "A map with all replacement variables."

  def __init__(self):
    self.variables = dict()
    self.variables['title'] = DocumentTitle().getvalue()
    self.variables['author'] = DocumentAuthor().getvalue()
    self.variables['version'] = GeneralConfig.version['number'] + ' (' \
        + GeneralConfig.version['date'] + ')'
    self.variables['year'] = unicode(datetime.date.today().year)
    self.variables['date'] = datetime.date.today().isoformat()
    self.variables['datetime'] = datetime.datetime.now().isoformat()
    self.variables['css'] = Options.css
    if Options.iso885915:
      self.variables['encoding'] = 'ISO-8859-1'
    else:
      self.variables['encoding'] = 'UTF-8'
    if Options.jsmath:
      self.variables['jsmath'] = Options.jsmath
    if Options.mathjax:
      self.variables['mathjax'] = Options.mathjax

  def replace(self, line):
    "Replace all variables in a line."
    result = ''
    pos = TextPosition(line)
    while not pos.finished():
      if pos.checkskip('<!--$'):
        result += self.getvalue(pos)
      else:
        result += pos.currentskip()
    return result

  def getvalue(self, pos):
    "Get the value of the variable at the given position."
    value = ''
    key = pos.globalpha()
    if not key in self.variables:
      Trace.error('Template variable ' + key + ' not found')
    else:
      value = self.variables[key]
    if not pos.checkskip('-->'):
      Trace.error('Weird template format in ' + line)
    return value

class DocumentTitle(object):
  "The title of the whole document."

  pdftitle = None
  title = None

  def getvalue(self):
    "Return the correct title from the option or the PDF title."
    if Options.title:
      return Options.title
    if DocumentTitle.title:
      return DocumentTitle.title
    if DocumentTitle.pdftitle:
      return DocumentTitle.pdftitle
    return 'Converted document'

class DocumentAuthor(object):
  "The author of the document."

  author = ''

  def appendauthor(cls, authorline):
    "Append a line with author information."
    cls.author += authorline

  appendauthor = classmethod(appendauthor)

  def getvalue(self):
    "Get the document author."
    return DocumentAuthor.author
