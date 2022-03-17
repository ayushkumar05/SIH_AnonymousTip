from flask import Blueprint, render_template, request, session,redirect,url_for
import pymongo
import bcrypt
import geocoder

views = Blueprint('views', __name__)

client = pymongo.MongoClient("mongodb+srv://mmm:2003@mmm.slnz2.mongodb.net/test")
db = client.get_database('total_records')
records = db.register

@views.route('/', methods = ['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        user = request.form.get('userid')
        password = request.form.get('password')
        user_found = records.find_one({'userid':user})
        if user_found:
            passwordcheck = user_found['password']

            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["user"] = user
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
        psta = records.find({'userid':user})
        ars=[]
        for ij in psta:
            ars.append(ij)
            a = ars[0]['police station']
        match = db.tips.find({"police station": a})
        
        ar=[]
        for i in match:
            ar.append(i)
        return render_template('logged_in.html',ar=ar,user=user, ps_sta = a)
    else:
        message = 'Please login into your account!'
        return redirect(url_for('/'), message = message)


@views.route("/logout")
def logout():
    if "user" in session:
        session.pop("user", None)
        return render_template('index.html')
    else:
        return render_template('index.html')


#get the database name
db  = client.get_database('total_records')
record = db.tips

#sasta location
def loc():
    g = geocoder.ip('me')
    return g.latlng[0],g.latlng[1]

@views.route('/tips/', methods = ['GET', 'POST'])
def tip():
    if request.method == 'POST':

        type = request.form.get('type')
        contact = request.form.get('contact')
        desc = request.form.get('desc')
        pincode = request.form.get('pincode')
        psta = request.form.get('police station')
        anynomous_input = {'type':type, 'contact':contact, 'desc':desc, 'police station':psta}
        record.insert_one(anynomous_input)

        message = 'successfully sent :)'
        la,lo = loc()
        temp = 'https://atlas.mapmyindia.com/api/places/nearby/json?explain&richData&&refLocation='+str(la)+','+str(lo)+'&keywords=police'
    
        return render_template('tips.html', message = message,temp=temp)

    la,lo = loc()
    temp = 'https://atlas.mapmyindia.com/api/places/nearby/json?explain&richData&&refLocation='+str(la)+','+str(lo)+'&keywords=police'
    print(temp)
    return render_template("tips.html",temp=temp)