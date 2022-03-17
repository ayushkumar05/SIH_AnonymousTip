from flask import Blueprint, render_template, request, session,redirect,url_for
import pymongo
import bcrypt

views = Blueprint('views', __name__)

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.get_database('total_records')
records = db.register

@views.route('/', methods = ['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        print('post')
        user = request.form.get('userid')
        password = request.form.get('password')
        print('huh')
        user_found = records.find_one({'userid':user})
        print('here0')
        if user_found:
            print('here')
            passwordcheck = user_found['password']

            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["user"] = user
                print('check')
                return redirect('/logged_in')
            else:
                if 'user' in session:
                    print('check123')
                    return (url_for('/logged_in'))
                message = "Wrong password"
                return render_template('index.html',message = message)
        else:
            message = 'User not found'
            return render_template('index.html', message = message)
    return render_template('index.html', message = message)

@views.route('/logged_in')
def logged_in():
    if 'user' in session:
        user = session['user']
        return render_template('logged_in.html')
    else:
        return redirect(url_for('/'))



    return render_template('index.html')