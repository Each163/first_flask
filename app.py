from flask import Flask, request, render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

# Database
HOSTNAME = '127.0.0.1'
PORT = 3306
USERNAME = 'each'
PASSWORD = 'password'
DATABASE = 'database_learn'
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"

db = SQLAlchemy(app)

# map the change in database with migrate
migrate = Migrate(app, db)
# run the following command in terminal
# flask db init (run only once. It will create "migrations" directory in the project)
# flask db migrate: identify the change of ORM model and then generate transfer script
# flask db upgrade



# # Test if the connection works
# with app.app_context():
#     with db.engine.connect() as conn:
#         rs = conn.execute('select 1')
#         print(rs.fetchone())

class User_db(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # varchar, null=0
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(5), nullable=True)

    # use it when there is back_populates in another class
    articles = db.relationship('Article', back_populates='author')


# table relationship
class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    # add foreign key
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # back_populates should be defined in the target class
    author = db.relationship("User_db", back_populates='articles')
    # backref can automatically add a property to this class and the User class
    # author = db.relationship("User_db", backref='articles')

with app.app_context():
    db.create_all()


# get time
def datetime_format(value, format="%Y-%d-%m %H:%M"):
    return value.strftime(format)

app.add_template_filter(datetime_format, "deformat")


class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email


@app.route('/')
def hello_world():
    return 'Hello world!!!!!'


@app.route('/profile')
def profile():
    return 'This is personal profile.'


# type: string, int , float, path, UUID, any
# path: similar to string, but can contain /
# UUID: a set of 32-bit hex number
# any: any one in them
@app.route('/blog/<string:blog_id>')
def blog_detail(blog_id):
    return 'blog: %s' % blog_id


@app.route('/blog/detail/<string:blog_id>')
def blog_detail_render(blog_id):
    return render_template('blog_detail.html', blog_id=blog_id, username='Each')


@app.route('/book/list')
def book_list():
    page = request.args.get("page", default=1, type=int)
    return(f'the page you request is {page}')


@app.route('/render1')
def render1():
    return render_template('index.html')


@app.route('/class')
def class1():
    user = User('Each', '123@q.com')
    person = {
        'username': 'Zhang San',
        'email': 'zhang@q.com'
    }
    return render_template('class1.html', user=user, person=person)


@app.route('/filter')
def filter_demo():
    user = User('Each', '123@q.com')
    mytime = datetime.now()
    return render_template('filter.html', user=user, mytime=mytime)


@app.route('/control')
def control_statement():
    age = 17
    books = [{
        'name': 'san guo',
        'author': 'luo guan zhong'
    }, {
        'name': 'shui hu',
        'author': 'shi nai an'
    }]
    return render_template('control.html', age=age, books=books)


@app.route('/child1')
def child1():
    return render_template('child1.html')


@app.route('/child2')
def child2():
    return render_template('child2.html')


@app.route('/static')
def static_demo():
    return render_template('static.html')


@app.route('/user/add')
def add_user():
    # create ORM object
    # sql: insert user(username, password) values('Zhang San', '111111');
    user1 = User_db(username='Zhang San', password='111111')
    # add the ORM object into the session
    db.session.add(user1)
    # update the db.session in the database
    db.session.commit()
    return "The user is created successfully"


@app.route('/user/query')
def query_user():
    # get request: search by primary key
    user = User_db.query.get(1)
    print(f"{user.id}: {user.username}-{user.password}")
    # filter_by
    users = User_db.query.filter_by(username='Zhang San')   # QuerySet class
    print(type(users))
    for user in users:
        print(user.username)

    return "data is got successfully"


@app.route('/user/update')
def update_user():
    user = User_db.query.filter_by(username='Zhang San').first()
    user.password = '222222'
    db.session.commit()

    return 'The data is edited successfully'


@app.route('/user/delete')
def delete_user():
    user = User_db.query.get(1)
    db.session.delete(user)
    db.session.commit()

    return 'The data is deleted successfully'


@app.route('/article/add')
def article_add():
    article1 = Article(title='Flask_study', content="Flaskxxxx")
    article1.author = User_db.query.get(2)
    article2 = Article(title='Flask1_study', content="Flaskxxxxxx")
    article2.author = User_db.query.get(2)
    db.session.add_all([article1, article2])
    db.session.commit()

    return 'The article is added successfully'


@app.route('/article/query')
def query_article():
    user = User_db.query.get(2)
    for article in user.articles:
        print(article.title)
    return 'The articles are found successfully'


@app.route('/register')
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
