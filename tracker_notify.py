import requests

TOKEN = "1318419631:AAFvLkBttHyGKUcn5n8jWua8V1_tZ-VsrMI"
URL = f'https://api.telegram.org/bot{TOKEN}/'
CHAT_ID = 822413069


def send_message(text, parse_mode=None):
    requests.post(URL + 'sendMessage', data={
        'chat_id': CHAT_ID,
        'text': text,
        'parse_mode': parse_mode
    })


if __name__ == '__main__':
    send_message('test')
