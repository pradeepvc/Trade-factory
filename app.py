from flask import Flask, render_template, request, redirect
from models import db, UserModel
from autologin import selenium_kite_login

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def login_users():
    if request.method == 'GET':
        return render_template('login_user.html')
    if request.method == 'POST':
        u_name = request.form['u_name']
        p_word = request.form['p_word']
        if u_name == "admin" and p_word == "admin@101":
            return redirect('/home')
        else:
            return redirect('/')


@app.route('/form', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('forms.html')

    if request.method == 'POST':
        user_id = request.form['user_id']
        name = request.form['name']
        password = request.form['password']
        apikey = request.form['api_key']
        api_secret_key = request.form['api_secret_key']
        totp_key = request.form['totp_key']
        access_key = ""
        access_key_time = ""
        autologin_status = request.form['autologin_status']
        autologin_verify = ""
        autologin1 = ""
        sp_buy_n = ""
        sp_sell_n = ""
        sp_buy_bn = ""
        sp_sell_bn = ""
        q_n = ""
        q_bn = ""
        users = UserModel(
            user_id=user_id,
            name=name,
            password=password,
            api_key=apikey,
            api_secret_key=api_secret_key,
            totp_key=totp_key,
            access_key=access_key,
            access_key_time=access_key_time,
            autologin_status=autologin_status,
            autologin_verify=autologin_verify,
            autologin1=autologin1,
            sp_buy_n=sp_buy_n,
            sp_sell_n=sp_sell_n,
            sp_buy_bn=sp_buy_bn,
            sp_sell_bn=sp_sell_bn,
            q_n=q_n,
            q_bn=q_bn
        )
        db.session.add(users)
        db.session.commit()
        return redirect('/users')


@app.route('/users')
def retrieve_list():
    users = UserModel.query.all()
    return render_template('tables-data.html', users=users)


@app.route('/autologin')
def autologin():
    users = UserModel.query.all()
    return render_template('autologin_table.html', users=users)


@app.route('/config')
def config():
    users = UserModel.query.all()
    return render_template('layout-sidebar-style-1.html', users=users)


@app.route('/running_config')
def running_config():
    users = UserModel.query.all()
    return render_template('running_configs.html', users=users)


@app.route('/default_config')
def default_config():
    users = UserModel.query.all()
    return render_template('default_config.html', users=users)


@app.route('/switch')
def switch():
    users = UserModel.query.all()
    return render_template('switchtrade.html', users=users)


@app.route('/close')
def close():
    users = UserModel.query.all()
    return render_template('closetrade.html', users=users)


@app.route('/balance')
def balance():
    users = UserModel.query.all()
    return render_template('balancetrade.html', users=users)


@app.route('/openposition')
def openposition():
    users = UserModel.query.all()
    return render_template('openposition.html', users=users)


@app.route('/m2m')
def m2m():
    users = UserModel.query.all()
    return render_template('m2m.html', users=users)


@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def update(id):
    user = UserModel.query.filter_by(id=id).first()
    if request.method == 'POST':
        if user:
            db.session.delete(user)
            db.session.commit()
        user_id = request.form['user_id']
        name = request.form['name']
        password = request.form['password']
        api_key = request.form['api_key']
        api_secret_key = request.form['api_secret_key']
        totp_key = request.form['totp_key']
        access_key = ""
        access_key_time = ""
        autologin_status = request.form['autologin_status']
        autologin_verify = ""
        autologin1 = ""
        sp_buy_n = ""
        sp_sell_n = ""
        sp_buy_bn = ""
        sp_sell_bn = ""
        q_n = ""
        q_bn = ""
        users = UserModel(
            user_id=user_id,
            name=name,
            password=password,
            api_key=api_key,
            api_secret_key=api_secret_key,
            totp_key=totp_key,
            access_key=access_key,
            access_key_time=access_key_time,
            autologin_status=autologin_status,
            autologin1=autologin1,
            autologin_verify=autologin_verify,
            sp_buy_n=sp_buy_n,
            sp_sell_n=sp_sell_n,
            sp_buy_bn=sp_buy_bn,
            sp_sell_bn=sp_sell_bn,
            q_n=q_n,
            q_bn=q_bn
        )
        db.session.add(users)
        db.session.commit()
        return redirect('/users')

    return render_template('update.html', user=user)


@app.route('/<int:id>/delete', methods=['GET', 'POST'])
def profile(id):
    users = UserModel.query.filter_by(id=id).first()
    if request.method == 'POST':
        if users:
            db.session.delete(users)
            db.session.commit()
            return redirect('/users')
    return render_template('delete.html')


@app.route('/<int:id>/login', methods=['GET', 'POST'])
def login(id):
    user = UserModel.query.filter_by(id=id).first()
    ad = selenium_kite_login(user.api_key, user.user_id, user.password, user.totp_key, user.api_secret_key)
    print(ad)
    user.access_key = ad[0]
    user.access_key_time = ad[1]
    user.autologin1 = ad[2]
    users = UserModel.query.all()
    db.session.commit()
    print(users)
    return redirect('/autologin')
    return render_template("autologin_table.html", users=users)


@app.route('/<int:id>/add_config', methods=['GET', 'POST'])
def add_config(id):
    user = UserModel.query.filter_by(id=id).first()

    return redirect('/config')


if __name__ == '__main__':
    app.run(debug=True)
