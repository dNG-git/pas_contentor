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

from dNG.pas.data.binary import Binary
from dNG.pas.data.data_linker import DataLinker
from dNG.pas.data.ownable_lockable_write_mixin import OwnableLockableWriteMixin
from dNG.pas.data.subscribable_mixin import SubscribableMixin
from dNG.pas.database.lockable_mixin import LockableMixin
from dNG.pas.database.instances.contentor_category import ContentorCategory as _DbContentorCategory

class Category(DataLinker, LockableMixin, OwnableLockableWriteMixin, SubscribableMixin):
#
	"""
"Category" represents a contentor category.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: contentor
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""

	_DB_INSTANCE_CLASS = _DbContentorCategory
	"""
SQLAlchemy database instance class to initialize for new instances.
	"""

	def __init__(self, db_instance = None):
	#
		"""
Constructor __init__(Category)

:param db_instance: Encapsulated SQLAlchemy database instance

:since: v0.1.00
		"""

		DataLinker.__init__(self, db_instance)
		LockableMixin.__init__(self)
		OwnableLockableWriteMixin.__init__(self)
		SubscribableMixin.__init__(self)
	#

	def get_categories(self, offset = 0, limit = -1):
	#
		"""
Returns the children categories of this instance.

:param offset: SQLAlchemy query offset
:param limit: SQLAlchemy query limit

:return: (list) Category children instances
:since:  v0.1.01
		"""

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.get_categories({1:d}, {2:d})- (#echo(__LINE__)#)", self, offset, limit, context = "pas_datalinker")
		return DataLinker.get_sub_entries(self, offset, limit, identity = "ContentorCategory")
	#

	def get_categories_count(self):
	#
		"""
Returns the number of child categories of this instance.

:return: (int) Number of child categories
:since:  v0.1.01
		"""

		return DataLinker.get_sub_entries_count(self, identity = "ContentorCategory")
	#

	def _get_data_attribute(self, attribute):
	#
		"""
Returns the data for the requested attribute.

:param attribute: Requested attribute

:return: (mixed) Value for the requested attribute; None if undefined
:since:  v0.1.00
		"""

		return (self.get_sub_entries_count()
		        if (attribute == "sub_entries") else
		        DataLinker._get_data_attribute(self, attribute)
		       )
	#

	def get_sub_entries(self, offset = 0, limit = -1):
	#
		"""
Returns the child entries of this instance.

:param offset: SQLAlchemy query offset
:param limit: SQLAlchemy query limit

:return: (list) DataLinker children instances
:since:  v0.1.00
		"""

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.get_sub_entries({1:d}, {2:d})- (#echo(__LINE__)#)", self, offset, limit, context = "pas_datalinker")
		return DataLinker.get_sub_entries(self, offset, limit, exclude_identity = "ContentorCategory")
	#

	def get_sub_entries_count(self):
	#
		"""
Returns the number of child entries of this instance.

:return: (int) Number of child entries
:since:  v0.1.00
		"""

		return DataLinker.get_sub_entries_count(self, exclude_identity = "ContentorCategory")
	#

	def _get_unknown_data_attribute(self, attribute):
	#
		"""
Returns the data for the requested attribute not defined for this instance.

:param attribute: Requested attribute

:return: (dict) Value for the requested attribute; None if undefined
:since:  v0.1.00
		"""

		if (attribute == "categories"): _return = self.get_categories_count()
		else: _return = DataLinker._get_unknown_data_attribute(self, attribute)

		return _return
	#

	def set_data_attributes(self, **kwargs):
	#
		"""
Sets values given as keyword arguments to this method.

:since: v0.1.00
		"""

		with self:
		#
			DataLinker.set_data_attributes(self, **kwargs)

			if ("id_subscription" in kwargs): self.local.db_instance.id_subscription = Binary.utf8(kwargs['id_subscription'])
			if ("entry_type" in kwargs): self.local.db_instance.entry_type = kwargs['entry_type']
			if ("owner_type" in kwargs): self.local.db_instance.owner_type = kwargs['owner_type']
			if ("locked" in kwargs): self.local.db_instance.locked = kwargs['locked']
			if ("guest_permission" in kwargs): self.local.db_instance.guest_permission = kwargs['guest_permission']
			if ("user_permission" in kwargs): self.local.db_instance.user_permission = kwargs['user_permission']
		#
	#
#

##j## EOF