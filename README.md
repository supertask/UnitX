![UnitX logo image](doc/images/unitx_logo.png)

*Read this in other languages: [English](README.md), [日本語](README.ja.md)*


What is UnitX
-----
UnitX is a script language for Unit.


How to install
-----
	
	git clone https://github.com/supertask/UnitX
	make
	sudo make install

Example
-----
Run Demo program like below.

	make demo


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
