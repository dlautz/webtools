from flask import Flask, render_template
from flask_jwt_simple import JWTManager
from src.common.database import Database
import pytz
import datetime


app = Flask(__name__)
app.config.from_object('src.config')


@app.before_first_request
def init_db():
    Database.initialize()

jwt = JWTManager(app)

@app.template_filter()
def format_date(date):
    utc_time = pytz.utc.localize(date)
    est_time = utc_time.astimezone(pytz.timezone("America/New_York"))
    return est_time.strftime("%m-%d-%Y %H:%M")

@app.template_filter()
def task_date(date):
    # utc_time = pytz.utc.localize(date)
    # est_time = utc_time.astimezone(pytz.timezone("America/New_York"))
    now = datetime.datetime.now()
    diff = date - now
    if diff.days < -1:
        return "Past Due"
    elif diff.days == -1:
        return "Today"
    elif diff.days == 0:
        return "Tomorrow"
    elif diff.days < 7:
        return date.strftime("%A")
    else:
        return date.strftime("%m-%d-%Y")

@app.template_filter()
def date_only(date):
    # utc_time = pytz.utc.localize(date)
    # est_time = utc_time.astimezone(pytz.timezone("America/New_York"))
    return date.strftime("%Y-%m-%d")

@app.route('/')
def home():
    return render_template('home.html')

from src.models.users.views import user_blueprint
from src.models.notebooks.views import notebook_blueprint
from src.models.notes.views import note_blueprint
from src.models.tasks.views import task_blueprint
from src.api.views import api_blueprint
app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(notebook_blueprint, url_prefix="/notebooks")
app.register_blueprint(note_blueprint, url_prefix="/notes")
app.register_blueprint(task_blueprint, url_prefix="/tasks")
app.register_blueprint(api_blueprint, url_prefix="/api")