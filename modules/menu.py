from services.logger_service import log_info
from services.logger_service import log_error

class Restaurant_Menu:

	def __init__(self, Restaurant_Name):
		self.Restaurant_Name = Restaurant_Name

		if(self.Restaurant_Name == Restaurant_Name):
			self.Restaurant_Menu = {}

	def set_restaurant_menu(self, Restaurant_Name, Restaurant_Menu_List):
		if(self.Restaurant_Name == Restaurant_Name):
			self.Restaurant_Menu.update(Restaurant_Menu_List)

		elif(self.Restaurant_Name == Restaurant_Name):
			self.Restaurant_Menu = Restaurant_Menu_List

		else:
			log_error("In-valied Restaurant Name...")

	def update_restaurant_details(self):
		while True:

			new_restaurant_menu_list = {}

			print("1) Add New Restaurant and Menu.")
			print("2) Change Existing Restaurant Menu Details.")
			print("3) Remove Restaurant Menu.")
			print("4) Exit.")
			
			user_choice = int(input("Enter Your Choice From (1, 2, 3 or 4): "))
			
			if (user_choice == 1 or user_choice == 2):

				print("Available Restaurant List:")
				for count, Restaurant_List in enumerate(list(restaurant_menu_obj.keys()),start=1):
					print("{}) {}".format(count,Restaurant_List))

				restaurant_name = input("Enter the Restaurant Name: ")

				if (user_choice == 2):
					get_restaurant_menu(restaurant_name)
				else:
					restaurant_menu_obj[restaurant_name] = Restaurant_Menu(restaurant_name)

				print(f"Enter the Restaurant Menu For Restaurant: '{restaurant_name}'")

				while True:
					menu_item = input("Enter the Menu Item: ")

					if (menu_item.lower() == "exit"):
						break
					menu_prepare_time = input("Menu Prepare Time: ")

					if(menu_item == "" or menu_prepare_time == ""):
						continue
					new_restaurant_menu_list[menu_item] = int(menu_prepare_time)
					print("{}\n".format(new_restaurant_menu_list))
				restaurant_menu_obj[restaurant_name].set_restaurant_menu(restaurant_name,new_restaurant_menu_list)
				print("\n")

			elif (user_choice == 3):
				
				print("Available Restaurant List:")
				for count, Restaurant_List in enumerate(list(restaurant_menu_obj.keys()),start=1):
					print("{}) {}".format(count,Restaurant_List))

				restaurant_name = input("Enter the Restaurant Name: ")

				get_restaurant_menu(restaurant_name)

				while True:
					print("1) Remove the restaurant menu items.")
					print("2) Remove the restaurant menu.")
					print("3) Exit.")
					user_choice = int(input("Enter Your Choice: "))
					if(user_choice == 1):
						print(f"{restaurant_menu_obj[restaurant_name].Restaurant_Menu} \n")
						res_menu_dele_item = input("Enter the menu items for delete: ")
						restaurant_menu_obj[restaurant_name].Restaurant_Menu.pop(res_menu_dele_item)
						log_info(f"Updated Menu List of the'{restaurant_menu_obj[restaurant_name].Restaurant_Name}': {restaurant_menu_obj[restaurant_name].Restaurant_Menu} \n")
						log_info("\n")
					elif(user_choice == 2):
						restaurant_menu_obj[restaurant_name].Restaurant_Menu.clear()
						log_info(f"Updated Menu List of the'{restaurant_menu_obj[restaurant_name].Restaurant_Name}': {restaurant_menu_obj[restaurant_name].Restaurant_Menu} \n")
						break
					else:
						break
			else:
				break
	def get_restaurant_menu(self, Restaurant_Name):
		if(self.Restaurant_Name == Restaurant_Name):
			print("Restaurant_Name: {}".format(Restaurant_Name))
			print("Menu: {}".format(list(self.Restaurant_Menu.keys())))
			return (self.Restaurant_Menu.keys())
		else:
			log_error("In-valied Restaurant Name...")