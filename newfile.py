from flask import Flask, render_template, request, redirect, session
from Auth_Module import Authorization
from Password_Manager_Final_Version import Vault
import os

auth = Authorization()
vault = Vault()

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY', 'local_key_used_for_testing')

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    success, msg, user_id = auth.login(email, password)
    
    
    if success:
        session['user_id'] = user_id
        session['email'] = email
        session['username'] = msg
        return render_template('Home_Page.html', username=msg, email=email)
    else:
        return render_template('login.html', errors=msg)
        
        
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')   
    
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
    
    
    success, msg, user_id = auth.signup(username, email, password)
    if success:
        session['user_id'] = user_id
        session['username'] = username
        session['email'] = email
        return render_template('Home_Page.html', username=username, email=email)
    else:
        return render_template('signup.html', errors=msg)
        
@app.route('/home_page', methods=['GET'])
def Home_Page():
        user_id = session.get('user_id')
        if not user_id:
            return render_template('login.html', errors='Please Sign In ')
        return render_template('Home_Page.html', username=session.get('username'), email=session.get('email'))
        
@app.route('/add_pass', methods=['GET'])
def add_pass_page():
    return render_template('add_password.html')                   
                    
@app.route('/add_passwords', methods=['POST'])
def add_password():
    user_id = session.get('user_id')
    if not user_id:
        return render_template('login.html', errors='Please Login!')
    
    website = request.form['website']
    username = request.form['username']
    password = request.form['password']
    
    add_pass = vault.add_passwords(user_id, website, username, password)
    if add_pass:
        return render_template('add_password.html', success='Password Saved Successfully!')
    else:
        return render_template('add_password.html', errors='Password Already Exists!')

@app.route('/view_pass', methods=['GET'])
def view_passwords():
    user_id = session.get('user_id')
    
    if not user_id:
        return render_template('login.html', errors='Please Login!')
        
    data = vault.view_all_passwords(user_id)
    return render_template('view_all_passwords.html', passwords=data)
    
@app.route('/search_pass', methods=['GET', 'POST'])
def search_password():
    user_id = session.get('user_id')
    
    if not user_id:
        return render_template('login.html', errors='Please Login')
        
    if request.method == 'GET':
        return render_template('search_password.html', searched=False)
        
    website_query = request.form['website']
    
    results = vault.search_passwords(user_id, website_query)
    
    return render_template('search_password.html', searched=True, query=website_query, results=results)   
    
@app.route('/update_pass', methods=['GET', 'POST'])
def update_password():
    user_id = session.get('user_id')
    
    if not user_id:
        return render_template('login.html', errors='Please Login!')
        
    if request.method == 'GET':
        return render_template('update_password.html', submit=False)                      
    website = request.form['website']
    username = request.form['username']
    new_password = request.form['password']
    
    upd_pass = vault.update_password(user_id, website, username, new_password)
    
    return render_template('update_password.html', submit=True, password=upd_pass)
    
    
@app.route('/delete_pass', methods=['GET', 'POST'])
def delete_password():
    user_id = session.get('user_id')
    
    if not user_id:
        return render_template('login.html', errors='Please Login')
        
    if request.method == 'GET':
        return render_template('delete_password.html', delete=False)
        
        
    website = request.form['website']
    username = request.form['username']
    
    delete_pass = vault.delete_password(user_id, website, username)
    
    return render_template('delete_password.html', delete=True, data=delete_pass)  
    
@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return render_template('login.html')                                                                
                                              
if __name__ == '__main__':
    app.run(debug=True)                                                                                        