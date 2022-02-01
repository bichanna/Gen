<div align="center">
    <img width="115px" src="https://user-images.githubusercontent.com/60306074/148671204-b759cf4b-dada-483b-80f5-7bc24efc49e5.png">
    <h1>Gen Programming Language</h1>
	|
	<a href="https://github.com/Gen-lang/Gen/tree/master/docs/doc_en.md">Doc(English)</a>
	|
	<a href="https://github.com/Gen-lang/Gen/tree/master/docs/doc_jp.md">Doc(日本語)</a>
	|
</div>

**WARNING!! THIS LANGUAGE IS IN DEVELOPMENT. ANYTHING CAN CHANGE AT ANY MOMENT.**

Gen is an easy-to-learn, dynamic, interpreted, procedural programming language. Gen's syntax is inspired by Ruby and Python. <br>
Gen also has a simple REPL (but you need to write for loops, if statements, and functions in one line, which is possible but hard to write).<br>
And in Gen, a semicolon is the same as a new line, so you can ultimately write everthing in one line.


### TODO
 - [x] Basic Built-in functions
 - [ ] File I/O Operation
 - [x] Official site


### Installation
> *Note:* Using `git clone` to clone the repository is discouraged. Please download the source code from the releases page
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
# Bubble sort

defunc bubble_sort(arr)
    for i=0 through size(arr) then
        for j=0 through size(arr)-i-1 then
            jpls1 = j + 1
            if (arr@j) > (arr@jpls1) then
                temp = arr@j
                arr@j = arr@jpls1
                arr@jpls1 = temp
            end
        end
    end
end


array = [3734, 3732, 3810, 1649, 4952, 7993, 1225, 2728, 2849, 2113, 9883, 3839, 2839, 5463, 2741, 5684, 6848, 2834, 1838, 2483, 8384, 7885, 4853, 5848, 3838]

bubble_sort(array)

println(array)

```

### Contributing
Contributions are welcome! Especially, I need help bug fixing.

### Reports
If you found a bug, please open a new issue and paste the error message and your code that caused the bug.

### Credits
I learned a lot from this [series](https://ruslanspivak.com/lsbasi-part1/) and [T# programming language](https://github.com/Tsharp-lang/Tsharp).
