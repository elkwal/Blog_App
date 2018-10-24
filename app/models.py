from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(10),unique = True,nullable = False)
    email = db.Column(db.String(),unique = True,nullable = False)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash= db.Column(db.String(255))
    blog = db.relationship('Blog',backref = 'users',lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')


    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def __repr(self):
        return f'User {self.username}'



class Blog (db.Model):
    '''
    Blog class to define Blog Objects
    '''
    __tablename__ = 'blog'

    id = db.Column(db.Integer,primary_key = True)
    blog = db.Column(db.String)
    blog_id = db.Column(db.Integer)
    category_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comments = db.relationship('Comment',backref = 'blog',lazy="dynamic")
    title = db.Column(db.String(255))


    def save_blog(self):
        '''
        Function that saves blogs
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all_blogs(cls):
        '''
        Function that queries the databse and returns all the blogs
        '''
        blogs = Blog.query.all()
        return blogs
    @classmethod
    def get_blogs_by_category(cls,cat_id):
        '''
        Function that queries the databse and returns blogs based on the
        category passed to it
        '''
        return blog.query.filter_by(category_id= cat_id)

class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    comment= db.Column(db.String)
    blog_id = db.Column(db.Integer,db.ForeignKey('blog.id'))
    username =  db.Column(db.String)
    votes= db.Column(db.Integer)


    def save_comment(self):
        '''
        Function that saves comments
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def clear_comments(cls):
        Comment.all_comments.clear()

    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(blog_id=id).all()

        return comments

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key=True)
    name_of_category = db.Column(db.String(255))

    def __repr__(self):
        return f'User {self.name}'




class Subscriber(db.Model):
    __tablename__='subscribers'

    id=db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(255),unique=True,index=True)

    def save_subscriber(self):
        db.session.add(self)
        db.session.commit()


class BlogCategory(db.Model):
    '''
    Function that defines different categories of pitches
    '''
    __tablename__ ='blog_categories'


    id = db.Column(db.Integer, primary_key=True)
    name_of_category = db.Column(db.String(255))
    category_description = db.Column(db.String(255))

    @classmethod
    def get_categories(cls):
        '''
        This function fetches all the categories from the database
        '''
        categories = BlogCategory.query.all()
        return categories
