import database.db
from services.logger_service import log_info
from services.logger_service import log_error

class Order_Food:

	def __init__(self,Order_id,Client_Id):
		self.Order_id = Order_id
		self.Order_dish = {}
		self.Order_Status = "Pending"
		self.Client_Id = Client_Id
		self.order_dish_prepare_time = 0

	def set_order_details(self,Client_Id,Order_id,Order_dish,Order_Status):
		if(self.Client_Id == Client_Id and self.Order_id == Order_id):
			self.Order_dish.update(Order_dish)
			self.Order_Status = Order_Status
		else:
			log_error("In-Valied Client_Id and Order_Id...")

	def set_order_status_details(self,Client_Id,Order_id,Order_Status):
		if(self.Client_Id == Client_Id and self.Order_id == Order_id):
			self.Order_Status = Order_Status
		else:
			log_error("In-Valied Client_Id and Order_Id...")

	def get_order_details(self,Client_Id,Order_id):
		if(self.Client_Id == Client_Id and self.Order_id == Order_id):
			log_info("Order id: {}".format(self.Order_id))
			log_info("Order dish: {}".format(self.Order_dish))
			log_info("Order Status: {}".format(self.Order_Status))
			return (self.Order_id,self.Order_dish,self.Order_Status)
		else:
			log_error("In-Valied Client id or Order id...")

	def get_order_dish_prepare_time(self,Restaurant_Menu_Obj,Client_Id,Order_id):
		if(self.Client_Id == Client_Id and self.Order_id == Order_id):
			log_info("Order id: {}".format(self.Order_id))
			log_info("Order dish: {}".format(self.Order_dish))
			order_dish_prepare_time = sum([Restaurant_Menu_Obj.Restaurant_Menu.get(key,0) for key in (self.Order_dish.keys())])
			log_info("Order Prepare Dish Time: {}".format(order_dish_prepare_time))
			return (order_dish_prepare_time)
		else:
			log_error("In-Valied Order id...")
