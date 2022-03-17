from flask import Blueprint, render_template, request,session,redirect,url_for
import pymongo,random,bcrypt

auth = Blueprint('auth', __name__)

client = pymongo.MongoClient("mongodb://localhost:27017/")

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

@auth.route('/sign-up/', methods = ['GET', 'POST'])
def sign_up():
    if "user" in session:
        return redirect(url_for('logged_in'))

    if request.method == 'POST':
        email = request.form.get('email')
        PS_loc = request.form.get('PS_loc')
        Pincode = request.form.get('Pincode')

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
            user_input = { 'userid':UserId, 'email': email, 'password': hashed, 'PS_loc': PS_loc, 'Pincode':Pincode}
            #inserting it in the record collection
            records.insert_one(user_input)

            user_data = records.find_one({"email":email})
            new_email = user_data['email']

            message = 'Check your registered email'
            return render_template('sign_up.html', message = message)
    return render_template('sign_up.html')