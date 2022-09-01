from apps.home import blueprint
import sqlalchemy
from flask import render_template, request, redirect, url_for
from flask_login import login_required
from jinja2 import TemplateNotFound
from algo.Recognition import Recognizer
from algo.Training import startTraining, getTraningStatus
from .forms import MemberInputForm
from .service import createMember, getAllMembers, getMember, updateMember, deleteMember


@blueprint.route('/home')
@blueprint.route('/dashboard')
@login_required
def home():
    return render_template('home/dashboard.html', segment='home')


@blueprint.route('/members')
@login_required
def members():
    members_list = getAllMembers()
    return render_template('home/members.html', members_list=members_list, segment='members')


@blueprint.route('/member-form/<member_id>/delete', methods=['POST'])
@login_required
def memberDelete(member_id):
    deleteMember(member_id)
    return redirect(url_for('home_blueprint.members'))


@blueprint.route('/member-form', methods=['GET', 'POST'])
@blueprint.route('/member-form/<member_id>', methods=['GET', 'POST'])
@login_required
def memberForm(member_id=None):
    if request.method == "POST":
        member_inputs = MemberInputForm(request.form)
        if member_id:
            updateMember(request, member_id)
            return redirect(url_for('home_blueprint.members'))
        if request.files.get('dataset'):
            m = createMember(request)
            return redirect(url_for('home_blueprint.members'))
        return render_template('home/member-form.html', success=False, msg="Please provide dataset", form=member_inputs)
    else:
        member_inputs = MemberInputForm()
        if member_id:
            try:
                member = getMember(member_id)
                member_inputs.first_name.default = member.first_name
                member_inputs.last_name.default = member.last_name
                member_inputs.gender.default = member.gender
                member_inputs.process()
            except sqlalchemy.exc.StatementError:
                return render_template('home/page-404.html'), 404
        return render_template('home/member-form.html', form=member_inputs, member_id=member_id)


# Image processing routes
print('Loading model...')
recognizer = Recognizer()


@blueprint.route('/recognize', methods=['GET', 'POST'])
def recognition():
    if request.method == "POST":
        if request.is_json:
            url = request.get_json().get('url', False)
            faces = recognizer.applyWithURL(url) if url else {
                'success': False, 'message': "Image url was not provid into 'url'"}
            return (faces)
        elif request.files:
            img = request.files.get('image', False)
            faces = recognizer.applyWithImg(img) if img else {
                'success': False, 'message': "Image file wasn't provided into 'image'"}
            return (faces)
        return ({'success': False, 'message': 'Request data should be in JSON format'})
    return ({"success": True, "message": "Recognition server is running...", "has_trained": recognizer.has_trained})


@blueprint.route('/train', methods=['GET'])
def train():
    traning_status = getTraningStatus()
    if not traning_status.get('is_training'):
        startTraining()
        recognizer.loadModel()
    else:
        return traning_status
    return ({'success': True, 'message': 'Training successful'})


@blueprint.route('/training-status', methods=['GET'])
def training_status():
    return getTraningStatus()


# @blueprint.route('/<template>')
# @login_required
# def route_template(template):

#     try:

#         if not template.endswith('.html'):
#             template += '.html'

#         # Detect the current page
#         segment = get_segment(request)

#         # Serve the file (if exists) from app/templates/home/FILE.html
#         return render_template("home/" + template, segment=segment)

#     except TemplateNotFound:
#         return render_template('home/page-404.html'), 404

#     except:
#         return render_template('home/page-500.html'), 500


# # Helper - Extract current page name from request
# def get_segment(request):
#     try:
#         segment = request.path.split('/')[-1]
#         if segment == '':
#             segment = 'index'
#         return segment
#     except:
#         return None
