from apps.home import blueprint
import sqlalchemy
from flask import render_template, request, redirect, url_for
from flask_login import login_required
from algo.Training import startTraining, getTraningStatus
from .recognition_service import checkRequestImage, reloadModel, isModelTrained
from .forms import MemberInputForm
from .service import (
    createMember,
    getAllMembers,
    getMember, updateMember, deleteMember, updateProfile, getUseSettings,
    addOrUpdateSettings,
    getEntryLog,
    configureRpi
)


# ToDo:: Make user UUID


@blueprint.route('/dashboard')
@login_required
def dashboard():
    log, total_auto, total_command = getEntryLog()
    return render_template('home/dashboard.html', log=log, total_auto=total_auto, total_command=total_command, segment='dashboard')


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


@blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == "POST":
        updateProfile(request)
    return render_template('home/profile.html', training_status=getTraningStatus(), segment='profile')


@blueprint.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == "POST":
        conf = addOrUpdateSettings(request)
    else:
        conf = getUseSettings()
    return render_template('home/settings.html', conf=conf, segment='settings')


@blueprint.route('/configure-rpi', methods=['GET'])
@login_required
def configureRequest():
    return configureRpi()


# Image processing routes

@blueprint.route('/recognize', methods=['GET', 'POST'])
def recognition():
    if request.method == "POST":
        if request.form.get('user_id') or (request.get_json() and request.get_json().get('user_id', False)):
            return checkRequestImage(request)
        else:
            return ({"success": True, "message": "user_id was not provided."})
    return ({"success": True, "message": "Recognition server is running...", "has_trained": isModelTrained()})


@blueprint.route('/train', methods=['GET'])
def train():
    traning_status = getTraningStatus()
    if not traning_status.get('is_training'):
        training_res = startTraining()
        reloadModel()
        return ({'success': True, 'message': training_res if training_res else 'Training successfull'})
    return traning_status


@blueprint.route('/training-status', methods=['GET'])
def trainingStatus():
    return getTraningStatus()
