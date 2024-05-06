from software_engineering_coursework import My_Time_Planner  # Import your My_Time_Planner class here

def main():
    # Initialize My_Time_Planner instance
    time_planner = My_Time_Planner()

    # Add tasks using create_tasks_diary method
    time_planner.create_tasks_diary("Meeting", "2024-05-10 15:00", "Office")
    time_planner.create_tasks_diary("Lunch", "2024-05-11 12:30", "Restaurant")
    time_planner.create_tasks_diary("Gym", "2024-05-12 18:00", "Fitness Center")

    # Print the list of tasks
    print("List of Tasks:")
    for task in time_planner.tasks:
        print(f"Task: {task['task']}, Time: {task['time']}, Location: {task['location']}")

if __name__ == "__main__":
    main()

