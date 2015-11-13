TARGET = unitx
SRC=test/test_code_0.num

all:
	./$(TARGET) $(SRC)
tests:
	python test_parsing.py
