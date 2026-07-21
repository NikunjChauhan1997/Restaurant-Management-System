from services.logger_service import log_info

class Kitchen_Scheduler:
	def __init__(self):
		self.next_available_chef = 0

	def get_next_available_chef(self,Chef_Obj):
		self.next_available_chef = min(Chef_Obj.Chef, key = Chef_Obj.Chef.get)
		log_info("Next Available Chef For Prepare the Order: {}".format(self.next_available_chef))
