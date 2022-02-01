# Gen文法

### 変数
```
a = "some string"
b = 28 + (c = 38)
println(c)
```

### 文字列
```
str = "Hello 世界 "
println(str * 3)
# output:
# Hello 世界 Hello 世界 Hello 世界
```

### Array
```
arr = ["Hello", "World", 123, 3.1415, ["me", "gen"]]
# '+' を使って値を配列に追加することができます。
arr = arr + "bichanna"

# iteration
for i in arr then
	println(i)
end

a = [1, 2, 3, 4]
# 配列から特定の値を取り出すには、'@' を使用します。
println(a@0) # the first element
println(a@-1) # the last element
```

### Map
```
map = {"foo": "bee"}
println(map@"foo")
```

### 論理演算子
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

### If文
```
age = 15
if age > 18 then
  println("over 18")
elseif age == 15 then
  println("15")
else # 'else' に 'then' キーワードは必要ないです。
  println("??")
end
```

### Forループ
文法が少し口説いかもしれないけど。
```
arr = []
for i = 1 through 12 step 2 then
  arr = arr + 2^i
end
println(arr)
# output
# [2, 8, 32, 128, 512, 2048]

# iteration
for i in arr then
	println(i)
end
```

### While文
```
arr = []
a = 0
while a <= 10 then
	arr = arr + a
	a = a + 1
end
println(arr)
```

### 関数
```
# 一行
defunc greet(name) -> println("Hello " + name)

# 複数行の関数
defunc greet(name)
	println("Hello " + name)
end

# 'return' で関数から値を返すことができます。
defunc return_greet(name)
	return_value = "Hello " + name
	return return_value
end

greet("bichanna")

println(return_greet("bichanna"))
```

### Import
```
import("some_file.gen")

# 上のようにインポートすると、some_file.gen にある関数を呼び出すことができます。
some_func_in_some_file()
```

[組み込み関数。](https://github.com/Gen-lang/Gen/blob/master/doc/builtin_functions.md)

