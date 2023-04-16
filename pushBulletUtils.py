import ujson
import requests
import time



class PushBullet:
    def __init__(self) -> None:
        
        self.data2send = {
            "type": "note",
            "title": "Aquamate",
            "body": "",
        }
        self.API_KEY = 'o.EwoH9sQjYvGQYEL4G2xIoqi38NQfMLlq'

        self.pb_headers = {
            'Access-Token': self.API_KEY,
            'Content-Type': 'application/json',
            'Host': 'api.pushbullet.com'
        }
    def notify(self,custom_msg):
        self.data2send["body"] = custom_msg
        r = requests.post('https://api.pushbullet.com/v2/pushes', data=ujson.dumps(self.data2send), headers=self.pb_headers)


if __name__ == "__main__":
    pushbullet = PushBullet()
    pushbullet.notify("working\nok")