1. Project Title

  Restaurant Order Management System (Python + SQLite + FLASK)

2. Objective

- Order placement
- Menu management
- Chef assignment
- Order preparation timing
- Live order status tracking
- SQLite database storage
- HTTP API

3. System Architecture

	1. modules/
   		- menu.py -> Restaurant details and Restaurant menu
   		- order.py -> Order creation and tracking
   		- chef.py -> Chef management

	2. services/
   		- estimater.py -> Order time estimation
   		- kitchen.py -> Chef selection logic
   		- timer.py -> Order countdown logic
   		- logger_service.py -> Logs System logic (create and store log --> rstaurant.log)

	3. database/
   		- db.py -> SQLite database operations (In-Memory Database Storage)
   		- restaurant.db -> Database file

   	4. Restorent Project/
   		- init.py -> Init the application and database
   		- restaurant_app.py -> Restaurant App Main Application
   		- rstaurant.log -> Application Logs
   		- restaurant_app_api.py -> API For the home_page, place_order, order_detail_with_countdown, order_history.

   	5. templates/
   		- index.html -> For Start the Countdown Timer

4. Database Design

	Tables:

	1. restaurant
		- restaurant_id
		- restaurant_name
		- restaurant_location
		- restaurant_contect_no
		- chef_count
		- created_at

	2. restaurant_menu
		- restaurant_name
		- dish_name
		- prep_time

	3. chef
		- restaurant_name
		- total_chef
		- chef_id
		- chef_busy_time

	4. order_food
		- order_id
		- client_id
		- order_status
		- created_at

	5. order_items
		- item_id
		- order_id
		- order_dish
		- order_dish_qut
		- estimated_time
		- elapsed_time

5. System Workflow

	1. User selects restaurant
	2. Menu is displayed
	3. User places order (Place order multiple items and store at the same time supported)
	4. Order is stored in SQLite database
	5. System calculates estimated preparation time
	6. Chef is assigned based on minimum busy time
	7. Order timer starts using threading
	8. Order status updates automatically

6. Features

	- Multi-restaurant support
	- Dynamic menu system
	- Real-time order tracking
	- Chef load balancing
	- Thread-based order timer
	- SQLite database integration

7. Notes

	- Please Check the given below Order Count Logs will be available into the "rstaurant.log" file.
	  (2026-06-13 05:55:11,036 - INFO - Order 1: 4 min remaining,
	  2026-06-13 05:56:11,065 - INFO - Order 1: 3 min remaining...)

8. Pre-requesitions for application before the run...
	
	1. check the packages are available into your system using blow run the command on command prompt.
		pip show flask
		pip show markupsafe
		pip show jinja2

	2. If markupsafe package is exist then run below commands.
		pip uninstall markupsafe
		pip install markupsafe==2.0.1
		(Expected something close to: version = 2.0.1)

	3. If jinja2 package is exist then run below commands.
		pip install --upgrade jinja2
		pip show jinja2 
		(Expected something close to: version = 3.1.6)

	4. Run the below command for remove the flask and werkzeug package if available.
		pip uninstall flask werkzeug -y

	5. Run the below command for install the flask and werkzeug package for required version.
		pip install Flask==2.0.3 Werkzeug==2.0.3

	6. check the packages are available into your system using blow run the command on command prompt.
		pip show flask
		pip show werkzeug

9. Steps for Run the application.

	1. Open the command Prompt
	2. Goto the application folder
	3. Run the application restaurant_app_api.py using given below command
		python restaurant_app_api.py
	4. Open the browser and open the given below URL for homepage.
		http://127.0.0.1:5000/
	5. Open the browser and open the given below URL for place the order.
		http://127.0.0.1:5000/order
	6. Open the browser and open the given below URL for get the order history.
		http://127.0.0.1:5000/order_history
