from flask import Flask, render_template, url_for, request, redirect, jsonify, flash, abort, session
from flask.helpers import flash
from flask_mysqldb import MySQL
import MySQLdb.cursors



app = Flask(__name__)

app.secret_key = 'x232x3x23x2x3xx'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'price'
mysql = MySQL(app)

result=""
def getdata():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'SELECT * FROM products ORDER BY date_updated DESC LIMIT 10')
    global result
    result = cursor.fetchall()
    return result


@app.route("/home")
@app.route("/")
def main():
    if 'loggedin' in session: 
        return render_template("index.html", data=getdata(),msg1=session['username'])

    return redirect(url_for('login'))


@app.route('/add', methods=['GET', 'POST'])
def add():

    if request.method == 'POST':
        name = request.form['product']
        price = request.form['price']
        qty = request.form['qty']
        if name and price and qty:
            name=name.title()
            qty=qty.title().strip(" ")
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'INSERT INTO products(product,price,qty) VALUES (% s, % s, % s)', (name, price, qty, ))
            mysql.connection.commit()

            flash("Successfully Registered!")
            return redirect(url_for('add'))
        else:
            flash("All the fields required!")

    return render_template("add.html")


@app.route("/delete/<int:id>")
def delete(id):

    if int(id):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM products WHERE id=%s', (id, ))
        mysql.connection.commit()

        flash('Record successfully Deleted !')
        return redirect(url_for('main'))


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if int(id):
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM products WHERE id=%s", (id,))
            result = cursor.fetchone()
        except:
            abort(404)
        if request.method == "POST":

            cursor.execute('UPDATE products SET product=%s ,price=%s,qty=%s WHERE id=%s', (
                request.form['product'].title(), request.form['price'], request.form['qty'].rstrip().title(), id, ))
            mysql.connection.commit()
            return redirect(url_for('main'))
        elif result:

            return render_template('add.html', data1=result)

    abort(401)


@app.route("/hint/<strr>", methods=['GET', 'POST'])
def hint(strr):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'GET':

        try:
            if strr.lower() == "all":
                cursor.execute(" SELECT * FROM products ORDER BY product ASC")
                result = cursor.fetchall()
            else:
                cursor.execute(
                    " SELECT * FROM products WHERE product LIKE '{}%' ".format(strr))
                result = cursor.fetchall()
            if result:
                return jsonify(result)

        except Exception as e:
            print(e)

        abort(401)


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ""
    if 'loggedin' in session: 
        return render_template("index.html", data=getdata(),msg1=session['username'])

    if request.method == 'POST' and 'username' in request.form and 'pswd' in request.form:
        username = request.form['username']
        password = request.form['pswd']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM user WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:

            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = username
            return render_template('index.html',data=getdata(), msg1=msg)
        else:
            

            flash("All the fields Required!")
            
    return render_template('login.html',msg1=msg)

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))

# /////////////////////////////////////////////////////
@app.route('/product_check', methods=['GET', 'POST'])
def product_check():
    pr=request.args.get('q')
    qt=request.args.get('q1')

  

    # validate the received values
    if pr and qt and request.method == 'GET':

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM products WHERE product=%s AND qty=%s", (pr,qt,))
        row = cursor.fetchone()
        print(row)

        if row:
            return "Product Already In Database!"
        else:
            pass
    else:
        return "Required"
    
    return ""


if __name__ == "__main__":
    app.run( debug=True)
