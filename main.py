from aiohttp import ClientSession
from constants import URL, URL_CITY
from parse import InfoParse, parse_main

import asyncio
import json
import os

async def main():
    parse = InfoParse(session=ClientSession(), url=URL)
    async with parse.session:
        info_region = await parse_main(parse)
        
        tasks = []
        for line in info_region:
            tasks.append(asyncio.create_task(parse_main(InfoParse(session=parse.session, url=URL_CITY, path=line.url, region=line))))
        info_city = await asyncio.gather(*tasks)
        
        final_info = []
        for line in info_city:
            final_info.append(line)

        basedir = os.path.abspath(os.path.dirname(__file__))
        os.makedirs('data', exist_ok=True)
        with open(os.path.join(basedir, 'data', 'data_file.json'), "w", encoding='utf8') as write_file:
            json.dump(final_info, write_file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    asyncio.run(main())