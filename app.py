from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'sanju'
app.config['MYSQL_PASSWORD'] = 'sanju'
app.config['MYSQL_DB'] = 'flaskapp'
mysql = MySQL(app)

@app.route('/post', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #Fetch the form data
        MessageDetails = request.form
        message = MessageDetails['message']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO messages (message) VALUES (%s)",[message])
        mysql.connection.commit()
        cur.close()

        return redirect('/view')
    return render_template('index.html')
@app.route('/view')
def view():
    cur = mysql.connection.cursor()
    resultValues = cur.execute("SELECT * FROM   messages")
    if resultValues > 0:
        Messages = cur.fetchall()
        return render_template('messages.html',Messages=Messages)
@app.route('/search', methods=['GET', 'POST'])
def search():

    if request.method == 'POST':

        SearchValue = request.form['searchField']
        print(SearchValue)
        cur = mysql.connection.cursor()
        searchResult = cur.execute("SELECT * FROM messages WHERE message LIKE %s", ("%" + SearchValue + "%",))
        if searchResult > 0:
            result = cur.fetchall()
            return render_template('search_result.html', result=result)

        
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)

