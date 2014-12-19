class TagsSet:
    def __init__(self, src=[], exclude=[]):
        if isinstance(src, TagsSet):
            self._include = set(src._include)
            self._exclude = set(src._exclude)
        else:
            include = set(src)
            exclude = set(exclude)
            inter = include & exclude
            self._include = include - inter
            self._exclude = exclude

    @classmethod
    def from_string(cls, s, sep='|', neg='~'):
        values = s.split(sep)
        inc_values = (v for v in values if not v.startswith(neg))
        exc_values = (v[len(neg):] for v in values if v.startswith(neg))
        return cls(inc_values, exc_values)

    def __str__(self):
        values = [str(v) for v in self._include]
        values += ['~{}'.format(v) for v in self._exclude]
        return '|'.join(values)

    def __repr__(self):
        return '{}({}, {})'.format(self.__class__.__qualname__,
                                   repr(self._include),
                                   repr(self._exclude))

    def add(self, value):
        self._include.add(value)
        if value in self._exclude:
            self._exclude.remove(value)

    def exclude(self, value):
        self._exclude.add(value)
        if value in self._include:
            self._include.remove(value)

    def remove(self, value):
        if value in self._include:
            self._include.remove(value)
        if value in self._exclude:
            self._exclude.remove(value)

    def clear(self):
        self._include.clear()
        self._exclude.clear()

    def __iter__(self):
        return iter(self._include)

    def iter_exclude(self):
        return iter(self._exclude)
