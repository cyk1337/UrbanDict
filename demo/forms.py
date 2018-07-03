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
from wtforms import StringField, RadioField, SelectField, SubmitField
from wtforms.validators import DataRequired


class QueryForm(FlaskForm):
    word = StringField(u'Please enter the word：', validators=[DataRequired()])
    model = SelectField(u'Model choice',
                        choices=[('bt', u'Bootstrapping'), ('crf', u'self-trained CRF'),]
                        , default='crf')
    conf = SelectField(u'Confidence level', choices=[('0.8', '0.8'), (u'0.9', '0.9')], default='0.8')
    iteration = SelectField(u'Self-training iteration', choices=[('0', '0'), ('1', '1'),('2', '2'),('3', '3'),('4', '4')], default='2')
    submit = SubmitField(u'Submit')
