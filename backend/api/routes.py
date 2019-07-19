from api.models import Pdf, Zone
from flask import request, Response, jsonify, render_template,send_file,escape,url_for,redirect,send_from_directory
from api import app, db
from api.schema import zone_schema, pdf_schema, zones_schema, pdfs_schema
from api.pdf_filler import gen_pdf
from io import BytesIO
from werkzeug.utils import secure_filename
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# app.config['UPLOAD_FOLDER'] = ''
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

@app.route('/', methods=['GET'])
def home():
	return render_template('index.html')

@app.route('/post_pdf', methods=['POST'])
def post_pdf():
	pfile = request.files['pfile']
	pfile.save(APP_ROOT+'/'+pfile.filename)
	# print(pfile)
	#create a pdf instance by passing respective data
	pdf = Pdf(pfile.filename,pfile.read())
	# print(BytesIO(pdf.pfile))
	#save to database
	db.session.add(pdf)
	db.session.commit()
	# return pdf_schema.jsonify(pdf)
	return url_for(os.path.join(APP_ROOT),filename=pfile.filename)

@app.route('/put_zones', methods=['PUT'])
def put_zones():
	zones = request.json['zones']
	output = []
	for zone_obj in zones:
		zone = Zone.query.get(zone_obj.get('zid'))
		zone.zname = zone_obj.get('zname')
		zone.left = zone_obj.get('left')
		zone.top = zone_obj.get('top')
		zone.width = zone_obj.get('width')
		zone.heigth = zone_obj.get('height')
		zone.pageOffset_left = zone_obj.get('pageOffset_left')
		zone.pageOffset_top = zone_obj.get('pageOffset_top')
		zone.pageno = zone_obj.get('pageno')
		zone.canvas_width = zone_obj.get('canvas_width')
		zone.canvas_height = zone_obj.get('canvas_height')
		db.session.commit()
		output.append(zone)
	result = zones_schema.dump(output)
	return jsonify(result.data)

@app.route('/post_zones', methods=['POST'])
def post_zones():
	
	res = Response()
	res.headers = {
		'Accept': 'application/json',
		'Content-Type': 'application/json',
		'Access-Control-Allow-Headers': 'Content-Type',
		'Access-Control-Allow-Methods': 'POST, OPTIONS',
		'Access-Control-Allow-Origin': '*'
	}

	pid = request.json['pid']
	zones = request.json['zones']

	output = []
	for zone_obj in zones:
		zone = Zone(zone_obj['zname'],zone_obj['left'],zone_obj['top'],zone_obj['width'],zone_obj['height'],zone_obj['pageOffset_left'],zone_obj['pageOffset_top'],zone_obj['pageno'],zone_obj['canvas_width'],zone_obj['canvas_height'])
		zone.pid = request.json['pid']
		db.session.add(zone)
		db.session.commit()
		output.append(zone)
	
	result = zones_schema.dump(output)

	res.response = {
		'status': 200
	}
	return jsonify(result.data)


@app.route('/delete_zones', methods=['DELETE'])
def delete_zones():
	zids = request.json['zids']
	output = []
	
	for zid in zids:
		zone = Zone.query.get(zid)
		db.session.delete(zone)
		db.session.commit()
		output.append(zone)
	result = zones_schema.dump(output)

	return  jsonify(result.data)

@app.route('/get_pdfs')
def get_pdfs():
	pdfs = pdfs_schema.dump(Pdf.query.all())
	return jsonify(pdfs.data)

@app.route('/get_zones')
def get_zones():
	zones = zones_schema.dump(Zone.query.all())
	return jsonify(zones.data)

@app.route('/get_pdf', methods=['POST'])
def get_pdf():
	pid = request.json['pid']
	print(pid)
	pdf = Pdf.query.filter_by(pid=pid).first()
	# print(Pdf.url(pdf.pname))
	# return send_file(BytesIO(pdf.pfile),attachment_filename=pdf.pname, as_attachment=True,mimetype='multipart/form-data')
	# uploads = os.path.join(app.config['UPLOAD_FOLDER'],'/')
	# print(uploads)
	return send_file(APP_ROOT+'/'+pdf.pname, mimetype='application/pdf')

@app.route('/get_pdf/<int:pdf_id>')
def getpdf(pdf_id):
	pdf = Pdf.query.get(pdf_id)
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

@app.route('/fill/<int:pid>')
def fill(pid):
	return gen_pdf(pid)

@app.route('/upload')
def upload_excel():
	return render_template('excel_uploader.html')

@app.route('/post_excel', methods=['POST'])
def post_excel():
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
