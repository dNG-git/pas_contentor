# -*- coding: utf-8 -*-
##j## BOF

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?pas;contentor

The following license agreement remains valid unless any additions or
changes are being made by direct Netware Group in a written form.

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc.,
59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;gpl
----------------------------------------------------------------------------
#echo(pasContentorVersion)#
#echo(__FILEPATH__)#
"""

# pylint: disable=unused-argument

from dNG.pas.database.schema import Schema
from dNG.pas.module.named_loader import NamedLoader
from dNG.pas.plugins.hook import Hook

def after_apply_schema(params, last_return = None):
#
	"""
Called for "dNG.pas.Database.applySchema.after"

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.1.00
	"""

	category_class = NamedLoader.get_class("dNG.pas.database.instances.ContentorCategory")
	Schema.apply_version(category_class)

	document_class = NamedLoader.get_class("dNG.pas.database.instances.ContentorDocument")
	Schema.apply_version(document_class)

	return last_return
#

def load_all(params, last_return = None):
#
	"""
Load and register all SQLAlchemy objects to generate database tables.

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.1.00
	"""

	NamedLoader.get_class("dNG.pas.database.instances.ContentorCategory")
	NamedLoader.get_class("dNG.pas.database.instances.ContentorDocument")

	return last_return
#

def register_plugin():
#
	"""
Register plugin hooks.

:since: v0.1.00
	"""

	Hook.register("dNG.pas.Database.applySchema.after", after_apply_schema)
	Hook.register("dNG.pas.Database.loadAll", load_all)
#

def unregister_plugin():
#
	"""
Unregister plugin hooks.

:since: v0.1.00
	"""

	Hook.unregister("dNG.pas.Database.applySchema.after", after_apply_schema)
	Hook.unregister("dNG.pas.Database.loadAll", load_all)
#

##j## EOF