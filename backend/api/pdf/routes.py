from api import app, db, bcrypt
from api.pdf.models import Pdf
from api.pdf.schema import pdf_schema, pdfs_schema
from api.pdf.utils import gen_pdf
from flask import request, jsonify
from api.auth.decorators import logged
from api.pdf.decorators import belongs_to
from os.path import dirname,abspath
from flask_cors import cross_origin

pdfs_folder = dirname(dirname(abspath(__file__))) + '/static/'

@app.route('/pdf', endpoint = 'pdf_all')
@cross_origin(supports_credentials=True)
@logged
def pdf_all(*args, **kwargs):
	pdfs = pdfs_schema.dump(Pdf.query.filter_by(uid = kwargs.get('uid')))
	return jsonify(pdfs.data)

@app.route('/pdf/<int:pid>', endpoint = 'pdf_get_pdf')
@logged
@belongs_to
def pdf_get_pdf(pid,*args,**kwargs):
	pdf = Pdf.query.get(pid)
	zones = pdf.zones
	output = {}
	output["pid"] = pdf.pid
	output["pname"] = pdf.pname

	zoneArr = []
	for zone in  zones:
		zoneObj = {}
		zoneObj["zid"] = zone.zid
		zoneObj["zname"] = zone.zname
		zoneObj["left"] = zone.left
		zoneObj["top"] = zone.top
		zoneObj["width"] = zone.width
		zoneObj["height"] = zone.height
		zoneObj["pageOffset_left"] = zone.pageOffset_left
		zoneObj["pageOffset_top"] = zone.pageOffset_top
		zoneObj["pageno"] = zone.pageno
		zoneObj["canvas_width"] = zone.canvas_width
		zoneObj["canvas_height"] = zone.canvas_height
		zoneArr.append(zoneObj)

	output["zones"] = zoneArr
	return jsonify(output)

@app.route('/pdf/create', methods=['POST'], endpoint = 'pdf_create')
@cross_origin(supports_credentials=True)
@logged
def pdf_create(*args, **kwargs):
	pfile = request.files['pfile']
	#create a pdf instance by passing respective data
	pdf = Pdf(pfile.filename)
	pdf.uid = kwargs['uid']
	#save to database
	db.session.add(pdf)
	db.session.commit()
	pfile.save(pdfs_folder + pfile.filename[:-4] + kwargs['key'][:3] + str(pdf.pid) + '.pdf')
	return pdf_schema.jsonify(pdf)

@app.route('/pdf/fill/<int:pid>', endpoint = 'pdf_fill')
@cross_origin(supports_credentials=True)
@logged
@belongs_to
def pdf_fill(pid):
	return gen_pdf(pid)