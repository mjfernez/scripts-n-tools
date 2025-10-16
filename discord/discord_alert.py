#!/usr/bin/python3
# Example usage
# echo "Test Alert!" | python discord_alert.py https://url
# https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks

import sys
import requests
import argparse


def send_update(name, msg, discord_webhook):
    """ Send a push to discord webhook url"""
    formatted = f"⚠️ ALERT {name}\n\n{msg}"
    message = { 'content' : formatted }
    sys.stderr.write("Sending request.... ")
    r = requests.post(url=discord_webhook, data=message)
    sys.stderr.write(f"{r.status_code}\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--title", default="")
    parser.add_argument("url")
    args = parser.parse_args()

    if not args.url:
        sys.stderr.write("A webhook url is required\n")
        sys.stderr.write("Usage:\n\n")
        sys.stderr.write("python discord_alert.py [-t] <title> <url>\n")
        sys.exit(1)

    msg = ""
    line = input()
    while line:
        msg += line
        try:
            line = input()
        except EOFError:
            break
    send_update(args.title, msg, args.url)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("User stopped program\n")
        sys.exit(0)

