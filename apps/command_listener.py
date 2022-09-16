import socketio
import requests
from datetime import datetime
from sqlalchemy import create_engine
from apps.utils import ColorText
from apps.authentication.models import Users
from apps.config import Config
from apps.messenger import MessageTemplate
from CONF import MESSENGER_WEBHOOK

sio = socketio.Client()
eng = create_engine(Config().SQLALCHEMY_DATABASE_URI)

@sio.event
def connect():
    print(ColorText.OKGREEN+'Webhook connected'+ColorText.ENDC)


@sio.event
def connect_error(data):
    print(ColorText.FAIL+"Failed to connect webhook"+ColorText.ENDC)


@sio.on('command')
def on_command(data):
    print('Received command -'+ColorText.OKCYAN, data, ColorText.ENDC)
    sender_id = data.get('sender_id')
    command = data.get('command')
    msgTemplate = MessageTemplate(sender_id)
    conn = eng.connect()
    admin = conn.exec_driver_sql(
        f"select id from Users where m_id={sender_id}").first()
    if admin and len(admin):
        msgTemplate.text("Command has been received :D")
        rpi = conn.exec_driver_sql(
            f"select rpi_ip from Configuration where user_id={admin[0]}").first()
        if command == 'UNLOCK':
            conn.exec_driver_sql(
                f"INSERT INTO EntryLog (user_id, entry_time, confidance_level, member, access_type) VALUES ({admin[0]}, '{datetime.now()}', {-1}, 'Unknown', 'Command')")
            # Do something after save the log
            requests.get(f"http://{rpi[0]}:5001/command/OPEN")
        elif command == 'ALARM':
            requests.get(f"http://{rpi[0]}:5001/command/ALARM")
    else:
        print(ColorText.UNDERLINE+"No admin found!"+ColorText.ENDC)
        msgTemplate.text("Could not find your account :(")


@sio.event
def disconnect():
    print(ColorText.WARNING+'Webhook disconnected'+ColorText.ENDC)


sio.connect(MESSENGER_WEBHOOK, wait_timeout=7)
