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
                        choices=[('0', u'Bootstrapping'), ('1', u'self-trained CRF'), ('2', u'others')], default='1')
    submit = SubmitField(u'Submit')
