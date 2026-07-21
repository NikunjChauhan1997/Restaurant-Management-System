import sqlite3
from services.logger_service import log_info
from services.logger_service import log_error

def get_connection():
	
	connection = sqlite3.connect("database/restaurant.db")

	return connection

def create_db():

	connect_db = get_connection()

	cursor = connect_db.cursor()

	connect_db.commit()

	connect_db.close()

	log_info("Data-base Created Successfully...")

def create_table():

	connect_db = get_connection()

	cursor = connect_db.cursor()

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS restaurant (
			restaurant_id INTEGER PRIMARY KEY AUTOINCREMENT,
			restaurant_name TEXT NOT NULL,
			restaurant_location TEXT NOT NULL,
			restaurant_contect_no TEXT NOT NULL,
			chef_count INTEGER NOT NULL,
			created_at DATETIME DEFAULT CURRENT_TIMESTAMP);
		''')

	cursor.execute("""
		CREATE TABLE IF NOT EXISTS restaurant_menu(
			restaurant_name TEXT NOT NULL,
			dish_name TEXT NOT NULL,
			prep_time INTEGER NOT NULL,
			PRIMARY KEY
			(restaurant_name, dish_name));
		""")

	cursor.execute("""
		CREATE TABLE IF NOT EXISTS chef(
			restaurant_name TEXT NOT NULL,
			total_chef INTEGER NOT NULL,
			chef_id TEXT NOT NULL,
			chef_busy_time INTEGER NOT NULL,
			PRIMARY KEY
			(restaurant_name, chef_id));
		""")

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS order_food (
			order_id INTEGER PRIMARY KEY AUTOINCREMENT,
			client_id INTEGER DEFAULT 1,
			order_status TEXT DEFAULT 'Pending',
			created_at DATETIME DEFAULT CURRENT_TIMESTAMP);
		''')

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS order_items (
			item_id INTEGER PRIMARY KEY AUTOINCREMENT,
			order_id INTEGER NOT NULL,
			order_dish TEXT NOT NULL,
			order_dish_qut INTEGER NOT NULL,
			estimated_time INTEGER NOT NULL,
			elapsed_time INTEGER DEFAULT 0,
			FOREIGN KEY(order_id)
			REFERENCES order_food(order_id));
		''')

	connect_db.commit()
	connect_db.close()
	log_info("Data-base Tables Created Successfully...")

def init_restaurant_table():

	connect_db = get_connection()

	cursor = connect_db.cursor()

	cursor.execute('''
		INSERT INTO restaurant(restaurant_name,
			restaurant_location,
			restaurant_contect_no,
			chef_count)
		VALUES("MoonWalk",
			"Anand",
			"7048458494",
			4)
		''')

	connect_db.commit()
	connect_db.close()
	log_info("Restaurant Table Init Successfully...")

def init_restaurant_menu_table():

	MENU = {"Burger": 10, "Pizza": 15, "Pasta": 12, "Sandwich": 5,
 "French Fries": 6, "Garlic Bread": 4, "Veg Wrap": 8, "Noodles": 10, "Fried Rice": 12,
 "Salad": 4, "Coffee": 2, "Tea": 2, "Milkshake": 5, "Ice Cream": 1, "Brownie": 3}

	MENU_ROWS = [("MoonWalk",dish,prep_time) for dish, prep_time in MENU.items()]

	connect_db = get_connection()

	cursor = connect_db.cursor()

	cursor.executemany("""
		INSERT OR IGNORE INTO restaurant_menu(restaurant_name,
			dish_name,
			prep_time)
		VALUES(
			?,?,?)
		""",
		MENU_ROWS)

	connect_db.commit()
	connect_db.close()
	log_info("Restaurant Menu Table Init Successfully...")

def init_chef_table():

	CHEF = {"1":0,"2":0,"3":0}

	CHEF_DETAILS = [("MoonWalk",3,chef_id,chef_busy_time) for chef_id, chef_busy_time in CHEF.items()]

	connect_db = get_connection()

	cursor = connect_db.cursor()

	cursor.executemany("""
		INSERT OR IGNORE INTO chef(restaurant_name,
			total_chef,
			chef_id,
			chef_busy_time)
		VALUES(
			?,?,?,?)
		""",
		CHEF_DETAILS)

	connect_db.commit()
	connect_db.close()
	log_info("Chef Table Init Successfully...")

def init_restaurant_order_food():

	connect_db = get_connection()

	cursor = connect_db.cursor()

	cursor.execute('''
		INSERT INTO order_food (
			client_id)
		VALUES
		(1)
		''')
	
	connect_db.commit()
	connect_db.close()
	log_info("Restaurant Table Init Successfully...")

def init_tables():

	init_restaurant_table()

	init_restaurant_menu_table()

	init_chef_table()

	init_restaurant_order_food()

	log_info("Data-base Tables Init Successfully...")

def db_get_restaurant_name():

	connect_db = get_connection()

	cursor = connect_db.cursor()

	cursor.execute('''
		SELECT DISTINCT restaurant_name
		FROM restaurant
		''')

	db_restaurant_list = [row[0] for row in cursor.fetchall()]

	connect_db.close()

	return db_restaurant_list

def db_get_restaurant_menu(restaurant_name):

	connect_db = get_connection()

	cursor = connect_db.cursor()

	cursor.execute('''
		SELECT
		dish_name,
		prep_time
		FROM restaurant_menu
		WHERE restaurant_name = ?
		''',
		(restaurant_name,)
		)

	menu = cursor.fetchall()
	connect_db.close()

	restaurant_menu_list = {dish: prepare_time for dish, prepare_time in menu}

	return restaurant_menu_list

def db_get_place_order_details():

	connect_db = get_connection()

	cursor = connect_db.cursor()

	cursor.execute('''
		SELECT
		*
		FROM order_food
		ORDER BY order_id DESC
		LIMIT 1
		''')
	
	db_place_order_details = cursor.fetchone()
	
	connect_db.close()

	return db_place_order_details

def db_get_chef_details(restaurant_name):

	connect_db = get_connection()

	cursor = connect_db.cursor()

	cursor.execute('''
		SELECT DISTINCT
		chef_count
		FROM restaurant
		WHERE restaurant_name = ?
		ORDER BY rowid DESC
		LIMIT 1
		''',
		(restaurant_name,)
		)
	
	db_chef_count = [row[0] for row in cursor.fetchall()]

	connect_db.close()

	return db_chef_count

def db_get_least_chef_busy_time(restaurant_name):

	connect_db = get_connection()

	cursor = connect_db.cursor()

	cursor.execute('''
		SELECT
		chef_id,
        chef_busy_time
        FROM chef
        WHERE restaurant_name = ?
        ORDER BY chef_busy_time ASC, chef_id ASC
        LIMIT 1
        ''',
        (restaurant_name,)
        )

	db_get_least_chef_busy_time = cursor.fetchone()

	connect_db.close()

	return db_get_least_chef_busy_time

def db_insert_order(ins_order_id, ins_order_dish,ins_estimated_time):

	connect_db = get_connection()

	cursor = connect_db.cursor()

	for db_order_dish, db_order_dish_qut in ins_order_dish.items():
		cursor.execute('''
			INSERT INTO order_items(
				order_id,
				order_dish,
				order_dish_qut,
				estimated_time)
			VALUES(?,?,?,?)
			''',
			(ins_order_id, db_order_dish, db_order_dish_qut, ins_estimated_time)
			)
	connect_db.commit()
	connect_db.close()
	init_restaurant_order_food()
	log_info("Order Details Inserted Into The Database Successfully...")

def db_update_chef_details(updb_restaurant_name, updb_new_busy_time, updb_chef_id):

	connect_db = get_connection()

	cursor = connect_db.cursor()

	cursor.execute('''
		UPDATE chef
			SET
			chef_busy_time = ?
			WHERE
			restaurant_name = ?
			AND chef_id = ?
			''',
			(updb_new_busy_time,updb_restaurant_name,updb_chef_id)
			)
	connect_db.commit()
	connect_db.close()
	log_info("Update chef busy time Details Into the Database Successfully...")

def db_update_order_time(updb_order_id, updb_remain_time):

	connect_db = get_connection()

	cursor = connect_db.cursor()

	cursor.execute('''
		UPDATE order_items
			SET
			elapsed_time = ?
			WHERE
			order_id = ?
			''',
			(updb_remain_time, updb_order_id)
			)
	connect_db.commit()
	connect_db.close()
	log_info("Update Order Time Details Into the Database Successfully...")

def db_update_order_status(updb_client_id,updb_order_id,updb_order_status):

	connect_db = get_connection()

	cursor = connect_db.cursor()

	cursor.execute('''
		UPDATE order_food
			SET
			order_status = ?
			WHERE
			client_id = ?
			AND order_id = ?
			''',
			(
			updb_order_status,
			updb_client_id,
			updb_order_id)
			)

	connect_db.commit()
	connect_db.close()
	log_info("Update Order Status Details Into the Database Successfully...")

def db_get_order():

	connect_db = get_connection()

	cursor = connect_db.cursor()

	cursor.execute('''
		SELECT
		of.client_id,
		of.order_id,
		oi.order_dish,
		oi.order_dish_qut,
		of.created_at,
		oi.estimated_time,
		of.order_status,
		oi.elapsed_time
		FROM order_food of
		INNER JOIN order_items oi
		ON of.order_id = oi.order_id
		''')
	order_details = cursor.fetchall()

	connect_db.close()

	log_info("Data-base Get Order Details Successfully...")

	return order_details

def db_get_order_details_and_timer(updb_order_id):

	connect_db = get_connection()

	cursor = connect_db.cursor()

	cursor.execute('''
    SELECT
        of.client_id,
        of.order_id,
        oi.order_dish,
        oi.order_dish_qut,
        of.created_at,
        oi.estimated_time,
        of.order_status,
        oi.elapsed_time
    FROM order_food of
    INNER JOIN order_items oi
        ON of.order_id = oi.order_id
    WHERE of.order_id = ?
    ''', (updb_order_id,))

	timer = cursor.fetchall()

	keys = ["client","order","dish","qty","created","eta","status","elapsed"]
	
	connect_db.close()

	return {"orders": [dict(zip(keys, row)) for row in timer]}
