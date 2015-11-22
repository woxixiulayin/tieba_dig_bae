#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import Flask, render_template, Response, request
from rat import Query
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        para = request.form.to_dict()
        para['deepth'] = int(para['deepth'])
        para['rep_num'] = int(para['rep_num'])
        posts = []
    try:
        query = Query(para)
        print 'done'
        posts = query.find()
        return Response(json.dumps(posts), mimetype='application/json', headers={'Cache-Control': 'no-cache'})
    except StandardError, e:
        print e
        import traceback
        traceback.print_exc()
        return Response(json.dumps(posts), mimetype='application/json', headers={'Cache-Control': 'no-cache'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888)
else:
    from bae.core.wsgi import WSGIApplication
    application = WSGIApplication(app)
