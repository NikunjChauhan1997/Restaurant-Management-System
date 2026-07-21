from services.logger_service import log_info

class Estimater:
	
	def __init__(self):
		self.Order_Dish_Prep_Time = 0
		self.Current_Chef_Time = 0
		self.estimated_time = 0

	def get_estimated_time(self, Restaurant_Name, Restaurant_Menu_Obj, Order_Obj, Chef_Obj, Client_Id, Order_id, Chef_No):
		self.Order_Dish_Prep_Time = Order_Obj.get_order_dish_prepare_time(Restaurant_Menu_Obj, Client_Id, Order_id)
		self.Current_Chef_Time = Chef_Obj.get_chef_time_details(Restaurant_Name, Chef_No)
		self.estimated_time = self.Current_Chef_Time + self.Order_Dish_Prep_Time
		log_info("Estimated Time: {}".format(self.estimated_time))
		return (self.estimated_time)

