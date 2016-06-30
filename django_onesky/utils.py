# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import polib


def remove_fuzzy_translations(file_name):
    """
    This function removes the fuzzy translation strings + fuzzy flags by
    given translation file.

    :file_name string.
    """
    po_file = polib.pofile(file_name)
    for entry in po_file.fuzzy_entries():
        entry.msgstr = ''
        if entry.msgid_plural and isinstance(entry.msgstr_plural, dict):
            # Some languages (ru) have more than two plural forms.
            entry.msgstr_plural = {
                key: ''
                for key, val in entry.msgstr_plural.iteritems()
            }
        entry.flags.remove('fuzzy')
    po_file.save()
