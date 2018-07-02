#!/usr/bin/env python

#-*- encoding: utf-8 

'''
                      ______   ___  __
                     / ___\ \ / / |/ /
                    | |    \ V /| ' / 
                    | |___  | | | . \ 
                     \____| |_| |_|\_\
 ==========================================================================
@author: Yekun Chai

@license: School of Informatics, Edinburgh

@contact: s1718204@sms.ed.ac.uk

@file: demo.py

@time: 01/07/2018 22:13 

@desc：       
               
'''              
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_script import Manager
app = Flask(__name__)
# app.config.from_pyfile('config.py')
manager = Manager(app)
bootstrap = Bootstrap(app)


@app.route('/', methods=['GET','POST'])
def demo_page():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        pass



if __name__ == '__main__':
    app.run(debug=True)
    # manager.run()