PYTHON		= python
CURDIR		= UnitX
DEST_SRC_DIR	= ./unitx
GARBAGE_DIRS	= ./build ./UnitX.egg-info
ANTLR_APP		= ./parser_generator/antlr-4.5.1-complete
SRC_DIR			= ./src
GRAMMAR			= UnitX
AFLAG			= -Dlanguage=Python2

TEST0	= test/test_0.num
TEST3	= test/test_3.num

SRC=\
	src/main.py \
	src/unitx_object.py \
	src/unitx_walker.py \
	src/unitx_tables.txt

all: prepare generate
	@date

install:
	$(PYTHON) setup.py install
	@date
	@echo "\nSUCCESS: The overall installation is successful!"

uninstall:
	$(PYTHON) setup.py install --record log.txt
	cat log.txt | xargs rm -vf
	rm -f log.txt
	rm -f "/Library/Python/2.7/site-packages/UnitX-1.0.0-py2.7.egg"
	@echo "\nSUCCESS: The overall uninstallation is successful!"
	@date

prepare:
	mkdir -p $(DEST_SRC_DIR)
	cp $(SRC_DIR)/*.{py,txt} $(DEST_SRC_DIR)/
	@date

# That generate lexer and parser from a grammar of ANTLR.
generate:
	java -jar $(ANTLR_APP).jar $(AFLAG) -o $(DEST_SRC_DIR)/ $(GRAMMAR).g4 
	@date

test0:
	cd $(DEST_SRC_DIR); ./$(TARGET) ../$(TEST0)
	@date

test3:
	cd $(DEST_SRC_DIR); ./$(TARGET) ../$(TEST3)
	@date

inline:
	cd $(DEST_SRC_DIR); ./$(TARGET)

clean:
	rm -rf $(DEST_SRC_DIR)/
	rm -rf $(GARBAGE_DIRS)
	@date
	
zip: clean
	cd ..; zip -r ${CURDIR}.zip ${CURDIR}
	@date
