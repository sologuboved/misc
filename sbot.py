from slack import WebClient as SlackWebClient
from slack.errors import SlackApiError
from userinfo import SLACK_TOKEN


def send(message, url):
    client = SlackWebClient(token=SLACK_TOKEN)
    try:
        client.chat_postMessage(
            channel='tracebacks',
            text=message,
            icon_url=url
        )
    except SlackApiError as e:
        print(e)


if __name__ == '__main__':
    send("Hello World", 'https://shiparrt.com/wp-content/uploads/2020/12/Pequod-Preview.png')
