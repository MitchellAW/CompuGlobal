from dataclasses import dataclass

from .client import CompuGlobalAPIClient
from .config import CompuGlobalAPIConfig


@dataclass
class EndpointBase:
    client: CompuGlobalAPIClient
    config: CompuGlobalAPIConfig

    def _get_public_methods(self):
        for attr_name in dir(self):
            if attr_name.startswith("_"):
                continue

            attr = getattr(self, attr_name)

            if callable(attr):
                yield attr_name, attr
