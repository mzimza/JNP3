from django.core.cache import cache
from django.db.models import Model
import json


class CachingModel(Model):

	class Meta:
		abstract = True

	_prefix = "CM_"

	def __make_cache_key(self):
		return self._prefix + str(self.id)

	@classmethod
	def __make_cache_key_c(cls, id_key):
		return cls._prefix + str(id_key)

	def __cache_set(self):
		return _set(self.__make_cache_key(), self)

	@classmethod
	def __cache_get(cls, **kwargs):
		obj = get(cls.__make_cache_key_c(kwargs['id']), cls.objects.get, **kwargs)
		return obj

	def __cache_remove(self):
		return remove(self.__make_cache_key())

	@classmethod
	def get(cls, *args, **kwargs):
		if 'id' in kwargs:
			return cls.__cache_get(**kwargs)
		return cls.objects.get(*args, **kwargs)

	def save(self, *args, **kwargs):
		ret = super(CachingModel, self).save(*args, **kwargs)
		self.__cache_set()
		return ret

	def delete(self, *args, **kwargs):
		tmp_id = self.id
		ret = super(CachingModel, self).delete(*args, **kwargs)
		self.id = tmp_id
		self.__cache_remove()
		self.id = None
		return ret

	@classmethod
	def from_dict(cls, **kwargs):
		return cls(**kwargs)


def date_handler(obj):
	return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def get(name, to_evaluate, *args, **kwargs):
	return_val = cache.get(name)
	if return_val is None:
		return_val = to_evaluate(*args, **kwargs)
		cache.set(name, return_val.serializer.data, 60)
		return return_val.to_dict()
	else:
		return return_val


def _set(name, value):
	cache.set(name, value.serializer.data)


def set(name, value):
	cache.set(name, value)


def remove(name):
	cache.delete(name)