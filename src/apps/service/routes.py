# -*- encoding: utf-8 -*-


from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)
import datetime as dt

from apps import db, login_manager
from apps.service import blueprint
from apps.service.models import OICalls, OIPuts, OI
from apps.service.script import  get_option_data, set_header

from sqlalchemy import create_engine
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#Service data inserted
@blueprint.route('/service', methods=['GET'])
def service():
    logger.info("Service called")
    bnf_nearest = set_header()
    df = get_option_data()
    
    for index, row in df.iterrows():
        calls = OICalls(
            oi = row['call_oi'],
            change_oi = row['call_change_oi'],
            strike = row['call_strikePrice'],
            price = row['call_value'],
        )
        db.session.add(calls) 
        puts = OIPuts(
            oi = row['put_oi'],
            change_oi = row['put_change_oi'],
            strike = row['put_strikePrice'],
            price = row['put_value'],
        )
        db.session.add(puts)
        db.session.commit()

        oi = OI(
            call_id = calls.id,
            put_id = puts.id,
            expiry = row['call_expiryDate']
        )
        db.session.add(oi)
        db.session.commit()
    
    return render_template('home/worksheet.html')
    

@blueprint.route('/worksheet', methods=['GET'])
def worksheet():
    logger.info("worksheet called")

    query = db.select([OICalls])

    print("here -> ", query)
    return render_template('home/worksheet.html')

    

# Errors
@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
