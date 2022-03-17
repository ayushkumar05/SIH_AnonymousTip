from flask import Blueprint, render_template, request,session,redirect,url_for
import pymongo,random,bcrypt,geocoder

auth = Blueprint('auth', __name__)

client = pymongo.MongoClient("mongodb+srv://mmm:2003@mmm.slnz2.mongodb.net/test")

#get the database name
db  = client.get_database('total_records')
records = db.register


def genrandom():
    n = ''
    x=0
    while x<7:
        y = random.randint(1,9)
        if str(y) not in n:
            n+=str(y)
            x+=1
    return str(n)

def gen_id():
    n = genrandom()
    if records.find_one({"userid":n}):
        print('already exists')
        gen_id()
    else:
        return n

#sasta location
def loc():
    g = geocoder.ip('me')
    return g.latlng[0],g.latlng[1]

@auth.route('/sign-up/', methods = ['GET', 'POST'])
def sign_up():
    if "user" in session:
        return redirect('/logged_in')

    if request.method == 'POST':
        email = request.form.get('email')
        psta = request.form.get('police station')

        password = request.form.get('password')
        confirm_pass = request.form.get('confirm_pass')
        UserId = gen_id()
        #Checking whether email is already registered or not
        email_found = records.find_one({"email":email})
        
        if email_found:
            message = 'This email already exists'
            return render_template('sign_up.html', message = message)

        if password!=confirm_pass:
            message = 'Passwords should match!'
            return render_template('sign_up.html',message = message)
        
        else:
            
            #hashing the password and encoding it
            hashed = bcrypt.hashpw(confirm_pass.encode('utf-8'), bcrypt.gensalt())

            #assigning the data in a dictionary in key value pairs
            user_input = { 'userid':UserId, 'police station':psta, 'email': email, 'password': hashed}
            #inserting it in the record collection
            records.insert_one(user_input)
            message = 'successfully sent :)'
            la,lo = loc()
            temp = 'https://atlas.mapmyindia.com/api/places/nearby/json?explain&richData&&refLocation='+str(la)+','+str(lo)+'&keywords=police'
    
            return render_template('sign_up.html', message = message,temp=temp)

    la,lo = loc()
    temp = 'https://atlas.mapmyindia.com/api/places/nearby/json?explain&richData&&refLocation='+str(la)+','+str(lo)+'&keywords=police'
    print(temp)
    return render_template("sign_up.html",temp=temp)

