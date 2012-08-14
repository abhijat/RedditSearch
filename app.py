from flask import Flask, render_template, request, url_for
from search import search

app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def start_page():
    if request.method == 'GET':
        return render_template('search_form.html')
    elif request.method == 'POST':
        q = request.form['query']
        matches = search(q)
        return render_template('search_results.html', 
            query=q, 
            results=matches, 
            css=url_for('static', filename='main.css'))

if __name__ == '__main__':
    app.run()
