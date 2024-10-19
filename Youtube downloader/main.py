from pytubefix import Playlist, YouTube
from tkinter import filedialog
from time import sleep as wait
import tkinter as tk
import asyncio
import os

def saveAs() -> os.path:
    root = tk.Tk()
    root.withdraw()
    root.title = "Save as"
    return filedialog.askdirectory()

def clearScreen() -> None:
    os.system("cls")

PlaylistUrls = "Youtube downloader\\PlaylistLinks.txt"

async def download_video(videoURL: str, pathToDownload: str, plist: Playlist, vcurrent_queue: int, errs: int):
    try:
        yt = YouTube(url=videoURL, client="WEB", use_po_token=True)
        video = yt.streams.filter(progressive=True, file_extension="mp4").get_highest_resolution()
        print(f"• Downloading: {video.title} ({vcurrent_queue}/{plist.length})")
        video.download(f"{pathToDownload}/{plist.title}/")
        print(f"✓ - Downloaded: {video.title}")
    except Exception as error:
        print(f"✘ - There was an error downloading: {video.title}\nError: {error}")
        errs += 1
        print("Downloading next video in:  ", end="", flush=True)

        for i in range(5, 0, -1):
            print(f"\b{i}", end="", flush=True)
            wait(1)

async def download_playlist(PURL, pathToDownload, pcurrent_queue, lines, errs):
    try:
        p = Playlist(PURL.strip())
    except Exception as error:
        print(f"There was an error collecting playlist N°: {i}\nError: {error}")
        errs += 1
        return

    clearScreen()
    print(f"Downloading: {p.title} (Queue: {pcurrent_queue}/{len(lines)})")

    tasks = []
    for j, videoURL in enumerate(p.video_urls, start=1):
        task = download_video(videoURL, pathToDownload, p, pcurrent_queue, errs)
        tasks.append(task)

    await asyncio.gather(*tasks)

    clearScreen()
    print(f"Playlist downloaded: {p.title}")

async def main():
    i = errs = 0

    with open(PlaylistUrls, "r") as f:
        lines = f.readlines()
        pathToDownload = f"{saveAs()}"

        tasks = []
        for i, PURL in enumerate(lines, start=1):
            task = download_playlist(PURL, pathToDownload, i, lines, errs)
            tasks.append(task)

        await asyncio.gather(*tasks)

    clearScreen()
    print(f"All playlists were downloaded\nTotal errors: {errs}")

if __name__ == "__main__":
    asyncio.run(main())