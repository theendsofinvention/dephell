# built-in
from datetime import datetime

# external
import attr
from cached_property import cached_property
from packaging.utils import canonicalize_name
from packaging.version import parse


@attr.s(hash=False, cmp=True)
class Release:
    dependencies = None

    raw_name = attr.ib(cmp=False)
    version = attr.ib(converter=parse, cmp=True)
    time = attr.ib(repr=False, hash=False)                              # upload_time
    python_constraint = attr.ib(default=None, repr=False, cmp=False)    # requires_python
    hashes = attr.ib(factory=tuple, repr=False, cmp=False)              # digests/sha256

    @classmethod
    def from_response(cls, name, version, info):
        latest = info[-1]
        return cls(
            raw_name=name,
            version=version,
            time=datetime.strptime(latest['upload_time'], '%Y-%m-%dT%H:%M:%S'),
            # python_constraint=latest['requires_python'],
            hashes=tuple(rel['digests']['sha256'] for rel in info),
        )

    @cached_property
    def name(self) -> str:
        return canonicalize_name(self.raw_name)

    def __str__(self):
        return '{name}=={version}'.format(name=self.raw_name, version=self.version)

    def hash(self):
        return hash((self.name, self.version))
