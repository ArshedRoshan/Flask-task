from models import TA
from flask import Flask,redirect,url_for,request,render_template,jsonify,make_response
from hello import apps,db
from  werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps


app = apps()

@app.route('/Add',methods = ['POST'])
def Add():
   if request.method == 'POST':
      native_english_speaker, course_instructor, course, semester, class_size, performance_score, email = request.json['native_english_speaker'],request.json['course_instructor'],request.json['course'],request.json['semester'],request.json['class_size'],request.json['performance_score'],request.json['email']
      password = request.json['password']
      s = TA(
         native_english_speaker=native_english_speaker,
         course_instructor=course_instructor,
         course=course,
         semester=semester,
         class_size = class_size,
         performance_score=performance_score,
         email=email,
         password=generate_password_hash(password)
      )
      db.session.add(s)
      db.session.commit()
      
      return jsonify(s.serialize())
   return jsonify('error')

@app.route('/login',methods = ['POST'])
def login():
   auth = request.form
   print('auth:', auth)
   user = TA.query.filter_by(email = auth.get('email')).first()
   print('user',user)
   if not user:
        # returns 401 if user does not exist
      return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
        )
   
   if check_password_hash(user.password,auth.get('password')):
      token = jwt.encode({
         'id' : user.id,
          'exp' : datetime.utcnow() + timedelta(minutes = 30),
          
      },app.config['SECRET_KEY'])
      return make_response(jsonify({'token' : token}), 201)
   return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
    )
   



def token_required(f):
   @wraps(f)
   def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            print('Token:', token)
            print('SECRET_KEY:', app.config['SECRET_KEY'])
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=['HS256'])
            current_user = TA.query\
                .filter_by(id = data['id'])\
                .first()
        except Exception as e:
            print('Exception:', e)
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users context to the routes
        return  f(current_user, *args, **kwargs)
  
   return decorated


@app.route('/retrieve/<int:id>',methods = ['GET'])
@token_required
def Retrieve(current_user,id):
   student = TA.query.filter_by(id=id).first()
   serilaizer = student.serialize()
   return jsonify(serilaizer)

@app.route('/delete/<int:id>',methods = ['DELETE'])
@token_required
def delete_student(current_user,id):
   print('requestdel',request)
   student = TA.query.filter_by(id=id).first()
   if not student:
      return jsonify(f"TA with ID {id} not found"), 404
   db.session.delete(student)
   db.session.commit()
   return jsonify('Deleted succesfully')

@app.route('/update/<int:id>',methods = ['PUT'])
@token_required
def update_details(current_user,id):
   student = TA.query.filter_by(id=id).first()
   student.native_english_speaker = request.json.get('native_english_speaker', student.native_english_speaker)
   student.course_instructor = request.json.get('course_instructor', student.course_instructor)
   student.course = request.json.get('course', student.course)
   student.semester = request.json.get('semester', student.semester)
   student.class_size = request.json.get('class_size', student.class_size)
   student.performance_score = request.json.get('performance_score', student.performance_score)
   student.email = request.json.get('email', student.email)
   db.session.commit()
   return jsonify(student.serialize())

