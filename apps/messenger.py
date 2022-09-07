import requests
import os


class MessageTemplate():
    def __init__(self, sender_id):
        self.sender_id = sender_id
        self.send_url = "https://graph.facebook.com/v14.0/me/messages?access_token={}".format(
            os.getenv('BOT_TOKEN'))
        # self._getUserInfo()

    def send(self, msg):
        resp = requests.post(self.send_url, json=msg).json()
        if resp.get('error'):
            print(resp['error'])
        return resp

    def text(self, msg):
        message = {
            "recipient": {"id": self.sender_id},
            "message": {"text": msg}
        }
        return self.send(message)

    def button(self, text, buttons=[]):
        button_list = [{
            "type": "postback",
            "title": btn['title'],
            "payload": btn.get('payload', 'DEVELOPER_DEFINED_PAYLOAD')
        } for btn in buttons]
        temp = {
            "recipient": {"id": self.sender_id},
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                            "template_type": "button",
                            "text": text,
                            "buttons": button_list
                    }
                }
            }
        }
        return self.send(temp)

    def generic(self, title=None, subtitle=None, url=None, image_url=None, buttons=[]):
        button_list = [{
            "type": btn.get("type", "postback"),
            "title": btn['title'],
            "payload": btn.get('payload', 'DEVELOPER_DEFINED_PAYLOAD')
        } for btn in buttons]

        temp = {
            "recipient": {"id": self.sender_id},
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                            "template_type": "generic",
                            "elements": [{
                                "title": title,
                                "image_url": image_url,
                                "subtitle": subtitle,
                                "default_action": {
                                    "type": "web_url",
                                    "url": url or image_url,
                                    "webview_height_ratio": "tall",
                                },
                                "buttons": button_list
                            }]}
                }
            }
        }
        return self.send(temp)
