#!/usr/bin/python3
"""contains the entry point of the command interpreter
   for the HBNB console.
"""
import cmd
import sys
import os
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


def parse_line(line):
    curly_braces = re.search(r"\{(.*?)\}", line)
    sq_brkts = re.search(r"\[(.*?)\]", line)
    if curly_braces is None:
        if sq_brkts is None:
            return [i.strip(",") for i in split(line)]
        else:
            tokens = split(line[:sq_brkts.span()[0]])
            item = [i.strip(",") for i in tokens]
            item.append(sq_brkts.group())
            return item
    else:
        tokens = split(line[:curly_braces.span()[0]])
        item = [i.strip(",") for i in tokens]
        item.append(curly_braces.group())
        return item


class HBNBCommand(cmd.Cmd):
    """Represents the HBNB console."""

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Amenity",
        "Place",
        "Review"
    }

    def emptyline(self):
        """Skips to the prompt when an empty line is encountered."""
        pass

    def default(self, line):
        """Overrides the default behaviour of the cmd module
           when an invalid input is encountered.
        """
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", line)
        if match is not None:
            argl = [line[:match.span()[0]], line[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(line))
        return False

    def do_create(self, line):
        """ Creates a new instance of BaseModel, saves it
            (to the JSON file) and prints the id.
            Usage: create <class>
        """
        parsed_line = parse_line(line)
        if len(parsed_line) == 0:
            print("** class name missing **")
        elif parsed_line[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(parsed_line[0])().id)
            storage.save()

    def do_show(self, line):
        """Prints the string representation of an instance based
           on the class name and id.
           Usage: show <class> <id> or <class>.show(<id>)
        """
        line_parsed = parse_line(line)
        objdict = storage.all()
        if len(line_parsed) == 0:
            print("** class name missing **")
        elif line_parsed[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(line_parsed) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(line_parsed[0], line_parsed[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(line_parsed[0], line_parsed[1])])

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id
           (save the change into the JSON file).
           Usage: destroy <class> <id> or <class>.destroy(<id>)
        """
        line_parsed = parse_line(line)
        objdict = storage.all()
        if len(line_parsed) == 0:
            print("** class name missing **")
        elif line_parsed[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(line_parsed) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(line_parsed[0], line_parsed[1]) \
                not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(line_parsed[0], line_parsed[1])]
            storage.save()

    def do_all(self, line):
        """Prints all string representation of all instances
           based or not on the class name.
           Usage: all or all <class> or <class>.all()
        """
        line_parsed = parse_line(line)
        if len(line_parsed) > 0 and line_parsed[0] \
                not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            obj_list = []
            for obj in storage.all().values():
                if len(line_parsed) > 0 and line_parsed[0] \
                        == obj.__class__.__name__:
                    obj_list.append(obj.__str__())
                elif len(line_parsed) == 0:
                    obj_list.append(obj.__str__())
            print(obj_list)

    def do_update(self, line):
        """
        Updates an instance based on the class name and id by adding or
        updating attribute (save the change into the JSON file).
        Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        """
        parsed_line = parse_line(line)
        objdict = storage.all()

        if len(parsed_line) == 0:
            print("** class name missing **")
            return False
        if parsed_line[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(parsed_line) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(parsed_line[0], parsed_line[1]) \
                not in objdict.keys():
            print("** no instance found **")
            return False
        if len(parsed_line) == 2:
            print("** attribute name missing **")
            return False
        if len(parsed_line) == 3:
            try:
                type(eval(parsed_line[2])) != dict
            except NameError:
                print("** value missing **")
                return False
        if len(parsed_line) == 4:
            obj = objdict["{}.{}".format(parsed_line[0], parsed_line[1])]
            if parsed_line[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[parsed_line[2]])
                obj.__dict__[parsed_line[2]] = valtype(parsed_line[3])
            else:
                obj.__dict__[parsed_line[2]] = parsed_line[3]
        elif type(eval(parsed_line[2])) == dict:
            obj = objdict["{}.{}".format(parsed_line[0], parsed_line[1])]
            for k, v in eval(parsed_line[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()

    def do_count(self, line):
        """Retrieves the number of instances of a queried class.
           Usage: count <class> or <class>.count()
        """
        line_parsed = parse_line(line)
        count = 0
        for obj in storage.all().values():
            if line_parsed[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_quit(self, line):
        """Ends the console session."""
        return True

    def do_EOF(self, line):
        """Ends the console session when EOF is supplied or
           ctrl-D is invoked."""
        sys.stdout.write("\n")
        return True

    def do_clear(self, line):
        """Clears the console screen."""
        os.system("clear")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
