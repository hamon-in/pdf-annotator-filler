from api.auth.models import User
from api.pdf.models import Pdf
from flask import request, jsonify

def belongs_to(func):
    def check_belongs_to_current_user(*args, **kwargs):
        #get key if available
        if request.json:
            key = str(request.json['key'])
        elif request.form:
            key = str(request.form['key'])
        elif request.args:
            key = str(request.args.get('key'))
        #fetch user
        user = User.query.filter_by(key = key).first()
        #fetch requested pdf
        pid=kwargs.get('pid')
        if type(pid)== str:
            pdf=Pdf.query.filter(Pdf.pname == pid, Pdf.uid == user.id).first()
            kwargs['pid']=pdf.pid
        else:
            pdf = Pdf.query.get(pid)
        if pdf and pdf.uid == user.id:
            #resource belongs to the requested user
            return func(*args, **kwargs)
        else:
            #invalid request
            return jsonify({
                'error': 'invalid request',
                'reason': 'requested resource does not belongs to the current user'
            }), 400

    return check_belongs_to_current_user