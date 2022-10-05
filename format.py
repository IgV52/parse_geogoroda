from dataclasses import dataclass
from typing import Literal

@dataclass(slots=True, frozen=True)
class RegionUrl:
    title: str
    url: str

def format_line_region(string: str) -> RegionUrl:
    string = ((string.strip("<a href=></a>-1\n")).replace('"', '')).split(">")
    if string[0]:
        return RegionUrl(title=string[1], url=string[0])

def format_line_city(string: str) -> dict[Literal["title"] | Literal["url"], str]:
    string = ((string.strip("<a href=></a>-1\n")).replace('"', '')).split(">")
    if string[0]:
        city = string[1]
        url = ((string[0].strip("/gorod")).split('-rossiya'))[0]
        return {'title': city, 'url': url}
