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

@file: forms.py

@time: 02/07/2018 11:03 

@desc：       
               
'''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired


class QueryForm(FlaskForm):
    word = StringField(u'Please enter the word：', validators=[DataRequired()])
    model = SelectField(u'Model choice',
                        choices=[('bt1', u'Bootstrapping'), ('crf0', u'self-trained CRF iter0'), ('crf1', u'self-trained CRF iter1'),('crf2', u'self-trained CRF iter2'),('crf3', u'self-trained CRF iter3'),('crf4', u'self-trained CRF iter4'), ('other', u'others')], default='crf1')
    submit = SubmitField(u'Submit')
