from apps import db
from flask_login import current_user
from apps.authentication.models import Users
from .models import Members, Configuration
from .util import saveDataset, updateDataset, deleteDataset


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
