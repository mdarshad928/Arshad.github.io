from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, Submit

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/Track")
def  Track():
        return render_template('Track.html', title='Track')


@app.route("/Track", methods=['GET', 'POST'])
def  Start():
        return render_template('Start.html', title='Track')


@app.route("/Contact-Us")
def  contact():
    return render_template('Contact-Us.html', title='Contact-Us')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=False)