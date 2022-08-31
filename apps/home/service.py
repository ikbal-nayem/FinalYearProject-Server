from apps import db
from .models import Members
from .util import saveDataset, updateDataset, deleteDataset


def getAllMembers():
  return Members.query.all()


def getMember(id):
  return Members.query.filter_by(id=id).first()


def createMember(request):
  m = Members(**request.form)
  db.session.add(m)
  print(m.id)
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
