from init import application_init
from init import place_order
from init import order_details

app_running = True

print("=========== Welcome ===========")

while app_running:
	
	print("1) Place the order.")
	print("2) Order Details.")
	print("3) Exit.")

	try:
		user_input = int(input("Enter your choice: "))
	except ValueError:
		print("Invalid input! Please enter a number (1-3).")

	if(user_input == 1):
		application_init()
		place_order()
	elif(user_input == 2):
		application_init()
		order_details()
	elif user_input == 3 :
		app_running = False
	else:
		print("Wrong choice! Please select 1, 2, or 3.")

print("==== Thank You Visit Again ====")