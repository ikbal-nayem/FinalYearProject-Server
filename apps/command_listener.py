import socketio
from apps.utils import ColorText
from apps.home.service import setEntryLog
from apps.authentication.models import Users
from CONF import MESSENGER_WEBHOOK

sio = socketio.Client()

print(ColorText.BOLD+'Connecting to webhook...'+ColorText.ENDC, end=" ")


@sio.event
def connect():
    print(ColorText.OKGREEN+'Connected'+ColorText.ENDC)


@sio.event
def connect_error(data):
    print(ColorText.FAIL+"Failed to connect webhook"+ColorText.ENDC)


@sio.on('command')
def on_command(data):
    print('Received command -'+ColorText.OKCYAN, data, ColorText.ENDC)
    sender_id = data.get('sender_id')
    command = data.get('command')
    admin = Users.query.filter_by(m_id=sender_id).first()
    print(admin)
    # if command == 'UNLOCK':
    #     setEntryLog(admin.id, "Unknown", 'Command', -1)


@sio.event
def disconnect():
    print(ColorText.WARNING+'Disconnected from webhook'+ColorText.ENDC)


sio.connect(MESSENGER_WEBHOOK, wait_timeout=10)
