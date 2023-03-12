import datetime
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, jsonify
from flask_paginate import get_page_parameter, Pagination
import funtion as fun
from exts import db

bp = Blueprint("test", __name__, url_prefix="/test")


@bp.route('/test')
def i():
    ScoreMatrix = fun.putScoreMatrixintoDatabase()
    return "hello"
