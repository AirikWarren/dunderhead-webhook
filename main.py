'''idk set this up as a cron job or something'''
from super_secret_shit import SLACK_WEBHOOK_URL, DISCORD_WEBHOOK_URL, INVITE_URL
import rss_parse

from datetime import datetime
import random

import requests
from slack_sdk.webhook import WebhookClient

greetings = [
    "Bonjour",
    "Hola",
    "Hello",
    "Good day"
]

group_title = [
    "dunderheads,",
    "dunders,",
]

pre_transition_phrases = [
    "hope you haven't broken too many codebases lately.",
    "hope you've been writing good docstrings.",
    "if you're reading this, you've learned to read since last we talked, I'm proud of you.",
    "I love you.",
    "have I ever told you how self-documenting your code is? No really, don't even bother writing docstrings.",
]

pre_transition_phrases.extend(
    ["" for x in range(len(pre_transition_phrases)*2)])

transition_phrases = [
    "Just stopped by to remind everybody that the",
    "Just a reminder that the",
    "Don't forget that the"
]


def send_message_to_discord_and_slack(message: str):
    slack_client = WebhookClient(SLACK_WEBHOOK_URL)
    r = slack_client.send(text=message)
    message = message.replace('*', '**')
    message = message.replace('_', '__')
    requests.post(
        url=DISCORD_WEBHOOK_URL,
        data={
            "content": message
        }
    )


def format_date(dt, include_time=True):
    def secs_to_mins(s): return (s // 60) % 60
    def secs_to_hours(s): return (s // 3600) % 24

    if isinstance(dt, datetime):
        return dt.strftime("%A, %B %d at %H:%M PM") if include_time else dt.strftime("%A, %-B %d")
    else:
        return f"{dt.days} Days, {secs_to_hours(dt.seconds)} Hours, and {secs_to_mins(dt.seconds)} Minutes from now"

if __name__ == '__main__':
    channel = rss_parse.extract_rss_channel_from_xml(
        'dunder.xml', ('title', 'description'))
    next_meeting_dt = rss_parse.extract_dates_from_channel(channel)[0]
    current_dt = datetime.now()
    delta_to_next_meet = next_meeting_dt - current_dt

    info_message = f"next meeting is on \n\n*{format_date(next_meeting_dt)}*\n_({format_date(delta_to_next_meet)} from now_)"
    greeting_message = f"{random.choice(greetings)} {random.choice(group_title)} {random.choice(pre_transition_phrases)}\n\n\n{random.choice(transition_phrases)}"

    send_message_to_discord_and_slack(
        f"\n\n{greeting_message} {info_message}\n\n The most up to date invite link is {INVITE_URL}")
