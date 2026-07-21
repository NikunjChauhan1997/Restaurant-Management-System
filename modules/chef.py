from services.logger_service import log_info
from services.logger_service import log_error

class Chef:

	def __init__(self, Restaurant_Name, Total_Chef):
		self.Restaurant_Name = Restaurant_Name
		self.Total_Chef = Total_Chef
		self.Chef = {}
		for chef_count in range(1, Total_Chef + 1):
			self.Chef[chef_count] = 0

	def get_chef_details(self,Restaurant_Name):
		if(self.Restaurant_Name == Restaurant_Name):
			log_info(f"Restaurant Name: {self.Restaurant_Name}")
			log_info(f"Total Number of Chef: {self.Total_Chef}")
			log_info(f"{'Chef':<5}{'Time'}")
			log_info(f"{'-'*4:<5}{'-'*4}")
			for chef, chef_busy_time in self.Chef.items():
				log_info(f"{chef:<5}{chef_busy_time:<5}mins busy")
			log_info("\n")
		else:
			log_error("In-Valid Restaurant Name...\n")
	
	def get_chef_time_details(self,Restaurant_Name, chef_no):
		if(self.Restaurant_Name == Restaurant_Name):
			return self.Chef[chef_no]
		else:
			log_error("In-Valid Restaurant Name...")

	def set_chef_details(self,Restaurant_Name):
		if(self.Restaurant_Name == Restaurant_Name):
			while True:
				print(f"1) Add New Chef for '{self.Restaurant_Name}'.")
				print(f"2) Remove Chef for '{self.Restaurant_Name}'.")
				print("3) Exit.")
				user_choice = int(input("Enter Your Choice:"))
				print(f"Current chef available at {self.Restaurant_Name} Restaurant: {list(self.Chef.keys())}")
				if(user_choice == 1):
					self.Total_Chef += 1
					self.Chef[self.Total_Chef] = 0
				elif(user_choice == 2):
					chef_no = int(input("Please select the chef:"))
					self.Total_Chef -= 1
					self.Chef.pop(chef_no)
				else:
					break
		else:
			log_error("In-Valid Restaurant Name...")

	def set_chef_time_details(self,Restaurant_Name, chef_no, chef_busy_time):
		if(self.Restaurant_Name == Restaurant_Name):
			self.Chef[chef_no] = chef_busy_time
		else:
			log_error("In-Valid Restaurant Name...")