import re


def _make_pattern(keys: list[str]) -> str:
    keys_joined = "|".join(keys)
    return fr"\n?:({keys_joined}):(.+)\n"


def parse_metadata(text: str, keys: list[str]) -> dict[str, str]:
    pattern = _make_pattern(keys)
    return {k.strip(): v.strip() for k, v in re.findall(pattern, text)}


def strip_metadata(text: str, keys: list[str]) -> str:
    pattern = _make_pattern(keys)
    return re.sub(pattern, "", text).strip()
