import feedparser
import requests
import html
import asyncio
from bs4 import BeautifulSoup
from aiogram import Bot
from datetime import datetime
from pytz import timezone, tzinfo
from Config.json import readJson, getURL

class RssParser:
    def __init__(self, bot: Bot) -> None:
        self.rss_url: str = getURL()
        self.dateFormat: str = "%a, %d %b %Y %H:%M:%S %z"
        self.lastDatePost: datetime = None
        self.bot: Bot = bot

    def checkLastDatePostIsNone(self) -> None:
        if self.lastDatePost is None:
            self.lastDatePost = datetime.strptime("Thu, 24 Oct 2024 13:36:39 +0300", self.dateFormat)
    
    def getStatusCode(self) -> int:
        return self.request.status_code
    
    def getCurrentTime(self) -> str:
        tz: tzinfo = timezone("Europe/Moscow")
        return datetime.now(tz=tz).strftime(self.dateFormat)
    
    def getEntries(self) -> None:
        self.request: requests.models.Response = requests.get(self.rss_url)
        if self.getStatusCode() == 200:
            self.feed: feedparser.util.FeedParserDict = feedparser.parse(self.request.content)
            
    def checkLastDatePost(self) -> bool:
        lastPubDate: str = self.feed.entries[0].published
        lastPubDate: datetime = datetime.strptime(lastPubDate, self.dateFormat)
        self.checkLastDatePostIsNone()
        if lastPubDate > self.lastDatePost:
            self.lastDatePost = lastPubDate
            return True
        else:
            return False
        
    async def sendMessage(self) -> None:
        datasub: dict = readJson()
        listUsers: list = datasub.get("listSubscription")
        dictText: dict = self.textFormatting()
        text: str = f"""
{dictText.get("titleEntry")}
{dictText.get("entryLink")}
{dictText.get("content")}
{dictText.get("publishedDate")}
"""
        for id in listUsers:
            await self.bot.send_photo(chat_id=id, photo=dictText.get("pictureLink"))
            maxLength = 4096
            while len(text) > maxLength:
                await self.bot.send_message(chat_id=id, text=text[:maxLength])
                text = text[maxLength:]
            await self.bot.send_message(chat_id=id, text=text)

    def textFormatting(self) -> dict:
        entry: dict = self.feed.get("entries")[0]
        titleEntry: str = html.unescape(entry.get("title"))
        entryLink: str = entry.get("links")[0].get("href")
        pictureLink: str = entry.get("links")[1].get("href")
        soup: BeautifulSoup = BeautifulSoup(entry.get("content")[0].get("value"), "html.parser")
        content: str = soup.get_text(separator='\n')
        publishedDate: str = entry.get("published")
        return {
            "titleEntry": titleEntry,
            "entryLink": entryLink,
            "pictureLink": pictureLink,
            "content": content,
            "publishedDate": publishedDate
        }
    
    async def asyncThread(self) -> None:
        i = 0
        while self.boolThread:
            i+=1
            print(i)
            self.getEntries()
            self.checkLastDatePostIsNone()
            if self.checkLastDatePost():
                await self.sendMessage()
            await asyncio.sleep(10)

    async def startAsync(self) -> None:
        self.boolThread: bool = True
        await self.asyncThread()

    def stopAsync(self) -> None:
        self.boolThread = False
