from flask import jsonify
from apps import db
import requests
from sqlalchemy import func
from datetime import date
from flask_login import current_user
from subprocess import check_output
from apps.authentication.models import Users
from .models import Members, Configuration, EntryLog
from .util import saveDataset, updateDataset, deleteDataset


current_ip = check_output(['hostname', '-I']).decode().strip()

def getAllMembers():
    return Members.query.filter_by(user_id=current_user.id).all()


def getMember(id):
    return Members.query.filter_by(id=id).first()


def createMember(request):
    m = Members(**request.form)
    m.user_id = current_user.id
    db.session.add(m)
    db.session.commit()
    m.number_of_dataset = saveDataset(request, m.id)
    db.session.commit()
    return m


def updateMember(request, member_id):
    member = Members.query.filter_by(id=member_id).first()
    member.first_name = request.form.get('first_name')
    member.last_name = request.form.get('last_name')
    member.gender = request.form.get('gender')
    if request.files.get('dataset'):
        member.number_of_dataset = updateDataset(request, member_id)
    db.session.commit()
    return member


def deleteMember(member_id):
    member = Members.query.filter_by(id=member_id).first()
    deleteDataset(member.id)
    db.session.delete(member)
    db.session.commit()


def updateProfile(request):
    user = Users.query.filter_by(id=current_user.id).first()
    user.email = request.form.get('email')
    user.m_id = request.form.get('m_id')
    db.session.commit()
    return user


def getUseSettings():
    return Configuration.query.filter_by(id=current_user.id).first()


def configureRpi():
    config = Configuration.query.filter_by(id=current_user.id).first()
    if config and config.rpi_ip:
        req_data = {"server_url": f"http://{current_ip}:5000/recognize",
                    "user_id": current_user.id}
        res = requests.post(f"http://{config.rpi_ip}:5001/configure",
                            json=req_data)
        if res.status_code == 200:
            return res.json()
        return jsonify({"success": False, "message": "Something went wrong configuring your device"})
    return jsonify({"success": False, "message": "Please provide configuration first"})


def addOrUpdateSettings(request):
    config = Configuration.query.filter_by(id=current_user.id).first()
    if not config:
        config = Configuration(**request.form)
        config.user_id = current_user.id
        db.session.add(config)
    else:
        config.rpi_ip = request.form.get('rpi_ip')
        config.rpi_username = request.form.get('rpi_username')
        config.rpi_password = request.form.get('rpi_password')
    db.session.commit()
    return config


# Setting member entry log
def setEntryLog(user_id, member, access_type, confidance=None):
    log = EntryLog(user_id=user_id, member=member, confidance_level=confidance,
                   access_type=access_type)
    db.session.add(log)
    db.session.commit()


def getEntryLog():
    entry_log = EntryLog.query.filter_by(
        user_id=current_user.id).order_by(EntryLog.entry_time.desc())
    total_auto = entry_log.filter(EntryLog.access_type == 'Auto', func.date(
        EntryLog.entry_time) == date.today()).all()
    total_command = entry_log.filter(EntryLog.access_type == 'Command', func.date(
        EntryLog.entry_time) == date.today()).all()

    return entry_log.all(), total_auto, total_command
