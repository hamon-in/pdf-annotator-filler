from api import app, db, bcrypt
from api.pdf.models import Pdf
from api.pdf.schema import pdf_schema, pdfs_schema
from api.pdf.utils import gen_pdf
from flask import request, jsonify,send_from_directory,send_file
from api.auth.decorators import logged
from api.pdf.decorators import belongs_to
from os.path import dirname,abspath
from flask_cors import cross_origin
from api.excel.routes import excel_create 

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
	count = db.session.query(Pdf).count()
	#create a pdf instance by passing respective data
	pfile.save(pdfs_folder + pfile.filename[:-4] + kwargs['key'][:3] + str(count+1) + '.pdf')
	f = open(pdfs_folder + pfile.filename[:-4] + kwargs['key'][:3] + str(count+1) + '.pdf','rb')
	pdf = Pdf(pfile.filename,f.read())
	pdf.uid = kwargs['uid']
	#save to database
	db.session.add(pdf)
	db.session.commit()
	return pdf_schema.jsonify(pdf)


@app.route('/pdf/fill/<int:pid>', endpoint = 'pdf_fill')
@cross_origin(supports_credentials=True)
@logged
@belongs_to
def pdf_fill(pid,*args,**kwargs):
	# return send_from_directory(pdfs_folder,filename="EPFS Form$2b1.pdf",as_attatchment=True)
	return gen_pdf(pid)