# To-Do List Application

def show_instructions():
    print("Welcome to the To-Do List Application!")
    print("Commands:")
    print("  add [task] - Add a new task")
    print("  remove [task number] - Remove a task by its number")
    print("  view - View all tasks")
    print("  quit - Exit the application")

def add_task(task_list, task):
    task_list.append(task)
    print(f'Task "{task}" added to the list.')

def remove_task(task_list, task_number):
    if 0 <= task_number < len(task_list):
        removed_task = task_list.pop(task_number)
        print(f'Task "{removed_task}" removed from the list.')
    else:
        print("Invalid task number.")

def view_tasks(task_list):
    if not task_list:
        print("Your to-do list is empty.")
    else:
        print("Your tasks:")
        for index, task in enumerate(task_list):
            print(f"{index}. {task}")

def main():
    task_list = []
    show_instructions()

    while True:
        command = input("\n> ").strip().lower().split(maxsplit=1)
        
        if len(command) == 0:
            continue
        
        action = command[0]

        if action == "add":
            if len(command) > 1:
                add_task(task_list, command[1])
            else:
                print("Please specify a task to add.")
        
        elif action == "remove":
            if len(command) > 1 and command[1].isdigit():
                remove_task(task_list, int(command[1]))
            else:
                print("Please specify a valid task number to remove.")
        
        elif action == "view":
            view_tasks(task_list)
        
        elif action == "quit":
            print("Thanks for using the To-Do List Application!")
            break
        
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
