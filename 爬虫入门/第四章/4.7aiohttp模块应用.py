import asyncio
import aiohttp
import csv
urls = [
    "https://www.cgwallpapers.com/wallpapers_free_wreoiux/wallpaper_christian_dimitrov_02_1920x1080.jpg",
    "https://www.cgwallpapers.com/wallpapers_free_wreoiux/wallpaper_paolo_giandoso_10_1920x1080.jpg",
    "https://www.cgwallpapers.com/wallpapers_free_wreoiux/wallpaper_pablo_carpio_17_1920x1080.jpg"
]

async def download(url):
    name = url.split("/")[-1]
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            with open(name,mode="wb") as f:
                f.write(await resp.content.read())


async def main():
    tasks = []
    for url in urls:
        tasks.append(download(url))

    await asyncio.gather(*tasks)


if __name__ =="__main__":
    asyncio.run(main())