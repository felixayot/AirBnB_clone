# AirBnB clone - The console

## About
In this project issued as part of the Software Engineering coursework at ALX Holberton, we were introduced to the steps of building a web application.

`The console` is the first step towards building our first full web application: `The AirBnB clone`. This first step is very important because we will use what we build during this project with all other following projects: HTML/CSS templating, database storage, API, front-end integration etc.

Each task here is linked and will enable us to perform the following tasks:

- put in place a parent class `BaseModel` to take care of the initialization, serialization and deserialization of our future instances.
- create a simple flow of serialization/deserialization: `Instance <-> Dictionary <-> JSON string <-> file`
- create all classes used for AirBnB (`User`, `State`, `City`, `Amenity`, `Place` and `Review`) that inherit from `BaseModel`.
- create the first abstracted storage engine of the project: File storage.
- create all unittests to validate all our classes and storage engine.

## Getting started on the console
- Ubuntu 20.04 LTS - Operating system required.
- Python version 3.8.5 and subsequent used.

## Usage
The console program is available in the `AirBnB_clone` repository under the module `console.py`. It's an executable Python script and you can run it on an Ubuntu 20.04 LTS terminal by invoking this command: `./console.py`.

### Examples of Usage
From the code snippet below, you can see that the console works in both interactive and non-interactive mode. There are various commands that you can use to manage data/file objects in the various classes created for the program.
When the `help` command is invoked, you can see all the available commands on the console. Use this command: `help <cmd>` as in `help` followed by the command without the angle brackets to view the documentation and the usage guide for each command.

```
f-ayot@mypc:~/AirBnB_clone$ ./console.py     # This is in an interactive mode
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  all  clear  count  create  destroy  help  quit  show  update

(hbnb) help create
 Creates a new instance of BaseModel, saves it
            (to the JSON file) and prints the id.
            Usage: create <class>

(hbnb) all HighClass
** class doesn't exist **
(hbnb) count User
0
(hbnb) show Place
** instance id missing **
(hbnb) create User
76673790-407c-4022-ae94-9feb5b085044
(hbnb) User.all()
["[User] (76673790-407c-4022-ae94-9feb5b085044) {'id': '76673790-407c-4022-ae94-9feb5b085044', 'created_at': datetime.datetime(2023, 8, 10, 14, 34, 40, 86778), 'updated_at': datetime.datetime(2023, 8, 10, 14, 34, 40, 86796)}"]
(hbnb) User.count()
1
(hbnb) Amenity.show("The Falls")
** no instance found **
(hbnb) User.destroy()
** instance id missing **
(hbnb) User.destroy("76673790-407c-4022-ae94-9feb5b085044")
(hbnb) User.count()
0
(hbnb) wrong cmd
*** Unknown syntax: wrong cmd
(hbnb)
f-ayot@mypc:~/AirBnB_clone$ echo "help" | ./console.py            # This is in a non-interactive mode
(hbnb)
Documented commands (type help <topic>):
========================================
EOF  all  clear  count  create  destroy  help  quit  show  update

(hbnb)
f-ayot@mypc:~/AirBnB_clone$
```

## Testing
Unit tests for all the class features for each module can be found on the repository using these paths:
- Unittests for `filestorage.py`: `tests/test_engine/test_filestorage.py`
- Unittests for `console.py`: `tests/test_console.py`
- Unittests for models module: `tests/test_models/test_*`

Run the tests using these commands: `python3 -m unittest discover tests` ,runs all the tests. Alternatively, use `python3 -m unittest tests/test_models/test_*` or `python3 -m unittest tests/test_engine/test_filestorage.py` to run specific tests for a given module.

## Authors
- ***Felix Ayot*** < felixayot@gmail.com >
- ***Abraham Maiko*** < bamjnr99@gmail.com >

## Acknowledgements
- ALX SE program provided the resources and project guidance. More information on this amazing program can be found through this [link](https://www.alxafrica.com/).
