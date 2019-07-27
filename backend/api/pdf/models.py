from api import db

class Pdf(db.Model):
	pid = db.Column(db.Integer, primary_key=True)
	pname = db.Column(db.String(255), nullable=False)
	zones = db.relationship('Zone', backref='zone', lazy=True)
	uid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

	def __init__(self,name):
		self.pname = name

	def __repr__(self):
		return f'Pdf({self.pid},{self.pname})'