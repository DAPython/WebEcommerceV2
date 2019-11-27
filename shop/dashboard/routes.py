from flask import render_template, session, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from shop.models import Product, User, Category
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators
from shop import app, db, bcrypt
import sqlite3
import os


class Categories(Form):
    name_category = StringField('Name', [validators.DataRequired()])
    image_category = StringField('Image', [validators.DataRequired()])
    description_category = StringField(
        'Description', [validators.DataRequired()])



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_authenticated and current_user.role != 'admin':
        return redirect(url_for('index'))
    return render_template('dashboard/index.html')


@app.route('/category', methods=['GET', 'POST'])
def category():
   if request.method == "POST":
      name = request.form['name']
      image = request.form['image']
      des = request.form['description']
      with sqlite3.connect('shop/database.db') as con:
         try:
            cur = con.cursor()
            cur.execute('INSERT INTO category(name_category, image_category, description_category) VALUES (?,?,?)', (name, image, des))
            con.commit()
         except:
            con.rollback()
      con.close()
   return render_template('dashboard/category.html')


@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
   if request.method == "POST":
      name = request.form['name']
      image = request.form['image']
      price = request.form['price']
      discount = request.form['discount']
      des = request.form['description']
      stock = request.form['stock']
      with sqlite3.connect('shop/database.db') as con:
         try:
            cur = con.cursor()
            cur.execute('INSERT INTO product(name_product, image_product, price, discount, description_product, stock) VALUES (?,?,?,?,?,?)', (name, image, price, discount, des, stock))
            con.commit()
         except:
            con.rollback()
      con.close()
   return render_template('dashboard/addproduct.html')



@app.route('/user')
def user():
    user = User.query.all()
    return render_template('dashboard/user.html', user=user)


@app.route('/product')
def product():
    title = 'Product | Admin'
    product = Product.query.all()
    return render_template('dashboard/product.html', product=product, title=title)
