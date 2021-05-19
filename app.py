from flask import Flask, render_template, request, redirect, url_for
from shop.shop import shop
from shop.models import shop_db

POSTGRES = {
    'user': 'postgres',
    'pw': 'Arya5214',
    'db': 'test',
    'host': 'localhost',
    'port': '5432',
}

app = Flask(__name__)
app.register_blueprint(shop, url_prefix="/shop-project")
# Configuring the database access
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# start the database
shop_db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
