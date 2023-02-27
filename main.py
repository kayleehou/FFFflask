import threading

# import "packages" from flask
from flask import render_template  # import render_template from "public" flask libraries

# import "packages" from "this" project
from __init__ import app  # Definitions initialization
from model.jokes import initJokes
from model.users import initUsers

# setup APIs
from api.covid import covid_api # Blueprint import api definition
from api.joke import joke_api # Blueprint import api definition
from api.user import user_api # Blueprint import api definition

# setup App pages
from projects.projects import app_projects # Blueprint directory import projects definition

# register URIs
app.register_blueprint(joke_api) # register api routes
app.register_blueprint(covid_api) # register api routes
app.register_blueprint(user_api) # register api routes
app.register_blueprint(app_projects) # register app pages

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')  # connects default URL to index() function
def index():
    return render_template("index.html")

@app.route('/stub/')  # connects /stub/ URL to stub() function
def stub():
    return render_template("stub.html")

@app.route('/page/')  # connects /stub/ URL to stub() function
def page():
    return render_template("page.html")

@app.route('/1/')  # connects /stub/ URL to stub() function
def one():
    return render_template("1")

@app.route('/2/')  # connects /stub/ URL to stub() function
def two():
    return render_template("2")

@app.route('/3/')  # connects /stub/ URL to stub() function
def three():
    return render_template("3")

@app.route('/4/')  # connects /stub/ URL to stub() function
def four():
    return render_template("4")

@app.route('/5/')  # connects /stub/ URL to stub() function
def five():
    return render_template("5")

@app.route('/6/')  # connects /stub/ URL to stub() function
def six():
    return render_template("6")

@app.route('/7/')  # connects /stub/ URL to stub() function
def seven():
    return render_template("7")

@app.route('/8/')  # connects /stub/ URL to stub() function
def eight():
    return render_template("8")

@app.route('/9/')  # connects /stub/ URL to stub() function
def nine():
    return render_template("9")

@app.route('/10/')  # connects /stub/ URL to stub() function
def ten():
    return render_template("10")

@app.route('/11/')  # connects /stub/ URL to stub() function
def eleven():
    return render_template("11")

@app.route('/12/')  # connects /stub/ URL to stub() function
def twelve():
    return render_template("12")

@app.route('/13/')  # connects /stub/ URL to stub() function
def thirteen():
    return render_template("13")

@app.route('/14/')  # connects /stub/ URL to stub() function
def fourteen():
    return render_template("14")

@app.route('/15/')  # connects /stub/ URL to stub() function
def fifteen():
    return render_template("15")

@app.route('/16/')  # connects /stub/ URL to stub() function
def sixteen():
    return render_template("16")

@app.route('/17/')  # connects /stub/ URL to stub() function
def seventeen():
    return render_template("17")

@app.route('/18/')  # connects /stub/ URL to stub() function
def eighteen():
    return render_template("18")

@app.route('/19/')  # connects /stub/ URL to stub() function
def nineteen():
    return render_template("19")

@app.route('/20/')  # connects /stub/ URL to stub() function
def twenty():
    return render_template("20")

@app.before_first_request
def activate_job():
    initJokes()
    initUsers()

# this runs the application on the development server
if __name__ == "__main__":
    # change name for testing 
    from flask_cors import CORS
    cors = CORS(app)
    app.run(debug=True, host="0.0.0.0", port="8332")
