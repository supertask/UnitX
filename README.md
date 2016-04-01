![UnitX logo image](doc/images/unitx_logo.png)


What is UnitX
-----
UnitX is a script language for Unit.

[English](README.md), [日本語](README.ja.md)

How to install
-----
	
	git clone https://github.com/supertask/UnitX
	make
	sudo make install

Example
-----
Run Demo program like below.

	make demo

or

```rb
>> 飛行機代 = 10{万} * 2{@往復}
>> 保険料 = 20{万}
---
rep i,['月','年'] {
	>> 学校代 = 8{万/月->i}
	>> レジデンス代 = 10{万/月->i}
	>> 食費 = 2{万/月->i}
	>> 計 = 飛行機代 + 保険料 + (学校代 + レジデンス代){万/i} * 1{i}
	-----
}
```

Coding style
-----
Following a [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) for using UnitX or developing UnitX.  
However, as a parser generator, we use ANTLR4. So, we use LCC in the visitor(UnitXEvalVisitor) for ANTLR4.

The Author
-----
Tasuku TAKAHASHI ([supertask.jp](http://supertask.jp))

LICENSE
-----
MIT

RELEASED
-----
Nothing

RELEASE SCHEDULE
-----
|   Version   | scheduled day |
|:------------|--------------:|
| 0.7.0 alpha |   2016-03-31  |
| 0.7.0 beta  |   2016-05-01  |
| 0.8.0 alpha |   2018-09-01  |
