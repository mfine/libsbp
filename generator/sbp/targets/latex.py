#!/usr/bin/env python
# Copyright (C) 2015 Swift Navigation Inc.
# Contact: Bhaskar Mookerji <mookerji@swiftnav.com>
#
# This source is subject to the license found in the file 'LICENSE' which must
# be be distributed together with this source. All other rights reserved.
#
# THIS CODE AND INFORMATION IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND,
# EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A PARTICULAR PURPOSE.

import re
from sbp.targets.templating import *

TEMPLATE_NAME = "sbp_messages_desc.tex"

LATEX_SUBS = (
    (re.compile(r'\\'), r'\\textbackslash'),
    (re.compile(r'([{}_#%&$])'), r'\\\1'),
    (re.compile(r'~'), r'\~{}'),
    (re.compile(r'\^'), r'\^{}'),
    (re.compile(r'_'), r'_'),
    (re.compile(r'"'), r"''"),
    (re.compile(r'\.\.\.+'), r'\\ldots'),
)

def escape_tex(value):
    newval = value
    for pattern, replacement in LATEX_SUBS:
        newval = pattern.sub(replacement, newval)
    return newval

def classnameify(s):
  return ''.join(w if w in ACRONYMS else w.title() for w in s.split('_'))

def commentify(value):
  return '\n'.join([' * ' + l for l in value.split('\n')[:-1]])

def packagenameify(s):
  return ''.join(w if w in ACRONYMS else w.title() for w in s.split('.')[-1:])

def size(d):
  return -1

def short_desc(d):
  return d.short_desc if d.short_desc else ""

def desc(d):
  return d.desc if d.desc else ""

JENV.filters['escape_tex'] = escape_tex
JENV.filters['classnameify'] = classnameify
JENV.filters['commentify'] = commentify
JENV.filters['packagenameify'] = packagenameify
JENV.filters['size'] = size
JENV.filters['short_desc'] = short_desc
JENV.filters['desc'] = desc

def render_source(output_dir, package_specs):
  """
  Render and output
  """
  destination_filename = "./sbp/targets/resources/sbp_out.tex"
  py_template = JENV.get_template(TEMPLATE_NAME)
  with open(destination_filename, 'w') as f:
    f.write(py_template.render(pkgs=package_specs))

