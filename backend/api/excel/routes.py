from api.pdf.models import Pdf
from flask import request, jsonify, render_template
from api import app, db


@app.route('/upload')
def excel_upload():
	return render_template('excel_uploader.html')

@app.route('/upload/create', methods=['POST'])
def excel_create():
	efile = request.files['excel']
	ename = efile.filename
	pid = request.form['pid']
	#attatch the excel to the table Pdf
	pdf = Pdf.query.get(pid)
	resp = {
		'status': 200
	}
	if pdf:
		pdf.efile = efile.read()
		pdf.ename = ename
		db.session.commit()
	else:
		resp['status'] = 404
	
	return jsonify(resp)