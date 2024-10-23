from json import load, dump
from pathlib import Path

currentPath: str = f"{str(Path.cwd())}/Config/config.json"

def actionsub(idUser: int, action: str) -> str:
        data: dict = readJson()
        listSub: list = data.get("listSubscription")
        if action == "add":
            if idUser not in listSub:
                listSub.append(idUser)
                writeJson(data=data)
                return "Подписка активирована! Ое :)"
            else:
                return "Вы уже и так подписаны!"
        
        elif action == "del":
            if idUser in listSub:
                listSub.remove(idUser)
                writeJson(data=data)
                return "Подписка деактивирована! Печалька :("
            else:
                return "От чего отписаться, если и так не от чего. подпишись и будет тебе счастье :)"

def getToken() -> str:
    return readJson().get("token")

def getURL() -> str:
    return readJson().get("URLparser")
    
def readJson() -> dict:
    with open(file=currentPath, mode="r", encoding="utf-8") as file:
        return load(fp=file)

def writeJson(data: dict) -> None:
    with open(file=currentPath, mode="w", encoding="utf-8") as file:
        dump(obj=data, fp=file, ensure_ascii=False, indent=4)
