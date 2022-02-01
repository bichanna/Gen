<link rel="icon" href="https://user-images.githubusercontent.com/60306074/148671204-b759cf4b-dada-483b-80f5-7bc24efc49e5.png">

<div align="center">
    <img width="115px" src="https://user-images.githubusercontent.com/60306074/148671204-b759cf4b-dada-483b-80f5-7bc24efc49e5.png">
</div>

> *Note:* **WARNING!! THIS LANGUAGE IS IN DEVELOPMENT. ANYTHING CAN CHANGE AT ANY MOMENT.**

## About
Gen is a brand new, easy-to-learn, dynamic, interpreted, procedural, programming language by [bichanna](https://github.com/bichanna) and others.<br>
Gen's syntax is greatly inspired by Ruby and Python. But one unique thing in Gen is the use of `@`. It also has a simple REPL (but you need to write for loops, if statements, and functions in one line, which is possible but hard to write).<br>
The language is created from scratch using Python (working on an implementation in C).


## Hello World
It's just one line without any entry function.
```
println("Hello World")
```

## Example
```
# Fizzbuzz

for fizzbuzz = 0 through 15000 then
	if fizzbuzz % 3 == 0 and fizzbuzz % 5 == 0 then
		println("fizzbuzz")
		continue
	elseif fizzbuzz % 3 == 0 then
		println("fizz")
		continue
	elseif fizzbuzz % 5 == 0 then
		println("buzz")
		continue
	end
end
```


### Current State
Gen has many features you would expect:
 - All the operators (`+`, `-`, `^`, `%`, `and`, `<=`, etc.)
 - Flow control (`if`, `elseif`, `for`/`while` loop)
 - Array
 - Map
 - Function
 - Basic built-in functions


### Contributing
Contributions are always welcome! Especially, I need help bug fixing.
