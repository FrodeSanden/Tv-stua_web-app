from urllib import request
from xmlrpc.client import DateTime
from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user
from .models import Program
from . import db
import json
import datetime

views = Blueprint('views', __name__ )
def hentDato():
    current_time = datetime.datetime.now()
    idag = str(current_time.day) + str(current_time.month)
    return idag

@views.route('/', methods = ['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        time_start = request.form.get('time_start')
        time_end = request.form.get('time_end')
        date = request.form.get('date')
        
        
        if len(name) < 1:
            flash('name too short', category='error')
        elif int(time_start) < 0:
            flash('tid start feil', category='error')
        elif int(time_end) < 0:
            flash('tid slutt feil', category='error')
        else:
            new_program = Program(Name=name,user_id=current_user.id, time_start=time_start, time_end=time_end,date=date, votes= 0 )
            db.session.add(new_program)
            db.session.commit()
            flash('Program lagt til', category='success')   
    return render_template("home.html", user = current_user )

@views.route('/delete-program', methods=['POST'])
def delete_program():
    program = json.loads(request.data)
    programId = program['programId']
    program = Program.query.get(programId)
    if program:
        if program.user_id == current_user.id:
            db.session.delete(program)
            db.session.commit()
            return jsonify({})
            
            
@views.route('/programList', methods=['POST','GET'])
@login_required
def showPrograms():
    if request.method=='GET':
        try:
            args = request.args
            dato = args.get('date', default=hentDato(), type=int)
            prog = Program.query.filter_by(date=dato).order_by(Program.votes.desc()).all()
            return render_template("programList.html", Program = prog, user=current_user, date=dato)
        except Exception as e:
            # e holds description of the error
            error_text = "<p>The error:<br>" + str(e) + "</p>"
            hed = '<h1>Something is broken.</h1>'
            return hed + error_text
        
    return render_template("programList.html")

@views.route('/vote-program', methods=['POST'])
def vote_program():
    program = json.loads(request.data)
    programId = program['programId']
    program = Program.query.get(programId)
    if program:
        program.votes += 1
        db.session.commit()
        return jsonify({})