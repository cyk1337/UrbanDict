#!/usr/bin/env python

# -*- encoding: utf-8

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
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask import render_template, request

from forms import QueryForm
from _view_func import search_UrbanDict

app = Flask(__name__)
app.config.from_pyfile('config.py')
manager = Manager(app)
bootstrap = Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def demo_page():
    form = QueryForm()
    if form.validate_on_submit():
        word = form.word.data
        model = form.model.data

        results, var_count = search_UrbanDict(word, model)
        return render_template('index.html', data=results, var_count=var_count, form=form)

    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
    # manager.run()
