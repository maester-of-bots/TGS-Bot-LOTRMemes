import praw
import os
from dotenv import load_dotenv

clonedir = 'clones/Prod/'

files = os.listdir(clonedir)

bots = []

for file in files:
    path = os.path.join(clonedir, file)
    bots.append(file)

load_dotenv()


config = {
    "Frodo-B-Bot_": {
            "reddit": praw.Reddit(
                        client_id=os.getenv("frodo_client_id"),
                        client_secret=os.getenv("frodo_client_secret"),
                        password=os.getenv("frodo_password"),
                        user_agent=os.getenv("frodo_user_agent"),
                        username=os.getenv("frodo_username")
                    ),
            "webhook": os.getenv("frodo_webhook"),
            "keywords": ["frodo"],
            "subs": "FreeFolkSimulator",
            "db": "frodo_comments",
            "quotes": open(clonedir+'Frodo-B-Bot_.txt','r', encoding='UTF-8').readlines()
            },

    "Galadriel-Bot_": {
            "reddit": praw.Reddit(
                        client_id=os.getenv("galadriel_client_id"),
                        client_secret=os.getenv("galadriel_client_secret"),
                        password=os.getenv("galadriel_password"),
                        user_agent=os.getenv("galadriel_user_agent"),
                        username=os.getenv("galadriel_username")
                    ),
            "webhook": os.getenv("galadriel_webhook"),
            "keywords": ["galadriel"],
            "subs": "FreeFolkSimulator",
            "db": "galadriel_comments",
            "quotes": open(clonedir+'Galadriel-Bot_.txt','r', encoding='UTF-8').readlines()
            },

    "Legolas-Bot_": {
            "reddit": praw.Reddit(
                        client_id=os.getenv("legolas_client_id"),
                        client_secret=os.getenv("legolas_client_secret"),
                        password=os.getenv("legolas_password"),
                        user_agent=os.getenv("legolas_user_agent"),
                        username=os.getenv("legolas_username")
                    ),
            "webhook": os.getenv("legolas_webhook"),
            "keywords": ["legolas"],
            "subs": "FreeFolkSimulator",
            "db": "legolas_comments",
            "quotes": open(clonedir+'Legolas-Bot_.txt','r', encoding='UTF-8').readlines()
            },

    "Sammy-G-Bot_": {
            "reddit": praw.Reddit(
                        client_id=os.getenv("sam_client_id"),
                        client_secret=os.getenv("sam_client_secret"),
                        password=os.getenv("sam_password"),
                        user_agent=os.getenv("sam_user_agent"),
                        username=os.getenv("sam_username")
                    ),
            "webhook": os.getenv("sam_webhook"),
            "keywords": ["samwise","potatoes"],
            "subs": "FreeFolkSimulator",
            "db": "sam_comments",
            "quotes": open(clonedir+'Sammy-G-Bot_.txt','r', encoding='UTF-8').readlines()
            },

    "Pippy-T-Bot_": {
            "reddit": praw.Reddit(
                        client_id=os.getenv("pippin_client_id"),
                        client_secret=os.getenv("pippin_client_secret"),
                        password=os.getenv("pippin_password"),
                        user_agent=os.getenv("pippin_user_agent"),
                        username=os.getenv("pippin_username")
                    ),
            "webhook": os.getenv("pippin_webhook"),
            "keywords": ["pippin"],
            "subs": "FreeFolkSimulator+lotrmemes",
            "db": "pippin_comments",
            "quotes": open(clonedir+'Pippy-T-Bot_.txt','r', encoding='UTF-8').readlines()
            },

    "Merry-B-Bot_": {
            "reddit": praw.Reddit(
                        client_id=os.getenv("merry_client_id"),
                        client_secret=os.getenv("merry_client_secret"),
                        password=os.getenv("merry_password"),
                        user_agent=os.getenv("merry_user_agent"),
                        username=os.getenv("merry_username")
                    ),
            "webhook": os.getenv("merry_webhook"),
            "keywords": ["merry","meriadoc", "brandybuck"],
            "subs": "FreeFolkSimulator+lotrmemes",
            "db": "merry_comments",
            "quotes": open(clonedir+'Merry-B-Bot_.txt','r', encoding='UTF-8').readlines()
            },
}