from flask import render_template,request,redirect,url_for,abort
from . import main
from datetime import datetime
from ..email import mail_message
from ..models import User,Blog,Role,Comment,BlogCategory,Subscriber
from flask_login import login_required,current_user
from .. import db,photos
from .forms import UpdateProfile,CommentsForm,BlogForm, SubscriberForm


@main.route('/')
def index():
    '''
    View root page function that returns the index page and it's data
    '''

    blogs= Blog.query.all()
    form = SubscriberForm()
    if form.validate_on_submit():
        email = form.email.data

        new_subscriber=Subscriber(email=email)
        new_subscriber.save_subscriber()

        mail_message("Subscription Received","email/welcome_subscriber",new_subscriber.email,subscriber=new_subscriber)


    title = 'Home - Welcome to the best Blogging Websit online'
    search_blog = request.args.get('blog_query')
    blogs = Blog.get_all_blogs()
    return render_template('index.html',title = title,blogs = blogs, subscriber_form= form)



@main.route('/business/blogs/')
def business():
    '''
    View root page function that returns the index page and its data
    '''
    blogs= Blog.get_all_blogs()
    title = 'Home - Welcome to The best Blogging Website Online'
    return render_template('business.html', title = title, blogs= blogs )


@main.route('/fashion/blogs/')
def fashion():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Fashion'

    blogs= Blog.get_all_blogs()

    return render_template('fashion.html', title = title, blogs= blogs )


@main.route('/product/blogs/')
def entertainment():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Entertainment'
    blogs= Blog.get_all_blogs()
    return render_template('entertainment.html', title = title, blogs= blogs )



@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/new_blog', methods = ['GET','POST'])
@login_required
def newblog():
    form = BlogForm()
    if form.validate_on_submit():
        title = form.title.data
        blog= form.blog.data

        #Updated blog instance
        new_blog= Blog(title = title, blog = blog,user_id=current_user.id)
        print(new_blog)

        #save blog instance
        new_blog.save_blog()
        subscribers = Subscriber.query.all()
        for subscriber in subscribers:

            mail_message("New Blog ","email/new_blog",subscriber.email,blog=new_blog)


        return redirect(url_for('main.index'))

    title = "View blogs"
    return render_template('new_blog.html',title = title, blog_form = form)


@main.route('/category/<int:id>')
def category(id):
    '''
    function that returns blogs based on the entered category id
    '''
    category = category.query.get(id)

    if category is None:
        abort(404)

    blogs_in_category = category(id)
    return render_template('category.html' ,category= category, blogs= blogs_in_category)

@main.route('/blog/comments/new/<int:id>',methods = ['GET','POST'])
@login_required
def new_comment(id):
    form = CommentsForm()
    # vote_form = UpvoteForm()
    if form.validate_on_submit():
        new_comment = Comment(blog_id =id,comment=form.comment.data,username=current_user.username)
        new_comment.save_comment()
        return redirect(url_for('main.index'))
    return render_template('new_comment.html',comment_form=form)
@main.route('/view/comment/<int:id>')
def view_comments(id):
    '''
    Function that returs  the comments belonging to a particular pitch
    '''
    comments = Comment.get_comments(id)
    return render_template('view_comments.html',comments = comments, id=id)

@main.route('/test/<int:id>')
def test(id):
    '''
    this is route for basic testing
    '''
    blog =Blog.query.filter_by(id=1).first()
    return render_template('test.html',blog= blog)
