from flask import Blueprint, render_template, request, redirect, url_for, flash
import os
import os.path
import datetime
from werkzeug.utils import secure_filename

exampleapp_bp = Blueprint('exampleapp_bp', __name__)
UPLOAD_FOLDER = "static/files"


@exampleapp_bp.route("/secondpage/")
@exampleapp_bp.route("/secondpage")
def second_page_index():
    return render_template("second_page.html", submenu=1)


@exampleapp_bp.route('/upload', methods=['GET', 'POST'])
def second_page_upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            if not os.path.isfile(UPLOAD_FOLDER+"/"+filename):
                file.save(os.path.join(UPLOAD_FOLDER, filename))
            else:
                filename = str(datetime.datetime.now())[:-7].replace(" ", "-") + filename
                file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('exampleapp_bp.second_page_files'))
    return render_template("upload.html", submenu=1)


@exampleapp_bp.route("/files")
def second_page_files():
    out = ""
    first = []
    for path, subdirs, files in os.walk(UPLOAD_FOLDER):
        for name in sorted(files, key=lambda name: os.path.getmtime(os.path.join(path, name))):
            first.append(name)
    for i in reversed(first):
        out += '<a href="{0}/{1}">{1}</a><br>'.format(UPLOAD_FOLDER, i)
    return render_template("files.html", files=out, submenu=1)