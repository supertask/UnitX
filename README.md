![UnitX logo image](doc/images/unitx_logo.png)


What is UnitX
-----
UnitX is a script language for Unit. **Especially, Unit handling is better than other languages.**

[English](README.md), [日本語](README.ja.md)

How to install
-----
	
	git clone https://github.com/supertask/UnitX
	make
	sudo make install

Example
-----
Run Demo program like below.

	$ unitx demo/demo_0.unit

And a content in the code is like bellow.

```python:demo_0.unit
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

The result become like bellow.

```text:result
飛行機代: 20{万}
保険料: 20{万}
---
学校代: 8{万/月}
レジデンス代: 10{万/月}
食費: 2{万/月}
計: 58{万}
-----
学校代: 96{万/年}
レジデンス代: 120{万/年}
食費: 24{万/年}
計: 256{万}
-----
```

Regulation
-----
If you're going to use UnitX, you must tune to UTF-8 on your command-line shell and editor.

Coding style
-----
Following a [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) for using UnitX or developing UnitX.  
However, as a parser generator, we use ANTLR 4. So, we use LCC(Lower Camel Case) in some code(eval\_visitor.py and eval\_error.py) for receiving messages from ANTLR 4.

The Author
-----
Tasuku TAKAHASHI ([supertask.jp](http://supertask.jp))

LICENSE
-----
MIT

RELEASED
-----
|   Version   |    Released   |
|:------------|--------------:|
| 0.7.0 alpha |   2016-04-04  |

RELEASE SCHEDULE
-----
|   Version   | scheduled day |
|:------------|--------------:|
| 0.7.0 beta  |   2016-05-01  |
| 0.8.0 alpha |   2018-09-01  |
