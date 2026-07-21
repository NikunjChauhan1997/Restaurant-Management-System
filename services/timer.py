import threading
import time
import database.db
from services.logger_service import log_info

class Order_Timer:

    def __init__(self):
        self.order_threads = {}
        self.stop_events = {}

    def order_timer(self, order_id, order_obj, client_id, order_prepare_time, stop_event):
        try:
            log_info("Started Thread: {}" .format(threading.current_thread().name))

            order_obj.set_order_status_details(client_id, order_id, "Preparing")
            database.db.db_update_order_status(client_id, order_id, "Preparing")
            database.db.db_update_order_time(order_id, order_prepare_time)

            while (order_prepare_time > 0 and not stop_event.is_set()):
                log_info("Order {} : {} min".format(order_id, order_prepare_time))
                time.sleep(60)
                order_prepare_time -= 1
                database.db.db_update_order_time(order_id, order_prepare_time)

            if stop_event.is_set():
                log_info("Order {} cancelled".format(order_id))
                order_obj.set_order_status_details(client_id, order_id, "cancel")
                database.db.db_update_order_status(client_id, order_id, "cancel")
                return

            order_obj.set_order_status_details(client_id, order_id, "Ready")
            database.db.db_update_order_status(client_id, order_id, "Ready")
            time.sleep(5)

            if stop_event.is_set():
                log_info("Order {} cancelled".format(order_id))
                order_obj.set_order_status_details(client_id, order_id, "cancel")
                database.db.db_update_order_status(client_id, order_id, "cancel")
                return

            order_obj.set_order_status_details(client_id, order_id, "Delivered")
            database.db.db_update_order_status(client_id, order_id, "Delivered")
            time.sleep(5)

            if stop_event.is_set():
                log_info("Order {} cancelled".format(order_id))
                order_obj.set_order_status_details(client_id, order_id, "cancel")
                database.db.db_update_order_status(client_id, order_id, "cancel")
                return

            order_obj.set_order_status_details(client_id, order_id, "Completed")
            database.db.db_update_order_status(client_id, order_id, "Completed")

            log_info("Order {} completed".format(order_id))

        except Exception as e:

            log_info("Thread Error:{}".format(e))

        finally:

            self.order_threads.pop(order_id,None)

            self.stop_events.pop(order_id,None)

            log_info("Thread Removed:{}".format(order_id))

    def start_order_timer(self, order_id, order_obj, client_id, order_prepare_time):

        if (order_id in self.order_threads and self.order_threads[order_id].is_alive()):
            log_info("Order {} already running".format(order_id))
            return

        stop_event = threading.Event()

        thread = threading.Thread(target=self.order_timer, args=(order_id, order_obj, client_id, order_prepare_time, stop_event),
            name="Order-" + str(order_id), daemon=False)

        self.order_threads[order_id] = thread
        self.stop_events[order_id] = stop_event

        thread.start()

        log_info("Running Threads:{}".format(threading.active_count()))

    def stop_order_timer(self, order_id):

        if order_id not in self.stop_events:
            log_info("Order not running")
            return

        self.stop_events[order_id].set()

        log_info("Stopping Order {}".format(order_id))