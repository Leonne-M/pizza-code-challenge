#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response,jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)



@app.route("/restaurants")
def get_allrestaurants():
    restaurants=[]
    list_restaurants=Restaurant.query.all()
    for restaurant in list_restaurants:
        restaurants.append({"id":restaurant.id ,"name":restaurant.name ,"adress":restaurant.address})
    return jsonify(restaurants)

@app.route("/restaurants/<int:id>",methods=['GET','DELETE'])
def get_restaurants(id):
 if request.method=='GET':
  restaurant=Restaurant.query.get(id)
  if restaurant:
    return jsonify(restaurant)
  else:
    return jsonify({"error":"Restaurant not found"}),404
 else:
    restaurant=Restaurant.query.get(id)
    if restaurant:
     db.session.delete(restaurant)
     db.session.commit()
     return jsonify({"message":"Success"}),200
    else:
      return jsonify({"error":"Restaurant not found"}),404
    

@app.route("/pizzas")
def get_pizzas():
    pizzas=[]
    list_pizzas=Pizza.query.all()
    for pizza in list_pizzas:
        pizzas.append({"id":pizza.id ,"name":pizza.name ,"ingredients":pizza.ingredients })
    return jsonify(pizzas)

@app.route("/restaurant_pizzas",methods=["POST"])
def add_pizzas():
   price=request.form['price']
   restaurant_id=request.form['restaurant_id']
   pizza_id=request.form['pizza_id']
   rest=RestaurantPizza(price=price,restaurant_id=restaurant_id,pizza_id=pizza_id)
   db.session.add(rest)
   db.session.commit()
   pizza=Pizza.query.get(pizza_id)
   restaurant=Restaurant.query.get(restaurant_id)
   return jsonify({"id":rest.id,'pizza':pizza,'pizza_id':pizza_id,'price':price,'restaurant':restaurant,'restaurant_id':restaurant_id})
   

 


if __name__ == "__main__":
    app.run(port=5555, debug=True)
