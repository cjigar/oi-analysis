from flask import Flask

from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy 
from apps.service.script import get_option_data, set_header


app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    bnf_nearest = set_header()
    df = get_option_data()
    return render_template('market.html', column_names=df.columns.values, row_data=list(df.values.tolist()), zip=zip, bnf_nearest=bnf_nearest)
    # return render_template('market.html', tables=[df.to_html(classes='data')], titles=df.columns.values)

# @app.route('/')
# def view_data():
#     get_option_data()
#     return None


if __name__ == "__main__":
  app.run(debug=True, port=5000, host='0.0.0.0')


#https://medium.com/fintechexplained/running-python-in-docker-container-58cda726d574

#docker build --tag python-docker .
#docker run --publish 5000:5000 python-docker

