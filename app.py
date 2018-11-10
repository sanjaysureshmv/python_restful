from flask import Flask, render_template, render_template_string, request, redirect
from flask_mysqldb import MySQL
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'sanju'
app.config['MYSQL_PASSWORD'] = 'sanju'
app.config['MYSQL_DB'] = 'flaskapp'
mysql = MySQL(app)

@app.route('/')
def home():
    return redirect('/view')

@app.route('/post', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch the form data
        MessageDetails = request.form
        message = MessageDetails['message']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO messages (message) VALUES (%s)", [message])
        mysql.connection.commit()
        cur.close()

        return redirect('/view', code=301)
    return render_template('index.html')


@app.route('/view')
def view():
    cur = mysql.connection.cursor()
    resultValues = cur.execute("SELECT * FROM   messages")
    if resultValues > 0:
        Messages = cur.fetchall()
        return render_template('messages.html', Messages=Messages)


@app.route('/search', methods=['GET', 'POST'])
def search():

    if request.method == 'POST':

        SearchValue = request.form['searchField']
        x = palindrome(SearchValue)
        #print (stringTest)
        cur = mysql.connection.cursor()
        searchResult = cur.execute(
            "SELECT * FROM messages WHERE message LIKE %s", ("%" + SearchValue + "%",))
        result = cur.fetchall()
        if searchResult > 0 and x == 'Palindrome':
            return render_template('search_result.html', result=result, check_palindrome=x)
        elif searchResult > 0 and x == 'Not palindrome':
            return render_template('search_result.html', result=result, check_palindrome=x)
        else:
            return render_template('search_not_found.html', message=SearchValue)



    return render_template('search.html')
@app.route('/delete', methods=['GET','POST'])
def delete():
    if request.method == 'POST':
        DeleteMsg = request.form['delete_field']
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM messages WHERE message=%s",(DeleteMsg,))
        mysql.connection.commit()
        cur.close()

        return redirect('/view', code=301)
    return render_template('delete.html')




def palindrome(search_value):
    rev = search_value[::-1]
    #print(rev)
    if (rev == search_value):
        return 'Palindrome'
    else:
        return 'Not palindrome'
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
