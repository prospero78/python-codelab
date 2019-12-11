import asyncio
import aiohttp
from flags import save_flag, show, main, BASE_URL


async def get_flag(session, cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    async with session.get(url) as response:
        return await response.read()


async def download_one(cc):
    async with aiohttp.ClientSession() as session:
        image = await get_flag(session, cc)
        show(cc)
        save_flag(image, cc.lower() + '.gif')
    return cc


def download_many(cc_list):
    loop = asyncio.get_event_loop()
    to_do = [download_one(cc) for cc in sorted(cc_list)]
    wait_coro = asyncio.wait(to_do)
    res, _ = loop.run_until_complete(wait_coro)
    loop.close()
    return len(res)


if __name__ == '__main__':
    main(download_many)