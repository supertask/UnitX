TARGET 	= unitx
CURDIR	= UnitX
SRCDIR	= src
TEST 	= test/test_0.num
SRC		= \
	$(SRCDIR)/unitx

GRAMMAR=UnitX
DEST_SRC_DIR=./dest_dir/src
ANTLR_APP=parser_generator/antlr-4.5.1-complete
ANTLR_SRC_DIR=./antlr_src
SRC_DIR=./src

grammar:
	@mkdir -p $(ANTLR_SRC_DIR)
	java -jar $(ANTLR_APP).jar $(GRAMMAR).g4 -Dlanguage=Python2 -o $(ANTLR_SRC_DIR)
	cp $(ANTLR_SRC_DIR)/* $(DEST_SRC_DIR)/
	cp $(SRC_DIR)/* $(DEST_SRC_DIR)/

test:
	cd $(DEST_SRC_DIR); ./$(TARGET) ../$(TEST)

inline:
	cd $(DEST_SRC_DIR); ./$(TARGET)

testcase:
	vim dest_dir/$(TEST)

clean:
	rm $(DEST_SRC_DIR)/*
	rm -rf $(ANTLR_SRC_DIR)
	
zip: clean
	cd ..; zip -r ${CURDIR}.zip ${CURDIR}

