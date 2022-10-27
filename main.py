from datetime import *
from random import *
from time import sleep

import requests

from sql import *
import praw
from bot_brains import *

def submissions_and_comments(subreddit, **kwargs):
    results = []
    results.extend(subreddit.new(**kwargs))
    results.extend(subreddit.comments(**kwargs))
    results.sort(key=lambda post: post.created_utc, reverse=True)
    return results



class BOTMOB:
    def __init__(self):
        # Import config from config file, this houses everything needed for each bot.
        self.bots = config

        # Import config for Vizzy.  Using Vizzy as the default account to crawl r/freefolksimulator
        load_dotenv()
        self.bofh_webhook = os.getenv('bofh_webhook')
        self.reddit = praw.Reddit(
                    client_id=os.getenv("vizzy_client_id"),
                    client_secret=os.getenv("vizzy_client_secret"),
                    password=os.getenv("vizzy_password"),
                    user_agent=os.getenv("vizzy_user_agent"),
                    username=os.getenv("vizzy_username"))

        # Set the subreddit to monitor
        self.subreddit = self.reddit.subreddit('FreeFolkSimulator+lotrmemes')

        self.stream = praw.models.util.stream_generator(lambda **kwargs: submissions_and_comments(self.subreddit, **kwargs))

        self.muted = {}

        # Hold on to yo butts
        self.run()

    def send_webhook(self, url, body, username):
        """Use webhooks to notify admin on Discord"""
        data = {'content': body, 'username': username}
        requests.post(url, data=data)

    def fight_it_out_boys(self, obj):
        skip = False
        if isinstance(obj,praw.models.Submission):
            smh = "post"
            to_check = obj.title.lower() + "\n" + obj.selftext.lower()
            if obj.link_flair_text == "fuck off bots":
                skip = True
        else:
            to_check = obj.body.lower()
            smh = "comment"

        if not skip:
            # Record the comment ID
            id = obj.id

            # Skip the comment if author doesn't exist
            if obj.author == None:
                pass
            else:
                upcount = False
                # Iterate through all the bots.  This allows us to easily add in bots without changing the main code.
                for bot in self.bots:
                    if bot == str(obj.author):
                        pass
                    elif bot in self.muted.keys():
                        if datetime.now() >= (self.muted[bot] + timedelta(minutes=10)):
                            # Let the bot out of jail
                            self.muted.pop(bot)
                            self.send_webhook(self.bots[bot]['webhook'], "Bot has been let out of jail.", bot)
                        else:
                            # link = f"\n{obj.author.name}: {to_check}\nResponse: Bot is rate-limited and in jail.\nLink - https://www.reddit.com{obj.permalink}"
                            # https://discord.gg/ne8bsgEBct
                            # self.send_webhook(self.bots[bot]['webhook'], link, bot)
                            continue

                    if bot in self.muted.keys():
                        pass
                    else:
                        # Load in the comment using the stored Reddit instance specific to each bot.  Without this, Vizzy T will make all comments.
                        if smh == "comment":
                            bot_obj = self.bots[bot]['reddit'].comment(id=id)
                        else:
                            bot_obj = self.bots[bot]['reddit'].submission(id=id)



                        # Run through bot keywords
                        for quote in self.bots[bot]['keywords']:
                            # Load in all comments that have been responded to from the database
                            readComments = getComments(self.bots[bot]['db'])

                            # Prevents double-commenting for multiple trigger words
                            if bot_obj.id in readComments:
                                pass
                            else:
                                try:
                                    if quote in to_check:
                                        # Get a random number based on how many quotes there are
                                        num = randint(0, len(self.bots[bot]['quotes']) - 1)

                                        # Grab the associated response from bot quotes
                                        response = self.bots[bot]['quotes'][num]

                                        # Splice in Reddit username if relevant
                                        if "{}" in response:
                                            try:
                                                response = response.format(bot_obj.author.name)
                                            except:
                                                # Surely there's a better way...
                                                response = response.format(bot_obj.author.name,bot_obj.author.name)

                                        # Reply to the comment
                                        bot_obj.reply(body=response)

                                        if upcount == False:
                                            # Upvote the comment
                                            bot_obj.upvote()
                                            upcount = True
                                        # Write comment to SQL database for the bot
                                        writeComment(bot_obj.id,self.bots[bot]['db'])

                                        # Formulate a message to send via WebHooks
                                        link = f"\n{bot_obj.author.name}: {to_check}\nResponse: **'{response}'** \nLink - https://www.reddit.com{bot_obj.permalink}"

                                        # Send webhook to FreeFolk Simulator Discord
                                        # https://discord.gg/ne8bsgEBct
                                        self.send_webhook(self.bots[bot]['webhook'], link, bot)
                                except Exception as e:
                                    if "RATELIMIT" in str(e) or "ratelimit" in str(e):
                                        print("Rate-limited.")
                                        self.muted[bot] = datetime.now()
                                        self.send_webhook(self.bofh_webhook, f"{bot} has been placed in Reddit Jail.", "Resident BOFH")
                                    else:
                                        print("Other Error.")
                                        link = F'ERROR - {e}\nLink - https://www.reddit.com{bot_obj.permalink}'
                                        self.send_webhook(self.bots[bot]['webhook'], link, bot)

    def run(self):
        print("Bot mob is online.")
        # Iterate through comments in r/freefolksimulator
        for obj in self.stream:
            # Run comment through function above to determine if a bot should respond.
            self.fight_it_out_boys(obj)

        # Let HealthChecks know we're online
        requests.get('https://hc-ping.com/fb8ac673-1079-4928-9f35-f9c426afc286')

BOTMOBBBB = BOTMOB()
