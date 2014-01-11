from django.db import models

from uuid import UUID

class UUIDField(models.BinaryField, metaclass=models.SubfieldBase):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 16
        super().__init__(*args, **kwargs)
    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs
    def to_python(self, value):
        if not value or isinstance(value, UUID):
            return value
        return UUID(bytes=value)
    def get_prep_value(self, value):
        return super().get_prep_value(value.bytes)
