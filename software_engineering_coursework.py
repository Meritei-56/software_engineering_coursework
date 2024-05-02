from datetime import datetime, timedelta
import geopy.distance
import sched
import time

class My_Time_Planner():
    # A class to manage tasks diary creation, distance calculation, and provision of timely updates
    def __init__(self):
        self.tasks = []
        self.current_location = None

    def create_tasks_diary(self, task, time, location):
        self.tasks.append({'task': task, 'time': time, 'location': location})
    
    def set_current_location(self, location):
        self.current_location = location  # Correctly assign to self.current_location
    
    def determine_distance_to_taskLocation(self):
        pass

    def estimate_timeTaken_to_taskLocation(self):
        pass
    
    def check_time_to_event(self):
        pass

    def provide_updates(self, message, delay):
        s = sched.scheduler(time.time, time.sleep)
        s.enter(delay.total_seconds(), 1, print, argument=(message,))
        s.run()
    
    def check_schedule(self):
        current_time = datetime.now()
        for task in self.tasks:
            task_time = datetime.strptime(task['time'], "%Y-%m-%d %H:%M")
            if current_time > task_time:
                continue
            if task['location'] and self.current_location:
                distance = geopy.distance.distance(task['location'], self.current_location).km
                travel_time = timedelta(minutes=distance * 10)  # Assuming 10 minutes per kilometer
                time_to_leave = task_time - travel_time
                if current_time > time_to_leave:
                    self.provide_updates(f"It's time to leave for {task['task']} at {task['location']}", timedelta(minutes=15))
            else:
                if current_time > task_time - timedelta(minutes=15):
                    self.provide_updates(f"Upcoming task: {task['task']} at {task['time']}", timedelta(seconds=1))

    def advise_on_routesToTasklocation(self):
        pass

    def cleanUp(self):
        pass
