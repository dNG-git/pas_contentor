# -*- coding: utf-8 -*-

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
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;gpl
----------------------------------------------------------------------------
#echo(pasContentorVersion)#
#echo(__FILEPATH__)#
"""

from time import time

from dNG.data.binary import Binary
from dNG.data.data_linker import DataLinker
from dNG.data.ownable_mixin import OwnableMixin as OwnableInstance
from dNG.data.ownable_lockable_read_mixin import OwnableLockableReadMixin
from dNG.database.instances.contentor_document import ContentorDocument as _DbContentorDocument
from dNG.database.instances.text_entry import TextEntry as _DbTextEntry
from dNG.database.lockable_mixin import LockableMixin
from dNG.database.sort_definition import SortDefinition

from .category import Category

class Document(DataLinker, LockableMixin, OwnableLockableReadMixin):
    """
"Document" represents a contentor entry.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: contentor
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
    """

    _DB_INSTANCE_CLASS = _DbContentorDocument
    """
SQLAlchemy database instance class to initialize for new instances.
    """

    def __init__(self, db_instance = None):
        """
Constructor __init__(Document)

:param db_instance: Encapsulated SQLAlchemy database instance

:since: v0.2.00
        """

        DataLinker.__init__(self, db_instance)
        LockableMixin.__init__(self)
        OwnableLockableReadMixin.__init__(self)

        self.set_max_inherited_permissions(OwnableLockableReadMixin.READABLE,
                                           OwnableLockableReadMixin.READABLE
                                          )
    #

    def delete(self):
        """
Deletes this entry from the database.

:since: v0.2.00
        """

        if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.delete()- (#echo(__LINE__)#)", self, context = "pas_datalinker")

        with self:
            db_text_entry_instance = self.local.db_instance.rel_text_entry

            DataLinker.delete(self)
            if (db_text_entry_instance is not None): self.local.connection.delete(db_text_entry_instance)
        #
    #

    def _get_default_sort_definition(self, context = None):
        """
Returns the default sort definition list.

:param context: Sort definition context

:return: (object) Sort definition
:since:  v0.2.00
        """

        if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}._get_default_sort_definition({1})- (#echo(__LINE__)#)", self, context, context = "pas_datalinker")

        return (DataLinker._get_default_sort_definition(self, context)
                if (context == "DataLinker") else
                SortDefinition([ ( "position", SortDefinition.ASCENDING ),
                                 ( "title", SortDefinition.ASCENDING )
                               ])
               )
    #

    def _get_unknown_data_attribute(self, attribute):
        """
Returns the data for the requested attribute not defined for this instance.

:param attribute: Requested attribute

:return: (dict) Value for the requested attribute
:since:  v0.2.00
        """

        if (attribute == "content" and self.local.db_instance.rel_text_entry is not None): _return = self.local.db_instance.rel_text_entry.content
        else: _return = DataLinker._get_unknown_data_attribute(self, attribute)

        return _return
    #

    def _insert(self):
        """
Insert the instance into the database.

:since: v0.2.00
        """

        with self.local.connection.no_autoflush:
            DataLinker._insert(self)

            if (self.local.db_instance.time_published is None): self.local.db_instance.time_published = int(time())

            is_acl_missing = (len(self.local.db_instance.rel_acl) == 0)
            is_data_missing = self.is_data_attribute_none("owner_type", "entry_type")
            is_permission_missing = self.is_data_attribute_none("guest_permission", "user_permission")

            parent_object = (self.load_parent() if (is_acl_missing or is_data_missing or is_permission_missing) else None)

            if (is_data_missing and (isinstance(parent_object, Category) or isinstance(parent_object, Document))):
                parent_data = parent_object.get_data_attributes("id_site", "entry_type")

                if (self.local.db_instance.id_site is None and parent_data['id_site'] is not None): self.local.db_instance.id_site = parent_data['id_site']
                if (self.local.db_instance.entry_type is None): self.local.db_instance.entry_type = parent_data['entry_type']
            #

            if (isinstance(parent_object, OwnableInstance)):
                if (is_acl_missing): self._copy_acl_entries_from_instance(parent_object)
                if (is_permission_missing): self._copy_default_permission_settings_from_instance(parent_object)
            #
        #
    #

    def set_data_attributes(self, **kwargs):
        """
Sets values given as keyword arguments to this method.

:since: v0.2.00
        """

        with self, self.local.connection.no_autoflush:
            DataLinker.set_data_attributes(self, **kwargs)

            if ("entry_type" in kwargs): self.local.db_instance.entry_type = kwargs['entry_type']
            if ("owner_type" in kwargs): self.local.db_instance.owner_type = kwargs['owner_type']
            if ("author_id" in kwargs): self.local.db_instance.author_id = kwargs['author_id']
            if ("author_ip" in kwargs): self.local.db_instance.author_ip = kwargs['author_ip']
            if ("time_published" in kwargs): self.local.db_instance.time_published = int(kwargs['time_published'])
            if ("description" in kwargs): self.local.db_instance.description = Binary.utf8(kwargs['description'])
            if ("locked" in kwargs): self.local.db_instance.locked = kwargs['locked']
            if ("guest_permission" in kwargs): self.local.db_instance.guest_permission = kwargs['guest_permission']
            if ("user_permission" in kwargs): self.local.db_instance.user_permission = kwargs['user_permission']

            if ("content" in kwargs):
                if (self.local.db_instance.rel_text_entry is None):
                    self.local.db_instance.rel_text_entry = _DbTextEntry()
                    self.local.db_instance.rel_text_entry.id = self.local.db_instance.id
                    db_text_entry = self.local.db_instance.rel_text_entry
                else: db_text_entry = self.local.db_instance.rel_text_entry

                db_text_entry.content = Binary.utf8(kwargs['content'])
            #
        #
    #
#
