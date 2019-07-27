import pandas as pd
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter,A4
from api.pdf.models import Pdf
import os
from os.path import dirname,abspath
import io
from io import BytesIO
from flask import jsonify, send_file
import zipfile

pdfs_folder = dirname(dirname(abspath(__file__))) + '/static/'

def adjust_text(data, width):
	data = list(data)
	i = 0
	data_arr = []
	line = ''
	while i < len(data):
		if len(line)*10 < width:
			line += data[i]
		else:
			data_arr.append(line)
			while i < len(data) and data[i] == ' ':
				i += 1
			if i >= len(data):
				break
			line = data[i]
		i += 1
	data_arr.append(line)
	return data_arr

def fill_pdf(pdf_data, data, i):
	zones = []
	#group zones to pages
	for zone in data:
		while zone.pageno-1 >= len(zones):
			zones.append([])
		zones[zone.pageno-1].append(zone)
	#initialise pdffilewriter and pdffilereader
	old_pdf = PdfFileReader(pdf_data)
	#for all page
	for pageno,curr_page in enumerate(zones):
		if len(curr_page) == 0:
			continue
		#initialise the bytes
		packet = io.BytesIO()
		can = canvas.Canvas(packet)
		#get the actual page size of the pdf
		height = int(list(old_pdf.getPage(pageno).mediaBox)[3])
		width = int(list(old_pdf.getPage(pageno).mediaBox)[2])
		#for all zones in current page
		for zone in curr_page:
			#get the actual coordinates
			hr = height/zone.canvas_height
			wr = width/zone.canvas_width

			data_arr = adjust_text(zone.zdata+'', 0.5*wr+zone.width*wr)
			for lineno, line in enumerate(data_arr):
				t = can.beginText()
				t.setTextOrigin(0.5*wr+zone.left*wr,height - zone.top*hr-10*hr - 9*lineno)
				t.setFont("Times-Roman", 10)
				t.setFillColor("blue")
				t.textOut(line)
				can.drawText(t)
		
		#watermark
		trial = True
		if trial:
			t = can.beginText()
			t.setTextOrigin(20, 20)
			t.setFont("Times-Roman", 20)
			t.setFillColor("orange")
			t.textOut("Watermark")
			can.drawText(t)
				
		#save the canvas and bring the cursor to the very first
		can.save()
		packet.seek(0)
		#open the packet io as new_pdf
		new_pdf = PdfFileReader(packet)
		#merge corresponding pdf page and packet
		page = old_pdf.getPage(pageno)
		page.mergePage(new_pdf.getPage(0))
		output = PdfFileWriter()
		output.addPage(page)
		
		output_stream = BytesIO()
		output.write(output_stream)
		output_stream.seek(0)
		return output_stream

def process_excel(pdf, pdf_data,efile):
	# excel_path = os.path.join(folder_path, pdf.ename)
	excel_data = BytesIO(efile.read())
	excel_data.seek(0)
	#read excel
	excel = pd.read_excel(excel_data)
	keys = excel.keys()
	length = len(excel[keys[0]])
	#create a copy of zones
	zones = pdf.zones.copy()
	arr = []
	pdf_col = []
	for i in range(length):
		arr.append(zones.copy())

	for i in range(length):
		for zone in arr[i]:
			zone.zdata = str(excel[zone.zname][i])
		#generate pdf for each record
		pdf_col.append(fill_pdf(pdf_data,arr[i],i))

	return pdf_col
		
def gen_pdf(pid,efile):
	pdf = Pdf.query.get(pid)
	#check if excel is attatched to it
	f = open(pdfs_folder + '/' + pdf.pname,'rb')
	pfile = f.read()
	pdf_data = BytesIO(pfile)
	pdf_data.seek(0)
	#read excel and fill pdf
	zip_col = process_excel(pdf, pdf_data,efile)
	
	pdfs = BytesIO()
	with zipfile.ZipFile(pdfs, mode = 'w') as zip:
		for idx, i in enumerate(zip_col):
			zip.writestr('des'+str(idx)+'.pdf',i.read())
	pdfs.seek(0)
	return send_file(pdfs, attachment_filename='pdf.zip', as_attachment=True, mimetype='application/zip')
