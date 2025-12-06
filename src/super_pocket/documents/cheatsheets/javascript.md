# JavaScript Cheat Sheet

## Variables

**`var name = "string";`**
Creates a new variable.
Variables can be numbers, strings, booleans, objects, arrays or functions.

**`var name = 123;`**
Creates a new variable.
The `var` keyword is used to declare variables.

## String Methods

**`"string".length`**
Returns the number of characters in the string. More information on the [String/length](http://www.javascripture.com/String/length) page.

**`"string".indexOf(substr, [start])`**
Returns the index of the first occurence of `substr` in `string`, starting the search at `start`. Returns -1 if `substr` is not found. More information on the [String/indexOf](http://www.javascripture.com/String/indexOf) page.

**`"string".lastIndexOf(substr, [start])`**
Returns the index of the last occurence of `substr` in `string`, searching backwards from `start`. Returns -1 if `substr` is not found. More information on the [String/lastIndexOf](http://www.javascripture.com/String/lastIndexOf) page.

**`"string".search(regexp)`**
Executes a regular expression search on the string. Returns the index of the match, or -1. More information on the [String/search](http://www.javascripture.com/String/search) page.

**`"string".match(regexp)`**
Executes a regular expression search on the string. Returns an array of information or null on a mismatch. More information on the [String/match](http://www.javascripture.com/String/match) page.

**`"string".slice(start, [end])`**
Extracts a section of a string from `start` to `end`, and returns it as a new string. More information on the [String/slice](http://www.javascripture.com/String/slice) page.

## String Methods (2)

**`"string".substr(start, [length])`**
Extracts a section of a string from `start` for `length` characters. Returns the new string. More information on the [String/substr](http://www.javascripture.com/String/substr) page.

**`"string".substring(start, [end])`**
Extracts a section of a string between `start` and `end`. Returns the new string. More information on the [String/substring](http://www.javascripture.com/String/substring) page.

**`"string".replace(substr|regexp, newSubstr|function)`**
Replaces `substr` or `regexp` matches with `newSubstr` or the result of a `function`. More information on the [String/replace](http://www.javascripture.com/String/replace) page.

**`"string".toUpperCase()`**
Returns the string with all characters converted to uppercase. More information on the [String/toUpperCase](http://www.javascripture.com/String/toUpperCase) page.

**`"string".toLowerCase()`**
Returns the string with all characters converted to lowercase. More information on the [String/toLowerCase](http://www.javascripture.com/String/toLowerCase) page.

**`"string".split(separator, [limit])`**
Splits a string on `separator`, returning an array of strings. The number of splits can be limited with `limit`. More information on the [String/split](http://www.javascripture.com/String/split) page.

## Arrays

**`var name = [];`**
Creates a new, empty array. More information on the [Array](http://www.javascripture.com/Array) page.

**`array.length`**
Returns the number of elements in the array. More information on the [Array/length](http://www.javascripture.com/Array/length) page.

**`array.sort()`**
Sorts an array alphabetically. More information on the [Array/sort](http://www.javascripture.com/Array/sort) page.

**`array.reverse()`**
Reverses the order of elements in an array. More information on the [Array/reverse](http://www.javascripture.com/Array/reverse) page.

**`array.push(item, ...)`**
Adds one or more elements to the end of an array. More information on the [Array/push](http://www.javascripture.com/Array/push) page.

**`array.pop()`**
Removes the last element from an array. More information on the [Array/pop](http://www.javascripture.com/Array/pop) page.

**`array.shift()`**
Removes the first element from an array. More information on the [Array/shift](http://www.javascripture.com/Array/shift) page.

**`array.unshift(item, ...)`**
Adds one or more elements to the front of an array. More information on the [Array/unshift](http://www.javascripture.com/Array/unshift) page.

**`array.join([separator])`**
Joins the elements of an array into a string. More information on the [Array/join](http://www.javascripture.com/Array/join) page.

**`array.concat(array2, ...)`**
Joins two or more arrays. More information on the [Array/concat](http://www.javascripture.com/Array/concat) page.

## Array Iteration

**`array.forEach(function(currentValue, index, array), [thisArg])`**
Executes a provided function once per array element. More information on the [Array/forEach](http://www.javascripture.com/Array/forEach) page.

**`array.every(function(currentValue, index, array), [thisArg])`**
Checks if every element in an array pass a test. More information on the [Array/every](http://www.javascripture.com/Array/every) page.

**`array.some(function(currentValue, index, array), [thisArg])`**
Checks if any of the elements in an array pass a test. More information on the [Array/some](http://www.javascripture.com/Array/some) page.

**`array.filter(function(currentValue, index, array), [thisArg])`**
Creates a new array with all elements that pass a test. More information on the [Array/filter](http://www.javascripture.com/Array/filter) page.

**`array.map(function(currentValue, index, array), [thisArg])`**
Creates a new array with the results of calling a function for every array element. More information on the [Array/map](http://www.javascripture.com/Array/map) page.

**`array.reduce(function(accumulator, currentValue, index, array), [initialValue])`**
Reduce the values of an array to a single value (from left-to-right). More information on the [Array/reduce](http://www.javascripture.com/Array/reduce) page.

**`array.reduceRight(function(accumulator, currentValue, index, array), [initialValue])`**
Reduce the values of an array to a single value (from right-to-left). More information on the [Array/reduceRight](http://www.javascripture.com/Array/reduceRight) page.

## Number Methods

**`number.toString([radix])`**
Returns a string representing the number. `radix` is the base to use for representing the number (from 2 to 36). More information on the [Number/toString](http://www.javascripture.com/Number/toString) page.

**`number.toFixed([digits])`**
Formats a number with `digits` numbers of digits to the right of the decimal. More information on the [Number/toFixed](http://www.javascripture.com/Number/toFixed) page.

**`parseInt(string, [radix])`**
Parses `string` and returns an integer. `radix` is the base of the number. More information on the [parseInt](http://www.javascripture.com/parseInt) page.

**`parseFloat(string)`**
Parses `string` and returns a floating point number. More information on the [parseFloat](http://www.javascripture.com/parseFloat) page.

**`isNaN(value)`**
Returns true if `value` is not a number. More information on the [isNaN](http://www.javascripture.com/isNaN) page.

**`isFinite(value)`**
Returns true if `value` is a finite number. More information on the [isFinite](http://www.javascripture.com/isFinite) page.

## Math

**`Math.random()`**
Returns a random number between 0 and 1. More information on the [Math/random](http://www.javascripture.com/Math/random) page.

**`Math.round(number)`**
Rounds a number to the nearest integer. More information on the [Math/round](http://www.javascripture.com/Math/round) page.

**`Math.floor(number)`**
Rounds a number down to the nearest integer. More information on the [Math/floor](http://www.javascripture.com/Math/floor) page.

**`Math.ceil(number)`**
Rounds a number up to the nearest integer. More information on the [Math/ceil](http://www.javascripture.com/Math/ceil) page.

**`Math.min(number, ...)`**
Returns the number with the lowest value. More information on the [Math/min](http://www.javascripture.com/Math/min) page.

**`Math.max(number, ...)`**
Returns the number with the highest value. More information on the [Math/max](http://www.javascripture.com/Math/max) page.

## Dates

**`new Date()`**
Creates a new date object with the current date and time. More information on the [Date](http://www.javascripture.com/Date) page.

**`date.getFullYear()`**
Gets the four digit year. More information on the [Date/getFullYear](http://www.javascripture.com/Date/getFullYear) page.

**`date.getMonth()`**
Gets the month, from 0 to 11. More information on the [Date/getMonth](http://www.javascripture.com/Date/getMonth) page.

**`date.getDate()`**
Gets the day of the month, from 1 to 31. More information on the [Date/getDate](http://www.javascripture.com/Date/getDate) page.

**`date.getHours()`**
Gets the hour, from 0 to 23. More information on the [Date/getHours](http://www.javascripture.com/Date/getHours) page.

**`date.getMinutes()`**
Gets the minute, from 0 to 59. More information on the [Date/getMinutes](http://www.javascripture.com/Date/getMinutes) page.

**`date.getSeconds()`**
Gets the second, from 0 to 59. More information on the [Date/getSeconds](http://www.javascripture.com/Date/getSeconds) page.

**`date.getMilliseconds()`**
Gets the millisecond, from 0 to 999. More information on the [Date/getMilliseconds](http://www.javascripture.com/Date/getMilliseconds) page.

## Conditions

**`if (condition) { ... } else if (condition) { ... } else { ... }`**
Standard if/else statement.

**`switch (expression) { case value: ... break; default: ... }`**
Switch statement.

## Regular Expressions

**`[abc]`**
Find any character between the brackets

**`[^abc]`**
Find any character not between the brackets

**`[0-9]`**
Find any digit from 0 to 9

**`[^0-9]`**
Find any character not a digit from 0 to 9

**`(a|b|c)`**
Find any of the alternatives separated with |

**`\w`**
Find a word character

**`\W`**
Find a non-word character

**`\d`**
Find a digit

**`\D`**
Find a non-digit character

**`\s`**
Find a whitespace character

**`\S`**
Find a non-whitespace character

**`\b`**
Find a match at the beginning/end of a word

**`\B`**
Find a match not at the beginning/end of a word

**`\0`**
Find a NUL character

**`\n`**
Find a new line character

**`\f`**
Find a form feed character

**`\r`**
Find a carriage return character

**`\t`**
Find a tab character

**`\v`**
Find a vertical tab character

**`\xxx`**
Find the character specified by an octal number xxx

**`\xdd`**
Find the character specified by a hexadecimal number dd

**`\udddd`**
Find the Unicode character specified by a hexadecimal number dddd

## Errors

**`try { ... } catch (e) { ... }`**
The try...catch statement marks a block of statements to try, and specifies a response, should an exception be thrown. More information on the [try...catch](http://www.javascripture.com/try...catch) page.

**`throw exception`**
Throws a user-defined exception. More information on the [throw](http://www.javascripture.com/throw) page.

## JSON

**`JSON.parse(string, [reviver])`**
Parses a JSON string, constructing the JavaScript value or object described by the string. More information on the [JSON/parse](http://www.javascripture.com/JSON/parse) page.

**`JSON.stringify(value, [replacer], [space])`**
Converts a JavaScript value to a JSON string. More information on the [JSON/stringify](http://www.javascripture.com/JSON/stringify) page.

## Miscellaneous

**`var person = {firstName:"John", lastName:"Doe", age:50, eyeColor:"blue"};`**
An object literal, with properties and values.

**`typeof x`**
Returns the type of a variable. More information on the [typeof](http://www.javascripture.com/typeof) page.

**`void(expression)`**
Evaluates an expression and returns undefined. More information on the [void](http://www.javascripture.com/void) page.