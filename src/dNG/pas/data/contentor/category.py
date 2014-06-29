# -*- coding: utf-8 -*-
##j## BOF

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?pas;contentor

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
http://www.direct-netware.de/redirect.py?licenses;gpl
----------------------------------------------------------------------------
#echo(pasContentorVersion)#
#echo(__FILEPATH__)#
"""

from dNG.pas.data.binary import Binary
from dNG.pas.data.data_linker import DataLinker
from dNG.pas.data.ownable_mixin import OwnableMixin
from dNG.pas.data.subscribable_mixin import SubscribableMixin
from dNG.pas.database.instances.contentor_category import ContentorCategory as _DbContentorCategory

class Category(DataLinker, OwnableMixin, SubscribableMixin):
#
	"""
"Category" represents a contentor category.

TODO: Handle "locked" in is_readable, is_*, ...

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: contentor
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;gpl
             GNU General Public License 2
	"""

	def __init__(self, db_instance = None):
	#
		"""
Constructor __init__(Category)

:param db_instance: Encapsulated SQLAlchemy database instance

:since: v0.1.00
		"""

		DataLinker.__init__(self, db_instance)
		OwnableMixin.__init__(self)
		SubscribableMixin.__init__(self)
	#

	def set_data_attributes(self, **kwargs):
	#
		"""
Sets values given as keyword arguments to this method.

:since: v0.1.00
		"""

		self._ensure_thread_local_instance(_DbContentorCategory)

		with self:
		#
			DataLinker.set_data_attributes(self, **kwargs)

			if ("id_subscription" in kwargs): self.local.db_instance.id_subscription = Binary.utf8(kwargs['id_subscription'])
			if ("entry_type" in kwargs): self.local.db_instance.entry_type = kwargs['entry_type']
			if ("owner_type" in kwargs): self.local.db_instance.owner_type = kwargs['owner_type']
			if ("locked" in kwargs): self.local.db_instance.locked = kwargs['locked']
			if ("guest_permission" in kwargs): self.local.db_instance.public_permission = kwargs['guest_permission']
			if ("user_permission" in kwargs): self.local.db_instance.public_permission = kwargs['user_permission']
		#
	#
#

##j## EOF