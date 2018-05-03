from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, MenuItem, Restaurant



engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurants(restaurant_id):
    rest_name = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return render_template('menu.html', restaurant=rest_name, items=items)


@app.route('/restaurants/<int:restaurant_id>/menu/json')
def restaurantMenu(restaurant_id):
    rest_name = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=rest_name.id).all()
    return jsonify(MenuItems=[item.serialize for item in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/json')
def oneMenuJson(restaurant_id, menu_id):
    rest_name = session.query(Restaurant).filter_by(id=restaurant_id).one()
    one_menu_item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(OneItem=[one_menu_item.serialize])


@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    rest_name = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        new_item_details = MenuItem(name=request.form['name'], description=request.form['description'], price=request.form['price'], restaurant_id=restaurant_id)
        session.add(new_item_details)
        session.commit()
        flash("New Item created")
        return redirect(url_for('restaurants', restaurant_id=restaurant_id))
    else:
        return render_template('create_new.html', restaurant=rest_name)

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    rest_name = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item_to_edit = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method=='POST':
        item_to_edit.name = request.form['name']
        session.add(item_to_edit)
        session.commit()
        flash('Item is edited')
        return redirect(url_for('restaurants', restaurant_id=restaurant_id))
    else:
        return render_template('edit_menu_item.html', restaurant=rest_name, menu_item=item_to_edit)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    item_to_delete = session.query(MenuItem).filter_by(id=menu_id).one()
    rest_name = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method=='GET':
        return render_template('delete_item.html', restaurant=rest_name, menu_item=item_to_delete)
    else:
        session.delete(item_to_delete)
        session.commit()
        flash('Item is deleted')
        return redirect(url_for('restaurants', restaurant_id=restaurant_id))





if __name__ == '__main__':
    app.secret_key='vishwas'
    app.debug = True
    app.run('0.0.0.0', port=5000)