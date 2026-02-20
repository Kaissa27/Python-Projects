import sys

def add_task(tasks):
    title = input("Task description: ").strip()
    priority = input("Priority (High/Med/Low): ").strip().capitalize()
    tasks.append({"title": title, "priority": priority, "done": False})
    print("Task added.")

def mark_complete(tasks):
    view_tasks(tasks)
    try:
        idx = int(input("Enter task number to complete: ")) - 1
        if 0 <= idx < len(tasks):
            tasks[idx]["done"] = True
            print(f"Task '{tasks[idx]['title']}' marked as done.")
        else:
            print("Invalid number.")
    except ValueError:
        print("Please enter a number.")

def view_tasks(tasks):
    if not tasks:
        print("No tasks found.")
        return

    print(f"\n{'#':<3} | {'Task':<20} | {'Priority':<10} | {'Status'}")
    print("-" * 45)
    
    for i, task in enumerate(tasks, 1):
        status = "Completed" if task["done"] else "Pending"
        print(f"{i:<3} | {task['title']:<20} | {task['priority']:<10} | {status}")

def main():
    todo_list = []
    
    while True:
        print("\nTask Manager")
        print("1. Add Task")
        print("2. Mark Task Complete")
        print("3. View All Tasks")
        print("4. Exit")
        
        choice = input("Select: ")
        
        if choice == "1":
            add_task(todo_list)
        elif choice == "2":
            mark_complete(todo_list)
        elif choice == "3":
            view_tasks(todo_list)
        elif choice == "4":
            sys.exit()
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    main()