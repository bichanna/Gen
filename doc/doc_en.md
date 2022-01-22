
# Gen Syntax


### Variables
Variable assignment is quite similar to Python.
```
a = "some string"
b = 28 + (c = 38)
println(c)
```

### String
Use "
```
str = "Hello World "
println(str * 3)
# output:
# Hello World Hello World Hello World 
```

### Array
Gen array can store any type.
```
arr = ["Hello", "World", 123, 3.1415, ["me", "gen"]]
# to add a new value, just use '+'
arr = arr + "bichanna"

a = [1, 2, 3, 4]
# use '@' to retrieve specific value from an array
println(a@0) # the first element
println(a@-1) # the last element
```

### Map
```
map = {"foo": "bee"}
println(map@"foo")
```

### Logical Operators
Just like any other languages.
```
gen>> 1 > 10
0
gen>> 1 < 10 
1
gen>> 2 <= 3
1
gen>> 2 >= 3
0
gen>> 2 == 3
0
gen>> 2 == 2
1
gen>> 2 != 4
1
```

### If statement
```
age = 15
if age > 18 then
  println("over 18")
elseif age == 15 then
  println("15")
else # notice you don't need 'then' keyword for 'else'
  println("??")
end
```

### For loop
Maybe a bit wordy.
```
arr = []
for i = 1 through 12 step 2 then
  arr = arr + 2^i
end
println(arr)
# output
# [2, 8, 32, 128, 512, 2048]
```

### While loop
It's quite similar to Python.
```
arr = []
a = 0
while a <= 10 then
	arr = arr + a
	a = a + 1
end
println(arr)
```

### Function
It's a bit unique with the keyword 'defunc' (def + func)
```
# one-line function
defunc greet(name) -> println("Hello " + name)

# multi-line function
defunc greet(name)
	println("Hello " + name)
end

# you can return from some value from function
defunc return_greet(name)
	return_value = "Hello " + name
	return return_value
end

greet("bichanna")

println(return_greet("bichanna"))
```

For built-in functions see [this doc](https://github.com/Gen-lang/Gen/blob/master/doc/builtin_functions.md).

