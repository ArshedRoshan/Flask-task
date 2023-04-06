from hello import db

class TA(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   native_english_speaker = db.Column(db.String(100))
   course_instructor = db.Column(db.String(50))
   course = db.Column(db.String(200)) 
   semester = db.Column(db.String(10))
   class_size = db.Column(db.String(200)) 
   performance_score = db.Column(db.String(200))  
   password = db.Column(db.String(800))
   email = db.Column(db.String(100))
   
   def __init__( self, native_english_speaker, course_instructor, course, semester, class_size, performance_score, password,email):
      self.native_english_speaker = native_english_speaker
      self.course = course
      self.course_instructor = course_instructor
      self.semester = semester
      self.class_size = class_size
      self.performance_score = performance_score
      self.email = email
      self.password = password
   
   def serialize(self):
      return {
         "id" : self.id,
         "native_english_speaker" : self.native_english_speaker,
         "course" : self.course,
         "course_instructor" : self.course_instructor,
         "semester"  : self.semester,
         "class_size" : self.class_size,
         "performance_score" : self.performance_score,
         "email" : self.email,
         "password" : self.password
      }
