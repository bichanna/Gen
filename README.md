<div align="center">
    <img width="115px" src="https://user-images.githubusercontent.com/60306074/148671204-b759cf4b-dada-483b-80f5-7bc24efc49e5.png">
    <h1>Gen Programming Language</h1>
	|
	<a href="https://github.com/Gen-lang/Gen/tree/master/doc/doc_en.md">Doc(English)</a>
	|
	<a href="https://github.com/Gen-lang/Gen/tree/master/doc/doc_jp.md">Doc(日本語)</a>
	|
</div>

**WARNING!! THIS LANGUAGE IS IN DEVELOPMENT. ANYTHING CAN CHANGE AT ANY MOMENT.**

Gen is an easy-to-learn, dynamic, interpreted, procedural programming language. Gen's syntax is inspired by Ruby and Python. <br>
You also have a simple REPL (but you need to write for loops, if statements, and functions in one line, which is possible but hard).

### TODO List
 - [x] Built-in functions
 - [x] Map
 - [ ] Import other files
 - [x] Reading files with extention .gen (meaning allowing multi-line statements)

### Installation
```
cd Gen/pygen
make install
```
Then you can use gen:
```
gen some_file.gen
```

### Hello World
```
println("Hello World")
```

### Example
For examples, see [examples directory](https://github.com/Gen-lang/Gen/tree/master/examples).
```
# Fizzbuzz

for fizzbuzz = 0 through 51 then
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

### Contributing
Contributions are welcome! Especially, I need a help on Makefile and importing.

### Reports
If you found a bug, please open a new issue and paste the error message and your code that caused the bug.

### Credits
I learned a lot from this [series](https://ruslanspivak.com/lsbasi-part1/) and [T# programming language](https://github.com/Tsharp-lang/Tsharp).
