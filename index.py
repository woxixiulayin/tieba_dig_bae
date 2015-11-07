#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import Flask, render_template, Response, request

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        print request.form.to_dict()

	return Response(json.dumps(comments), mimetype='application/json', headers={'Cache-Control': 'no-cache'})

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8888)
else:
	from bae.core.wsgi import WSGIApplication
	application = WSGIApplication(app)
