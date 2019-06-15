import os
import sqlite3
from flask import *
from flask_sqlalchemy import *
from datetime import datetime
from flask import send_from_directory
from werkzeug.utils import secure_filename
from sqlalchemy import update
from sqlalchemy import desc


app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///confessions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key = 'random string'

UPLOAD_FOLDER = 'F:/MSIT/Social computing/Heroku-MSITConfessions-master/Heroku-MSITConfessions-master/static'

ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif','txt','pdf','JPG'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

class Users(db.Model):
	__tablename__='users'
	pic = db.Column(db.String(255))
	password = db.Column(db.String(255))
	email = db.Column(db.String(255),primary_key=True)
	name = db.Column(db.String(255))
	phone = db.Column(db.String(255))
	gender = db.Column(db.String(255))
	Birthday = db.Column(db.String(255))

class Image(db.Model):
	__tablename__='images'
	title = db.Column(db.String(255))
	id =db.Column(db.Integer,primary_key=True)
	imagename = db.Column(db.String(255))
	upvotes =db.Column(db.Integer)
	downvotes =db.Column(db.Integer)
	email = db.Column(db.String(255))


class Like(db.Model):
	__tablename__='votes'
	likes_id =db.Column(db.String(255),primary_key=True)

class comm(db.Model):
	__tablename__='cmts'
	email =db.Column(db.String(255))
	id =db.Column(db.Integer,primary_key=True)
	idn =db.Column(db.Integer)
	comment = db.Column(db.String(255))



db.create_all()

em = ''
@app.route("/register",methods = ['GET','POST'])
def register():
	if request.method =='POST':
		pic = "No"
		password = request.form['password']
		password1= request.form['password1']
		email = request.form['email']
		name = request.form['name']
		gender = request.form['gender']
		Birthday = request.form['Birthday']
		phone = request.form['phone']
		if(password == password1):
			try:
				user = Users(pic=pic,password=password,email=email,name=name,gender=gender,Birthday=Birthday,phone=phone)
				db.session.add(user)
				db.session.commit()
				msg="registered successfully"
			except:
				db.session.rollback()
				msg="error occured"
		else:
			return render_template("layout.html",error1="password doesnot match")
	db.session.close()
	return render_template("layout.html",msg=msg)

@app.route("/loginForm")
def loginForm():
		return render_template('layout.html', error='')


@app.route('/')
def layout():	
	return render_template("layout.html")

@app.route("/registerationForm")
def registrationForm():
	return render_template("layout.html")


@app.route("/login", methods = ['POST', 'GET'])
def login():
	if request.method == 'POST':
		email = request.form['email']
		global em 
		em = email
		password = request.form['password']
		if is_valid(email, password):
			session['email'] = email
			session['logged_in'] = True
			global x
			x = email
			return redirect(url_for('index'))
		else:
			error = 'Invalid UserId / Password'
			return render_template('layout.html', error=error)
x=""		
@app.route('/index')
def index():
	if 'email' in session:
		email = session['email']
		image1 = "SELECT * FROM images"
		data1 = db.engine.execute(image1).fetchall()
		data2=reversed(data1)
		cts1 = "SELECT * FROM cmts"
		data3 = db.engine.execute(cts1).fetchall()
		# data2=reversed(data1)

		return render_template('main.html',email=email,name=data2,cts=data3)
	return render_template('layout.html')

def is_valid(email,password):
	stmt = "SELECT email, password FROM users"
	data = db.engine.execute(stmt).fetchall()
	for row in data:
		if row[0] == email and row[1] == password:
			return True
	return False


@app.route("/write")
def write():
	return render_template('main.html')


@app.route('/update', methods=['GET', 'POST'])
def update_Details():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			# "SELECT * FROM users WHERE email = x"
			det = Users.query.get(x)
			det.pic = file.filename
			db.session.commit()
			return redirect(url_for('about'))
	

@app.route("/About")
def about():
	stmt = "SELECT * FROM users"
	data = db.engine.execute(stmt).fetchall()
	# print(data.pic)
	for confession1 in data:
		if(confession1.email==x):
			Pic = confession1.pic 
			print("pic = ",Pic)
			Name=confession1.name
			Email=confession1.email
			Birthday=confession1.Birthday
			gender=confession1.gender
			mobile=confession1.phone
			return render_template('about.html',Img=Pic,Name=Name,Email=Email,Birthday=Birthday,gender=gender,mobile=mobile)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		print("vignan")

		title = request.form['article']

		print(title)
		file = request.files['file']
		print (file)
		# check if post request has file path
		if 'file' not in request.files or file.filename == '':
			print ("return.............")
			print("no image...................")
			print("vignan")

			return redirect(url_for('uploaded_file',filename="NO_IMG",title=title))

			# flash('No file part')
			# return redirect(request.url)
		file = request.files['file']
		print (file)
		# if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
			flash('No selected file')
			print(123456789)
			return redirect(request.url)
		print("path doesn't know....")
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			# MYDIR = os.path.dirname(__file__)
			print ("Is saving.....")
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			# os.path.join(app.config['UPLOAD_FOLDER'], filename)
			# file.save(os.path.join(MYDIR + "/" + app.config['UPLOAD_FOLDER'] + "/" + filename))
			print("image...................")
			# 
			return redirect(url_for('uploaded_file',filename=file.filename,title=title))
		print("No data")
	error="error occured"
	return render_template("main.html",error=error)


@app.route('/delete/<xid>/<email>', methods=['GET', 'POST'])
def delete_post(xid,email):
	print(xid,email)
	xd = int(xid)
	xd1 = email+xid
	print(xd1)
	print(type(xd1))
	sql1 = "SELECT email FROM images WHERE id = ?"
	adr = (xd)
	sql2 = db.engine.execute(sql1,adr).fetchall()
	if str(sql2[0][0]) == str(em):
		Image.query.filter_by(id=xd).delete()
		db.session.commit()
		Like.query.filter_by(likes_id=xd1).delete()
		db.session.commit()
		comm.query.filter_by(idn=xd).delete()
		db.session.commit()



	return redirect(url_for('index'))

@app.route('/edit/<xid>/<email>', methods=['GET', 'POST'])
def edit_post(xid,email):
	print("vignan is a good boy")
	print(xid,email)
	xd = int(xid)
	xd1 = email+xid
	print(xd1)
	print(type(xd1))
	sql1 = "SELECT email FROM images WHERE id = ?"
	adr = (xd)
	sql2 = db.engine.execute(sql1,adr).fetchall()
	if request.method == 'POST':
		Image.query.filter_by(id=xd).delete()
		db.session.commit()
		Like.query.filter_by(likes_id=xd1).delete()
		db.session.commit()
		# if request.method == 'POST':

		title = request.form['article']

		file = request.files['file']
		# print (file)
		print(title)
		
		print("vignan")
		
		# check if post request has file path
		if 'file' not in request.files or file.filename == '':
			print ("return.............")
			print("no image...................")
			print("vignan")

			return redirect(url_for('uploaded_file',filename="NO_IMG",title=title))

			# flash('No file part')
			# return redirect(request.url)
		file = request.files['file']
		print (file)
		# if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
			flash('No selected file')
			print(123456789)
			return redirect(request.url)
		print("path doesn't know....")
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			print ("Is saving.....")
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			print("image...................")
			return redirect(url_for('uploaded_file',filename=file.filename,title=title))
		print("No data")
	error="error occured"
	return render_template("main.html",error=error)


@app.route('/editdetails/<Email>', methods=['GET', 'POST'])
def edit_details(Email):
	if request.method == 'POST':
		name = request.form['name']
		phone = request.form['phone']
		admin = Users.query.filter_by(email=Email).first()
		if name != "":
			admin.name = name
		if phone != "":
			admin.phone = phone
		db.session.commit()
	return redirect(url_for('about'))

@app.route('/editcomment/<xid>', methods=['GET', 'POST'])
def edit_comment(xid):
	adr = int(xid)
	cmt = request.form['text']
	admin = comm.query.filter_by(id=adr).first()
	new_d = admin.comment
	print(new_d)
	admin.comment = cmt
	db.session.commit()
	return redirect(url_for('index'))

@app.route('/deletecomment/<xid>', methods=['GET', 'POST'])
def del_comment(xid):
	comm.query.filter_by(id=int(xid)).delete()
	db.session.commit()
	return redirect(url_for('index'))





def allowed_file(filename):
	return '.' in filename and \
			filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>/<title>',methods=['GET', 'POST'])
def uploaded_file(filename,title):
	print (filename)
	if(len(filename)>0):
		print("Hello All",em)
		ImagesAll = Image(imagename=filename,title=title,upvotes=0,email = em,downvotes=0)
		db.session.add(ImagesAll)
		db.session.commit()
		return redirect(url_for('index'))
	else:
		ImagesAll = Image(imagename=filename,title=title,upvotes=0,email = em,downvotes=0)
		db.session.add(ImagesAll)
		db.session.commit()
		return redirect(url_for('index'))


@app.route('/votes/<xid>', methods=['GET', 'POST'])
def votes(xid):
	xid=int(xid)
	s=x+str(xid)
	# print(xid+"........................XID")
	if request.method == 'POST':
		name = request.form['voted']
		print("sdsd",name)
		stmt=Image.query.filter_by(id=xid).all()[0]
		stmt2=Like.query.filter_by(likes_id=s).all()
		if(len(stmt2)==0):
			if(name =="like"):
				liked=Like(likes_id=s)
				db.session.add(liked)
				# db.session.commit()
				stmt.upvotes+=1
				db.session.commit()
				return redirect(url_for('index'))
			else:
				liked=Like(likes_id=s)
				db.session.add(liked)
				stmt.downvotes+=1
				print(stmt.downvotes)
				db.session.commit()
				return redirect(url_for('index'))
		return redirect(url_for('index'))

	return render_template("layout.html")

@app.route('/comment/<xid>', methods=['GET', 'POST'])
def comment(xid):
	cmts1 = request.form['text']

	cmt = comm(email = em,idn=xid,comment=cmts1)
	db.session.add(cmt)
	db.session.commit()













	# xid=int(xid)
	# print("rm = ",type(request.method))

	# if request.method == 'POST':
	# 	# print(12345)
	# 	name = request.form['text']
	# 	print(12345)
	# 	print("Your commentis here")
	# 	print(name)
	# 	if(len(name)>0):
	# 		stmt=Image.query.filter_by(id=xid).all()[0]
	# 		z=stmt.comment.replace('\n','<br>')
	# 		s=z+"\n"+em+' '+'says : '+name
	# 		s=s.replace('\n','<br>')
	# 		stmt.comment=s
	# 		db.session.commit()
	# 		return redirect(url_for('index'))
	return redirect(url_for('index'))

@app.route('/sign/<name>/<email>')
def sign(name,email):
	try:
		user = Users(password=None,email=email,name=name,gender=None,Birthday=None,phone=None)
		db.session.add(user)
		db.session.commit()
		msg="registered successfully"
	except:
		db.session.rollback()
		msg="error occured"
	session['email'] = email
	session['logged_in'] = True
	global y
	y=email
	return redirect(url_for('index'))

@app.route('/logout')
def logout():
	session['logged_in'] = False
	session.pop('email',None)
	x=''
	return redirect(url_for('index'))

if __name__ =='__main__':
	app.run(debug = True)
	# debug = True
