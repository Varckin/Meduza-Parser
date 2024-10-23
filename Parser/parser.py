import feedparser
import requests
from bs4 import BeautifulSoup
from aiogram import Bot
from datetime import datetime
from pytz import timezone, tzinfo
from Config.json import readJson, getURL


class RssParser:
    def __init__(self, bot: Bot = None) -> None:
        self.rss_url: str = getURL
        self.dateFormat: str = "%a, %d %b %Y %H:%M:%S %z"
        self.lastDatePost: datetime = None
        self.bot: Bot = bot

        self.request: requests.models.Response = requests.get(self.rss_url)

    def checkLastDatePostIsNone(self) -> None:
        if self.lastDatePost is None:
            self.lastDatePost = datetime.strptime(self.getCurrentTime(), self.dateFormat)
    
    def getStatusCode(self) -> int:
        return self.request.status_code
    
    def getCurrentTime(self) -> str:
        tz: tzinfo = timezone("Europe/Moscow")
        return datetime.now(tz=tz).strftime(self.dateFormat)
    
    def getEntries(self) -> None:
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
        
    def sendMessage(self) -> None:
        datasub: dict = readJson()
        listUsers: list = datasub.get("listSubscription")
        dataDict: dict = {
            "title" : self.feed.get("title"),
            "link" : self.feed.get("link"),
            "published" : self.feed.get("published")
        }
    
    def threadfun(self) -> None:
        self.getEntries()
        self.checkLastDatePostIsNone()

        if self.checkLastDatePost:
            self.sendMessage()
