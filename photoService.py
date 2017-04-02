from abc import ABCMeta, abstractmethod


class PhotoService:
    __metaclass__ = ABCMeta

    @abstractmethod
    def photo_lookup(self, tag_set, tags_intersect=False):
        pass

    @abstractmethod
    def get_next_photo(self):
        pass