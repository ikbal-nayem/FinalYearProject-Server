from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps import db
from .forms import MemberInputForm
from .models import Members
from .util import saveDataset


@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index')


@blueprint.route('/home')
@login_required
def home():
    return render_template('home/dashboard.html', segment='home')


@blueprint.route('/members')
@login_required
def members():
    return render_template('home/members.html', segment='members')


@blueprint.route('/member-form', methods=['GET', 'POST'])
@login_required
def memberForm():
    member_inputs = MemberInputForm(request.form)
    if request.method == "POST":
        if request.files.get('dataset'):
            m = Members(**request.form)
            db.session.add(m)
            db.session.commit()
            saveDataset(request, m.id)
            return render_template('home/member-form.html', success=True, msg="Member information has been saved successfully.", form=member_inputs)
        else:
            return render_template('home/member-form.html', success=False, msg="Please provide dataset", form=member_inputs)
    else:
        return render_template('home/member-form.html', form=member_inputs)


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return None
