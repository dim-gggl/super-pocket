# Python Cheat Sheet

## Sys Module

| Method | Description |
|---|---|
| `sys.argv` | Command line args |
| `sys.executable` | Path of Python interpreter |
| `sys.exit()` | Exit the program |
| `sys.modules` | A dictionary of loaded modules. |
| `sys.path` | List of module search paths |
| `sys.platform` | The current platform |
| `sys.stdin` | Stdin stream |
| `sys.stdout` | Stdout stream |
| `sys.stderr` | Stderr stream |
| `sys.version` | Python version |

## OS Module

| Method | Description |
|---|---|
| `os.environ` | A dictionary of environment variables. |
| `os.getcwd()` | Get current working directory |
| `os.getenv()` | Get an environment variable. |
| `os.getpid()` | Get current process id |
| `os.getuid()` | Get current user's id. |
| `os.listdir(path)` | Returns a list of the entries in the directory given by path. |
| `os.mkdir(path)` | Creates a directory. |
| `os.putenv(key, value)` | Set an environment variable. |
| `os.rmdir(path)` | Removes a directory. |
| `os.sep` | Path separator |
| `os.strerror(code)` | Get error message for an error code |
| `os.system(cmd)` | Execute a command in a subshell |

## File System Methods

| Method | Description |
|---|---|
| `os.path.abspath(path)` | Returns the absolute version of a path. |
| `os.path.basename(path)` | Returns the final component of a path. |
| `os.path.dirname(path)` | Returns the directory component of a path. |
| `os.path.exists(path)` | Returns true if path exists. |
| `os.path.isdir(path)` | Returns true if path is a directory. |
| `os.path.isfile(path)` | Returns true if path is a file. |
| `os.path.join(path, ...)` | Joins two or more pathname components. |
| `os.path.split(path)` | Splits a path into a (head, tail) pair. |

## String Methods

| Method | Description |
|---|---|
| `string.capitalize()` | Capitalize first letter |
| `string.count(sub)` | Count occurrences of sub in string |
| `string.find(sub)` | Find first index of sub in string |
| `string.index(sub)` | Find first index of sub in string (raises ValueError if not found) |
| `string.isalnum()` | Returns true if all characters are alphanumeric |
| `string.isalpha()` | Returns true if all characters are alphabetic |
| `string.isdigit()` | Returns true if all characters are digits |
| `string.islower()` | Returns true if all characters are lower case |
| `string.isspace()` | Returns true if all characters are whitespace |
| `string.istitle()` | Returns true if the string is titlecased |
| `string.isupper()` | Returns true if all characters are upper case |
| `string.join(list)` | Join elements of list with string as separator |
| `string.lower()` | Convert to lower case |
| `string.lstrip()` | Strip leading whitespace |
| `string.replace(old, new)` | Replace all occurrences of old with new |
| `string.rfind(sub)` | Find first index of sub from end of string |
| `string.rindex(sub)` | Find first index of sub from end of string (raises ValueError if not found) |
| `string.rstrip()` | Strip trailing whitespace |
| `string.split(sep)` | Split string into list of substrings |
| `string.startswith(prefix)` | Returns true if string starts with prefix |
| `string.strip()` | Strip leading and trailing whitespace |
| `string.swapcase()` | Swap the case of all characters |
| `string.title()` | Change to title case |
| `string.upper()` | Convert to upper case |

## List / String Operations

| Operation | Description |
|---|---|
| `len(list)` | Length of list |
| `list[i]` | Get element at index |
| `list[i:j]` | Get slice from list |
| `list[i] = "v"` | Set element at index |
| `del list[i]` | Delete element at index |
| `list.append("v")` | Add to end of list |
| `list.extend(list2)` | Add all items from list2 to end of list |
| `list.insert(i, "v")` | Insert at index |
| `list.pop()` | Remove and return from end of list |
| `list.remove("v")` | Remove first occurrence of value |
| `list.reverse()` | Reverse list |
| `list.sort()` | Sort list |
| `v in list` | Returns true if value is in list |
| `v not in list` | Returns true if value is not in list |

## List Methods

| Method | Description |
|---|---|
| `list.append(x)` | Add an item to the end of the list. |
| `list.extend(L)` | Extend the list by appending all the items in the given list. |
| `list.insert(i, x)` | Insert an item at a given position. |
| `list.remove(x)` | Remove the first item from the list whose value is x. |
| `list.pop([i])` | Remove the item at the given position in the list, and return it. |
| `list.index(x)` | Return the index in the list of the first item whose value is x. |
| `list.count(x)` | Return the number of times x appears in the list. |
| `list.sort(cmp=None, key=None, reverse=False)` | Sort the items of the list in place. |
| `list.reverse()` | Reverse the elements of the list, in place. |

## Dictionary Methods

| Method | Description |
|---|---|
| `dict.clear()` | Remove all items from the dictionary. |
| `dict.copy()` | Return a shallow copy of the dictionary. |
| `dict.fromkeys(seq[, value])` | Create a new dictionary with keys from seq and values set to value. |
| `dict.get(key[, default])` | Return the value for key if key is in the dictionary, else default. |
| `dict.has_key(key)` | Test for the presence of key in the dictionary. |
| `dict.items()` | Return a copy of the dictionary’s list of (key, value) pairs. |
| `dict.iteritems()` | Return an iterator over the dictionary’s (key, value) pairs. |
| `dict.iterkeys()` | Return an iterator over the dictionary’s keys. |
| `dict.itervalues()` | Return an iterator over the dictionary’s values. |
| `dict.keys()` | Return a copy of the dictionary’s list of keys. |
| `dict.pop(key[, default])` | If key is in the dictionary, remove it and return its value, else return default. |
| `dict.popitem()` | Remove and return an arbitrary (key, value) pair from the dictionary. |
| `dict.setdefault(key[, default])` | If key is in the dictionary, return its value. If not, insert key with a value of default. |
| `dict.update([other])` | Overwrite existing keys, and add new keys from another dictionary. |
| `dict.values()` | Return a copy of the dictionary’s list of values. |
| `dict.viewitems()` | Return a new view of the dictionary’s items ((key, value) pairs). |
| `dict.viewkeys()` | Return a new view of the dictionary’s keys. |
| `dict.viewvalues()` | Return a new view of the dictionary’s values. |

## File Methods

| Method | Description |
|---|---|
| `file.close()` | Closes the file. |
| `file.flush()` | Flush the internal buffer. |
| `file.next()` | Returns the next line from the file each time it is called. |
| `file.read([size])` | Read at most size bytes from the file. |
| `file.readline([size])` | Read one entire line from the file. |
| `file.readlines([sizehint])` | Read until EOF using readline() and return a list containing the lines. |
| `file.seek(offset[, from])` | Set the file's current position. |
| `file.tell()` | Return the file's current position. |
| `file.truncate([size])` | Truncate the file's size. |
| `file.write(str)` | Write a string to the file. |
| `file.writelines(sequence)` | Write a sequence of strings to the file. |

## Exceptions

| Exception | Description |
|---|---|
| `Exception` | Base class for all exceptions |
| `AttributeError` | Raised when an attribute reference or assignment fails. |
| `IOError` | Raised when an I/O operation fails. |
| `ImportError` | Raised when an import statement fails to find the module definition. |
| `IndexError` | Raised when a sequence subscript is out of range. |
| `KeyError` | Raised when a mapping (dictionary) key is not found in the set of existing keys. |
| `KeyboardInterrupt` | Raised when the user hits the interrupt key (normally Control-C or Delete). |
| `NameError` | Raised when a local or global name is not found. |
| `OSError` | Raised when a function returns a system-related error. |
| `SyntaxError` | Raised when the parser encounters a syntax error. |
| `TypeError` | Raised when an operation or function is applied to an object of inappropriate type. |
| `ValueError` | Raised when a built-in operation or function receives an argument that has the right type but an inappropriate value. |
| `ZeroDivisionError` | Raised when the second argument of a division or modulo operation is zero. |

## Reading a File

```python
f = open("tmp.txt", "r") # "r" is default
try:
  for line in f:
    print line.strip()
finally:
  f.close()
  
# With statement will automatically close the file
with open("tmp.txt") as f:
  for line in f:
    print line.strip()
```

## Writing to a File

```python
f = open("tmp.txt", "w") # "w" for write, "a" for append
try:
  f.write("hello\n")
finally:
  f.close()
  
# With statement will automatically close the file
with open("tmp.txt", "w") as f:
  f.write("hello\n")
```

## Date Formatting

| Directive | Meaning | Example |
|---|---|---|
| `%a` | Abbreviated weekday name. | Sun, Mon, ... |
| `%A` | Full weekday name. | Sunday, Monday, ... |
| `%b` | Abbreviated month name. | Jan, Feb, ... |
| `%B` | Full month name. | January, February, ... |
| `%c` | Appropriate date and time representation. | Sun Aug 19 02:56:02 2012 |
| `%d` | Day of the month as a decimal number [01,31]. | 01, 02, ..., 31 |
| `%H` | Hour (24-hour clock) as a decimal number [00,23]. | 00, 01, ..., 23 |
| `%I` | Hour (12-hour clock) as a decimal number [01,12]. | 01, 02, ..., 12 |
| `%j` | Day of the year as a decimal number [001,366]. | 001, 002, ..., 366 |
| `%m` | Month as a decimal number [01,12]. | 01, 02, ..., 12 |
| `%M` | Minute as a decimal number [00,59]. | 00, 01, ..., 59 |
| `%p` | Locale’s equivalent of either AM or PM. | AM, PM |
| `%S` | Second as a decimal number [00,61]. | 00, 01, ..., 61 |
| `%U` | Week number of the year (Sunday as the first day of the week). | 00, 01, ..., 53 |
| `%w` | Weekday as a decimal number [0(Sunday),6]. | 0, 1, ..., 6 |
| `%W` | Week number of the year (Monday as the first day of the week). | 00, 01, ..., 53 |
| `%x` | Appropriate date representation. | 08/19/12 |
| `%X` | Appropriate time representation. | 02:50:02 |
| `%y` | Year without century as a decimal number [00,99]. | 00, 01, ..., 99 |
| `%Y` | Year with century as a decimal number. | 2012, 2013, ... |
| `%Z` | Time zone name (no characters if no time zone exists). |
| `%%` | A literal "%" character. | % |

```python
import datetime
now = datetime.datetime.now()
print now.strftime("It's %d/%m/%Y %H:%M:%S")
# It's 19/08/2012 02:50:02
```

## Class Example

```python
class MyClass(object):
  """A simple example class"""
  i = 12345
  
  def __init__(self, name):
    self.name = name
    
  def say_hi(self):
    print "hello", self.name
    
# Create instance and call a method
x = MyClass("Dave")
x.say_hi()
# hello Dave
```