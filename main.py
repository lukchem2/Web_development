from flask import Flask, render_template, url_for, flash,redirect
from forms import LoginForm, RegisterForm,AddcityForm
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,MetaData,Table,select
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, Text, ForeignKey, String, URL
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user,login_required
login_manager = LoginManager()

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

Bootstrap5(app)

login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(Users, user_id)


# Creating database

class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# "unnecessary  from line 35 to line 47"
# engine = create_engine('sqlite:///instance/cafes.db')
# connection = engine.connect()
# metadata = MetaData()
# metadata.reflect(bind=engine)
# users_table = metadata.tables['cafe']
#
# # Create a query to select all records from the users table
# query = select(users_table)
#
# # Execute the query
# result = connection.execute(query)
# results = result.fetchall()

class Users(db.Model,UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250),unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)

class Cafe(db.Model):
    __tablename__ = "cafe"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    map_url: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(Text, nullable=True)
    location: Mapped[str] = mapped_column(Text, nullable=True)
    has_sockets: Mapped[str] = mapped_column(Text, nullable=True)
    has_toilet: Mapped[str] = mapped_column(Text, nullable=True)
    has_wifi: Mapped[str] = mapped_column(Text, nullable=True)
    can_take_calls: Mapped[str] = mapped_column(Text, nullable=True)
    seats: Mapped[str] = mapped_column(Text, nullable=True)
    coffee_price: Mapped[str] = mapped_column(Text, nullable=True)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

#"muj kod " ????
    # def __init__(self, **kwargs):
    #     for key, value in kwargs.items():
    #         setattr(self,key,value)






with app.app_context():
    db.create_all()


@app.route("/")
def home():
    results = db.session.execute(db.select(Cafe)).scalars().all()
    return render_template("index.html",results = results)


@app.route("/login",methods=["POST","GET"])
def get_logged():
    log_form = LoginForm()
    if log_form.validate_on_submit():
        user = db.session.execute(db.select(Users).where(Users.email == log_form.email.data)).scalar()
        if user and check_password_hash(user.password, log_form.password.data):
            login_user(user)
            print(user.is_active)
            print(user.is_authenticated)
            print(user.is_anonymous)
            print(user.get_id())
            return render_template("index.html", results = results)
        elif user:
            flash("You have entered a wrong password, please try again")
        else:
            flash("This email does not exist, please try again")
    return render_template("login.html",form=log_form)


    return render_template("login.html", form=log_form)


@app.route("/register",methods=["POST","GET"])
def get_register():
    reg_form = RegisterForm()
    if reg_form.validate_on_submit():
        user = Users(name=reg_form.name.data,email = reg_form.email.data,
                     password = generate_password_hash(reg_form.password.data,
                     method="pbkdf2",salt_length=14))
        db.session.add(user)
        db.session.commit()
    return render_template("register.html", form=reg_form)

@app.route("/list")
def get_list():
    all = db.get_or_404()

@app.route("/add", methods=["POST","GET"])
def get_add():
    addform = AddcityForm()
    if addform.validate_on_submit():
        cafe = Cafe(**addform.data)
        db.session.add(cafe)
        db.session.commit()
        flash("Cafe successfully added!", "success")
        return redirect(url_for('home'))

    return render_template("add.html",form = addform)

@app.route("/cafe")
def get_cafe():
    return "<p>hello</p>"



@app.route("/log out",methods=["POST","GET"])
def get_log_out():

    logout_user()

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
