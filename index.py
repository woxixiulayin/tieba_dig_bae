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
    #run in develop environment
    from livereload import Server
    #anychange will trigger browser refresh
    server = Server(app.wsgi_app)
    server.serve(port=8080, host='0.0.0.0')

else:
    #run in bae
    from bae.core.wsgi import WSGIApplication
    application = WSGIApplication(app)
