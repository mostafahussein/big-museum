import os

from flask import flash, jsonify, render_template, request, Blueprint
from werkzeug.utils import secure_filename

from app import app
from app.tasks import parse_xml


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['xml']

        if file and file.filename.rsplit(".", 1)[-1] == 'xml':
            filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(filename)
            task = parse_xml.apply_async(args=[filename])

            return render_template('info.html', task_id=task.id, filename=file.filename)
        else:
            flash("You have to upload only valid xml files")

    return render_template('index.html')


@views.route('/status/<task_id>', methods=['GET'])
def status(task_id):
    task = parse_xml.AsyncResult(task_id)
    response = {}
    message = 'Unknown error'

    if task.info:
        print(task.info)
        if task.info.get('status'):
            response.update({'current': task.info.get('current', 0), 'status': True})

            if 'fulness' in task.info:
                response['fulness'] = task.info['fulness']

            return jsonify(response)
        message = task.info.get('message', message)

    response.update({'status': False, 'message': message})

    return jsonify(response)
