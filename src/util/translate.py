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
# Alex 20100112
# eLyXer translations and translation generation

import gettext
from util.trace import Trace
from conf.config import *


class Translator(object):
  "Reads the configuration file and tries to find a translation."
  "Otherwise falls back to the messages in the config file."

  instance = None

  def translate(cls, key):
    "Get the translated message for a key."
    return cls.instance.getmessage(key)

  translate = classmethod(translate)

  def __init__(self):
    self.translations = None

  def getmessage(self, key):
    "Get the translated message for the given key."
    message = self.getuntranslated(key)
    try:
      translation = gettext.translation('elyxer')
      message = translation.ugettext(message)
    except IOError:
      pass
    return message

  def getuntranslated(self, key):
    "Get the untranslated message."
    return TranslationConfig.constants[key]

Translator.instance = Translator()

class TranslationExport(object):
  "Export the translation to a file."

  def __init__(self, writer):
    self.writer = writer

  def export(self, constants):
    "Export the translation constants as a .po file."
    for key, message in constants.iteritems():
      self.writer.writeline('')
      self.writer.writeline('#: ' + key)
      self.writer.writeline('msgid  "' + message + '"')
      self.writer.writeline('msgstr "' + message + '"')
    self.writer.close()

