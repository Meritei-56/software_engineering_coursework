from datetime import datetime, timedelta
import geopy.distance
import sched
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

class My_Time_Planner():
    def __init__(self):
        self.tasks = []
        self.current_location = None
        self.geolocator = Nominatim(user_agent="my_time_planner")

    def create_tasks_diary(self, task_name, scheduled_time, location):
        # Check if the task with the same name already exists
        for task in self.tasks:
            if task['task'] == task_name:
                # Update the existing task entry
                task['time'] = scheduled_time
                task['location'] = location
                return
         
        # If the task does not exist, create a new entry
        self.tasks.append({'task': task_name, 'time': scheduled_time, 'location': location})

    def set_current_location(self, location):
        #
        self.current_location = location
    
    def determine_distance_to_taskLocation(self, task_location):
        if self.current_location:
            distance = geopy.distance.distance(task_location, self.current_location).km
            return distance
        return None

    def check_time_to_event(self):
        #please readjust this method as well to work
        current_time = datetime.now()
        for task in self.tasks:
            task_time = datetime.strptime(task['time'], "%Y-%m-%d %H:%M")
            if current_time > task_time:
                continue
            
            if task['location']:
                distance = self.determine_distance_to_taskLocation(task['location'])
                if distance is not None:
                    travel_time = timedelta(minutes=distance * 10)  # Assuming 10 minutes per kilometer
                    time_to_leave = task_time - travel_time
                    if current_time > time_to_leave:
                        self.provide_updates(f"It's time to leave for {task['task']} at {task['location']}", timedelta(minutes=15))
            else:
                if current_time > task_time - timedelta(minutes=15):
                    self.provide_updates(f"Upcoming task: {task['task']} at {task['time']}", timedelta(seconds=1))

    def monitor_location(self, interval=60):
        #this method is still not working, work
        while True:
            try:
                location = self.get_current_gps_location()
                if location:
                    self.set_current_location(location)
            except GeocoderTimedOut:
                print("Geocoding service timed out. Retrying...")
            time.sleep(interval)

    def get_current_gps_location(self):
        # Use geopy to get current GPS coordinates
        current_location = self.geolocator.geocode("my location")
        if current_location:
            return (current_location.latitude, current_location.longitude)
        return None

    def provide_updates(self, message, delay=timedelta(seconds=0)):
        s = sched.scheduler(time.time, time.sleep)
        s.enter(delay.total_seconds(), 1, print, argument=(message,))
        s.run()
    
    def check_schedule(self):
        # Sort tasks by scheduled time before printing
        sorted_tasks = sorted(self.tasks, key=lambda x: datetime.strptime(x['time'], "%Y-%m-%d %H:%M"))

        print("List of Tasks:")
        for task in sorted_tasks:
            print(f"Task: {task['task']}, Time: {task['time']}, Location: {task['location']}")

    def advise_on_routesToTasklocation(self):
        #integrate google maps API to provide route directions 
        pass

    def cleanUp(self):
        pass


def main():
    p = My_Time_Planner()
    print("Add tasks to your planner. Enter 'done' to finish.")

    # Start location monitoring in a separate thread
    import threading
    location_thread = threading.Thread(target=p.monitor_location, daemon=True)
    location_thread.start()

    while True:
        task_name = input("Enter task name: ")
        if task_name.lower() == 'done':
            break
        
        scheduled_time = input("Enter scheduled time (YYYY-MM-DD HH:MM): ")
        location = input("Enter location: ")

        # Add task to the planner
        p.create_tasks_diary(task_name, scheduled_time, location)

    # After adding tasks, print the list of tasks organized by scheduled time
    p.check_schedule()
    #p.check_time_to_event()    -- needs further code readjustments for this step to work

if __name__ == "__main__":
    main()



