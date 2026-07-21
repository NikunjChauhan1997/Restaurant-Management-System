import database.db
import time
from init import get_place_order_details
from init import application_init
from init import place_order
from init import order_details
from flask import Flask, redirect, url_for, Blueprint, jsonify, render_template

countdown_timer = None
last_order_timer = 0
last_order_id = 0

restaurant_app = Flask(__name__)

@restaurant_app.route("/")
def home():
    return {
        "message":"Welcome to Restaurant App"
    }

@restaurant_app.route("/order", methods=["GET"])
def order():

    application_init()

    place_order()

    return redirect(
        url_for("order_countdown")
    )

@restaurant_app.route("/order_history", methods=["GET"])
def order_history():

    application_init()

    user_order_history = order_details()

    return {
        "order_details": user_order_history
    }

@restaurant_app.route("/order_countdown", methods=["GET"])
def order_countdown():
    return render_template("index.html")

@restaurant_app.route("/order_timer", methods=["GET"])
def order_timer():

    global last_order_timer
    global countdown_timer
    global last_order_id

    order_id = get_place_order_details()

    get_order_timer = database.db.db_get_order_details_and_timer(order_id - 1)

    current_order_timer = time.time()

    if ((countdown_timer is None) or (countdown_timer <= 0 and last_order_id != (order_id - 1))):
        countdown_timer = get_order_timer["orders"][0]["eta"]
        last_order_timer = current_order_timer
        last_order_id = order_id - 1

    if current_order_timer - last_order_timer >= 1 and countdown_timer > 0:
        countdown_timer -= 1
        last_order_timer = current_order_timer

    return {
        "order_details": get_order_timer,
        "order_timer": countdown_timer
    }

if __name__ == "__main__" :
    restaurant_app.run(debug=True)