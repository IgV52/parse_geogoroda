from aiohttp import ClientSession
from bs4 import BeautifulSoup
from dataclasses import dataclass
from format import RegionUrl, format_line_region, format_line_city

@dataclass(slots=True, frozen=True)
class InfoParse:
    session: ClientSession
    url: str
    path: str | None = None
    region : RegionUrl | None = None

async def parse_main(data: InfoParse) -> list:
    url = _get_create_url({'url': data.url, 'path': data.path})
    async with data.session.get(url=url) as resp:
        html = await resp.text()
        info = _get_create_info(html, data)
        return info

def _get_create_info(html: str, data: InfoParse) -> list:
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('tbody')
    table_line = []
    format_line = _get_format_line(data.region)
    for line in table:
        line = format_line['func'](str(line.find('a')))
        if line:
            table_line.append(line)
    if data.region:
        return {'title': data.region.title, 'url': data.region.url, 'city': table_line}
    return table_line

def _get_format_line(region: RegionUrl) -> dict:
    if not region:
        return {'func': format_line_region}
    return {'func': format_line_city}

def _get_create_url(link: dict) -> str:
    match link:
        case {'url': url, 'path': None}:
            return url
        case {'url': url, 'path': path}:
            return url+path
        case _:
            raise ValueError(f'Invalid data: {link !r}')
