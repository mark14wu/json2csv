#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : changyanlong

from flask import Flask,render_template,request,redirect,url_for,send_file
from werkzeug.utils import secure_filename
import os
import sys

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = sys.path[0]
        upload_path = os.path.join(basepath, "static/uploads",secure_filename(f.filename))
        f.save(upload_path)
        os.system("jsoncsv -e " + upload_path + " expand.json")
        os.system("mkexcel -t csv expand.json > output.csv")
        return send_file(open("output.csv"), as_attachment=True, attachment_filename=f.filename.split('.')[0] + '.csv')
    os.system("rm expand.json")
    os.system("rm output.csv")
    os.system("rm static/uploads/*")
    return render_template("upload.html")

if __name__ == '__main__':
    app.run(debug=True)