                                     +-------------------------------+
                                     |                               |
                                     |         TodoModel             |
                                     |       (model.py)              |
                                     |                               |
                                     +---------------^---------------+
                                                     |
                                     +---------------|---------------+
                                     |               |               |
                        +------------v---+ +---------v---------+ +-----v----------+
                        |                | |                   | |                |
                        |    TodoView    | |  TodoController   | |    tkinter     |
                        |   (view.py)    | |  (controller.py) | |                |
                        |                | |                   | |                |
                        +----------------+ +-------------------+ +----------------+
                                   |                 |                    |
                +------------------|-----------------|--------------------|------------------+
                |                  |                 |                    |                  |
       +--------v--------+ +-------v--------+ +------v--------+ +-------v--------+ +------v-------+
       |                 | |                | |               | |               | |              |
       |  Task Entry     | | Add Task Btn   | |   Add Task    | | Remove Task   | |  Listbox     |
       |  Entry Widget   | | Button Widget  | |   Method      | |  Method       | |  Widget      |
       |                 | |                | |               | |               | |              |
       +-----------------+ +----------------+ +---------------+ +---------------+ +--------------+

Algorithms:
- TodoModel:
  - add_task(task): Appends a task to the list of tasks.
  - remove_task(task): Removes a task from the list of tasks.
  - get_tasks(): Retrieves the list of tasks.

- TodoController:
  - __init__(): Initializes the TodoModel and TodoView.
  - add_task(task): Passes the task to the TodoModel's add_task() method.
  - remove_task(task): Passes the task to the TodoModel's remove_task() method.
  - get_tasks(): Calls the TodoModel's get_tasks() method to retrieve tasks.

- TodoView:
  - add_task(): Gets the task from the entry widget, passes it to the TodoController's add_task() method, and refreshes the task list.
  - refresh_tasks(): Clears the task listbox and repopulates it with tasks retrieved from the TodoController.
