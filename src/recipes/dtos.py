from dataclasses import dataclass


@dataclass
class Example:
    id: str
    exception: Exception = None

    @property
    def success(self) -> bool:
        return self.exception is None

