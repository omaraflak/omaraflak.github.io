import re
import datetime
import dataclasses


@dataclasses.dataclass
class Metadata:
    _KEYS = ["title", "description", "year", "month", "day"]

    metadata: dict[str, str]

    @property
    def title(self) -> str:
        return self.metadata["title"]

    @property
    def description(self) -> str:
        return self.metadata["description"]

    @property
    def year(self) -> int:
        return int(self.metadata["year"])

    @property
    def month(self) -> int:
        return int(self.metadata["month"])

    @property
    def day(self) -> int:
        return int(self.metadata["day"])

    @property
    def date(self) -> datetime.date:
        return datetime.date(self.year, self.month, self.day)


def _make_pattern() -> str:
    keys_joined = "|".join(Metadata._KEYS)
    return f"\n?:({keys_joined}):(.+)\n"


def parse_metadata(text: str) -> Metadata:
    metadata = {
        k.strip(): v.strip()
        for k, v in re.findall(_make_pattern(), text)
    }
    return Metadata(metadata)


def strip_metadata(text: str) -> str:
    return re.sub(_make_pattern(), "", text).strip()
