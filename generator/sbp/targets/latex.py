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
from sbp.utils import fmt_repr
from operator import itemgetter, attrgetter, methodcaller


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

def nobrackets(v):
  return v.translate(None, '[]')

def removearray(v):
  import re
  return re.sub('^[a-z]*\[N\]\.', '', v)

JENV.filters['escape_tex'] = escape_tex
JENV.filters['classnameify'] = classnameify
JENV.filters['commentify'] = commentify
JENV.filters['packagenameify'] = packagenameify
JENV.filters['size'] = size
JENV.filters['short_desc'] = short_desc
JENV.filters['desc'] = desc
JENV.filters['nobrackets'] = nobrackets
JENV.filters['removearray'] = removearray

field_sizes = {
    'u8': 1,
    'u16': 2,
    'u32': 4,
    'u64': 8,
    's8': 1,
    's16': 2,
    's32': 4,
    's64': 8,
    'float': 4,
    'double': 8,
}

CONSTRUCT_CODE = set(['u8', 'u16', 'u32', 'u64', 's8', 's16', 's32', 's64', 'float', 'double'])

class TableItem:
  def __init__(self, pkg, name, sbp_id, short_desc, desc, size, fields):
    self.pkg = pkg
    self.name = name
    self.sbp_id = sbp_id
    self.short_desc = short_desc or ""
    self.desc = desc or ""
    self.size = size
    self.fields = fields

class FieldItem:
  def __init__(self, name, fmt, offset, size, units, desc, n_with_values, bitfields):
    self.name = name
    self.fmt = fmt
    self.offset = offset
    self.size = size
    self.units = units
    self.desc = desc or ""
    self.n_with_values = n_with_values
    self.bitfields = bitfields

def handle_fields(definitions, fields, prefix, offset, multiplier):
  items = []
  for f in fields:
    if f.type_id == "array":
      name = f.options['fill'].value
      definition = next(d for d in definitions if name == d.identifier)
      prefix_name = '.'.join([prefix, f.identifier]) if prefix else f.identifier
      (new_items, new_offset, new_multiplier) = handle_fields(definitions, definition.fields, prefix_name + "[*N*]", offset, multiplier)
      multiplier = new_offset - offset
      (newer_items, newer_offset, newer_multiplier) = handle_fields(definitions, definition.fields, prefix_name + "[N]", offset, multiplier)
      items += newer_items
      offset = newer_offset
    elif f.type_id not in CONSTRUCT_CODE:
      name = f.type_id
      definition = next(d for d in definitions if name == d.identifier)
      prefix_name = '.'.join([prefix, f.identifier]) if prefix else f.identifier
      (new_items, new_offset, new_multiplier) = handle_fields(definitions, definition.fields, prefix_name, offset, multiplier)
      items += new_items
      offset = new_offset
      multiplier = new_multiplier
    else:
      size = field_sizes[f.type_id]
      name = f.type_id
      adj_offset = "%dN+%d" % (multiplier, offset) if multiplier else offset
      prefix_name = '.'.join([prefix, f.identifier]) if prefix else f.identifier
      n_with_values = f.options['n_with_values'].value
      bitfields = f.options['fields'].value if n_with_values > 0 else None
      item = FieldItem(prefix_name, name, adj_offset, size, f.units, f.desc, n_with_values, bitfields)
      items.append(item)
      offset += size
  return (items, offset, multiplier)

def render_source(output_dir, package_specs):
  """
  Render and output
  """
  destination_filename = "./sbp/targets/resources/sbp_out.tex"
  py_template = JENV.get_template(TEMPLATE_NAME)
  msgs = []
  for p in sorted(package_specs, key=attrgetter('identifier')):
    pkg_name = p.identifier
    for d in p.definitions:
      if d.public and d.static and d.sbp_id:
        items, size, multiplier = handle_fields(p.definitions, d.fields, "", 0, None)
        adj_size = "%dN+%d" % (multiplier, size) if multiplier else size
        ti = TableItem(pkg_name, d.identifier, d.sbp_id, d.short_desc, d.desc, adj_size, items)
        pkg_name = ""
        msgs.append(ti)
  with open(destination_filename, 'w') as f:
    f.write(py_template.render(msgs=msgs))

