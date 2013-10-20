#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Google App Engine app"""
import webapp2
import re
import string
from handlers import *
from security import *

from google.appengine.ext import db



app = webapp2.WSGIApplication([
    ('/', FrontPageHandler),
    ('/maps', MapsHandler),
    ('/gent-en', GentEnHandler),
    ('/gent-es', GentEsHandler)],
    debug=True)
