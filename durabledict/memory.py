from __future__ import absolute_import, division, print_function

import six

from durabledict.base import DurableDict
from durabledict.encoding import NoOpEncoding


class MemoryDict(DurableDict):
    """
    Does not actually persist any data to a persistant storage.  Instead, keeps
    everything in memory.  This is really only useful for use in tests
    """

    def __init__(self, autosync=True, encoding=NoOpEncoding, *args, **kwargs):
        self.__storage = dict()
        self.__last_updated = 1

        super(MemoryDict, self).__init__(autosync, encoding, *args, **kwargs)

    def persist(self, key, val):
        self.__storage[key] = self.encoding.encode(val)
        self.__last_updated += 1

    def depersist(self, key):
        del self.__storage[key]
        self.__last_updated += 1

    def durables(self):
        encoded_tuples = six.iteritems(self.__storage)
        tuples = [(k, self.encoding.decode(v)) for k, v in encoded_tuples]
        return dict(tuples)

    def last_updated(self):
        return self.__last_updated

    def _setdefault(self, key, default=None):
        self.__last_updated += 1
        val = self.__storage.setdefault(key, self.encoding.encode(default))
        return self.encoding.decode(val)

    def _pop(self, key, default=None):
        self.__last_updated += 1

        if default:
            default = self.encoding.encode(default)

        val = self.__storage.pop(key, default)

        if val is None:
            raise KeyError

        return self.encoding.decode(val)
