import os
import modules.menu
import modules.order
import modules.chef
import services.estimater
import services.kitchen
import services.timer
import database.db
import time
from services.logger_service import log_info
from services.logger_service import log_error

db_file_name = "database/restaurant.db"

# init_restaurant_name = ""

# restaurant_menu = {}

please_order_order_id = 0

please_order_client_id = 0

total_chef = 0

def set_restaurant_name():

	# global init_restaurant_name

	db_init_restaurant_name = []

	'''
	get restaurant name form database
	'''
	db_init_restaurant_name = database.db.db_get_restaurant_name()

	for Restaurant_id, Restaurant_Name in enumerate(db_init_restaurant_name, start = 1):
		log_info("{}) {} Restaurant".format(Restaurant_id, Restaurant_Name))
		print("{}) {} Restaurant".format(Restaurant_id, Restaurant_Name))

	if len(db_init_restaurant_name) == 1 :
		init_restaurant_name = db_init_restaurant_name[0]
		log_info("Auto-selected Restaurant: {}".format(init_restaurant_name))
	else:
		while True:
			print("Select Restaurant to place order:")
			init_restaurant_name = input("Enter the Restaurant Name: ")
			if init_restaurant_name in db_init_restaurant_name :
				break
			else:
				log_error("Invalid restaurant name. Try again.")

	return init_restaurant_name

def get_restaurant_menu():

	# global restaurant_menu

	'''
	get restaurant menu form database
	'''

	restaurant_menu = database.db.db_get_restaurant_menu(init_restaurant_name)

	return restaurant_menu

def get_place_order_details():

	global please_order_order_id

	global please_order_client_id

	'''
	get place order details form database
	'''

	db_place_order_details = database.db.db_get_place_order_details()

	db_order_id, db_client_id, db_order_status, db_current_time_stamp = db_place_order_details

	please_order_order_id = db_order_id

	please_order_client_id = db_client_id

	return please_order_order_id

def get_chef_details():

	global total_chef

	total_chef = database.db.db_get_chef_details(init_restaurant_name)[0]

def init_database():

	'''
	create database
	'''
	database.db.create_db()

	'''
	create table
	'''
	database.db.create_table()

	'''
	init the database tables
	'''
	database.db.init_tables()
	
def init_modules(Restaurant_Name):
	
	'''
	init the restaurant menu module
	with default restaurant and menu

	restaurant_menu_obj[Restaurant_Name] = Restaurant_Menu(Restaurant_Name)
	'''
	restaurant_menu_obj = {}
	restaurant_menu_obj[init_restaurant_name] = modules.menu.Restaurant_Menu(init_restaurant_name)

	'''
	init the order food module

	order_obj[Client_id] = Order_Food(Order_id, Client_id)
	'''
	order_obj = {}
	order_obj[please_order_client_id] = modules.order.Order_Food(please_order_order_id,please_order_client_id)

	'''
	init the chef module

	with default chef details

	chef_obj[restaurant_name] = modules.chef.Chef(restaurant_name, total_chef_no)
	'''
	chef_obj = {}
	chef_obj[init_restaurant_name] = modules.chef.Chef(init_restaurant_name, total_chef)

	'''
	init the estimated time for order preparation

	estimater_obj[order_id] = services.estimater.Estimater()
	'''
	estimater_obj = {}
	estimater_obj[please_order_order_id] = services.estimater.Estimater()

	'''
	init the Kitchen Scheduler for order preparation
	kitchen_scheduler_obj[restaurant_name] = services.kitchen.Kitchen_Scheduler()
	'''
	kitchen_scheduler_obj = {}
	kitchen_scheduler_obj[init_restaurant_name] = services.kitchen.Kitchen_Scheduler()

	'''
	init the timer for get the order prepaired
	'''
	timer_manager = services.timer.Order_Timer()

	return (restaurant_menu_obj, order_obj, chef_obj, estimater_obj, kitchen_scheduler_obj, timer_manager)

def application_init():
	if not os.path.exists(db_file_name):
		init_database()
	set_restaurant_name()
	get_chef_details()
	get_place_order_details()

def place_order():

	order_items_list = {}

	rest_name = set_restaurant_name()

	print("\n===== PLACE ORDER =====")

	get_restaurant_menu()

	restaurant_menu_obj, order_obj, chef_obj, estimater_obj, kitchen_scheduler_obj, timer_manager = init_modules(rest_name)

	'''
	Get Restaurant Menu
	'''
	restaurant_menu_obj[init_restaurant_name].set_restaurant_menu(init_restaurant_name,restaurant_menu)

	while True:
		print("\nAvailable Menu:")
		restaurant_menu_obj[init_restaurant_name].get_restaurant_menu(init_restaurant_name)
		print("Select dish from menu below:")

		order_items = input("Enter Dish Name: ")

		if order_items in restaurant_menu:
			order_items_quantity = int(input("Enter the order quantity: "))
		else:
			continue

		order_items_list[order_items] = order_items_quantity

		user_confirm_order = input("Confirm Order (Y/N):")

		if (user_confirm_order == 'Y'):
			'''
			User Order details
			'''
			get_place_order_details()
			order_obj[please_order_client_id].set_order_details(please_order_client_id,please_order_order_id,order_items_list,"Pending")
			order_obj[please_order_client_id].get_order_dish_prepare_time(restaurant_menu_obj[init_restaurant_name],please_order_client_id,please_order_order_id)
			break
		else:
			continue

	chef, chef_busy_time = database.db.db_get_least_chef_busy_time(init_restaurant_name)

	'''
	Get Order from user and assign to the chef
	'''
	chef_obj[init_restaurant_name].set_chef_time_details(init_restaurant_name, chef, chef_busy_time)

	database.db.db_update_chef_details(init_restaurant_name, chef_busy_time, chef)

	'''
	Get the estimated time for prepare order
	'''
	estimater_obj[please_order_order_id].get_estimated_time(init_restaurant_name, restaurant_menu_obj[init_restaurant_name], order_obj[please_order_client_id], chef_obj[init_restaurant_name], please_order_client_id, please_order_order_id, chef)

	database.db.db_insert_order(please_order_order_id,order_items_list,estimater_obj[please_order_order_id].estimated_time)

	'''
	Get the next available chef for prepare order
	'''
	kitchen_scheduler_obj[init_restaurant_name].get_next_available_chef(chef_obj[init_restaurant_name])
	timer_manager.start_order_timer(
		order_obj[please_order_client_id].Order_id,
		order_obj[please_order_client_id],
		please_order_client_id,
		estimater_obj[please_order_order_id].get_estimated_time(init_restaurant_name, restaurant_menu_obj[init_restaurant_name], order_obj[please_order_client_id], chef_obj[init_restaurant_name], please_order_client_id, please_order_order_id, chef)
		)

def order_details():
	db_order_details = database.db.db_get_order()

	print("-" * 90)
	print(f"{'Client':<10}{'Order':<10}{'Dish':<15}{'Qty':<6}{'Created':<20}{'ETA':<6}{'Status':<10}{'Elapsed':<8}")
	print("-" * 90)

	for (client_id,order_id,order_dish,order_dish_qut,created_at,estimated_time,order_status,elapsed_time) in db_order_details:
		print(f"{client_id:<10}{order_id:<10}{order_dish:<15}{order_dish_qut:<6}{created_at:<20}{estimated_time:<6}{order_status:<10}{elapsed_time:<8}")
		print("-" * 90)

	log_info("Get Order Details Successfully...")

	keys = ["client","order","dish","qty","created","eta","status","elapsed"]

	return {"orders": [dict(zip(keys, row)) for row in db_order_details]}