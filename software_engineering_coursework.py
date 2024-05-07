from datetime import datetime, timedelta
import geopy.distance
import sched
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import json

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
                self.save_tasks_to_file()
                return
        
        # If the task does not exist, create a new entry
        self.tasks.append({'task': task_name, 'time': scheduled_time, 'location': location})
        self.save_tasks_to_file()

    def load_tasks_from_file(self, filename='tasks.json'):
        try:
            with open(filename, 'r') as f:
                self.tasks = json.load(f)
        except FileNotFoundError:
            print("No tasks file found. Starting with an empty list.")

    def save_tasks_to_file(self, filename='tasks.json'):
        with open(filename, 'w') as f:
            json.dump(self.tasks, f, indent=4)

    def check_time_to_event(self):
        #may be the distance to event location should be ignored at this point
        #remove the distance element and modify the code such that it checks the time to event within every two seconds (for demonstration)
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
    def provide_notifications(self, message, delay=timedelta(seconds=0)):
        #modify these method to provide notifications within every 2 seconds
        s = sched.scheduler(time.time, time.sleep)
        s.enter(delay.total_seconds(), 1, print, argument=(message,))
        s.run()

    def set_current_location(self, location):
        self.current_location = location

    def determine_distance_to_taskLocation(self, task_location):
        # Fetch the task location from the tasks list
        for task in self.tasks:
            if task['location'] == task_location:
                # Try to geocode the task location
                try:
                    task_geocode = self.geolocator.geocode(task_location)
                    if task_geocode:
                        task_coordinates = (task_geocode.latitude, task_geocode.longitude)
                        current_coordinates = self.current_location
                        if current_coordinates:
                            distance = geopy.distance.distance(task_coordinates, current_coordinates).km
                            return distance
                except GeocoderTimedOut:
                    print("Geocoding service timed out. Unable to determine distance.")
                    return None

        print(f"Location '{task_location}' not found or could not be geocoded.")
        return None
            

    def monitor_location(self, interval=60):
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
        current_location = self.geolocator.geocode("Manchester, Greater Manchester, England, United Kingdom")
        if current_location:
            return (current_location.latitude, current_location.longitude)
        return None


    
    def check_schedule(self):
        # Sort tasks by scheduled time before printing
        sorted_tasks = sorted(self.tasks, key=lambda x: datetime.strptime(x['time'], "%Y-%m-%d %H:%M"))

        print("List of Tasks:")
        for task in sorted_tasks:
            print(f"Task: {task['task']}, Time: {task['time']}, Location: {task['location']}")

    def advise_on_routesToTasklocation(self):
        # Integrate Google Maps API to provide route directions
        pass

    def cleanUp(self):
        #modify this method as well to ensure that the code closes appropriately and all records are saved
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

    # Fetch current GPS location (provide a more specific location)
    current_gps_location = p.get_current_gps_location()
    if current_gps_location:
        p.set_current_location(current_gps_location)

    # Calculate distance to a specific task location (e.g., "Manchester")
    task_location = "Manchester, Greater Manchester, England, United Kingdom"  # Example: Provide a more specific task location
    p.determine_distance_to_taskLocation(task_location)

    # Check time to events based on the current location and task distances
    p.check_time_to_event()

if __name__ == "__main__":
    main()



