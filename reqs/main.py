

import requests
import asyncio


async def crawl(url):
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding
        print(resp.text)
        return resp.text
    except Exception as e:
        raise e
    finally:
        print(url)


async def main():
    url = "https://www.baidu.com"
    await crawl(url)
    return


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
