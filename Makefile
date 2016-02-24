PYTHON		= python
TARGET		= $(PYTHON) unitx/example.py
CURDIR		= UnitX
DEST_SRC_DIR	= ./unitx
GARBAGE_DIRS	= ./build ./dist ./UnitX.egg-info
ANTLR_APP		= ./parser_generator/antlr-4.5.1-complete
SRC_DIR			= ./src
GRAMMAR			= UnitX
AFLAG			= -Dlanguage=Python2

DEMO0	= demo/demo_0.num
DEMO1	= demo/demo_1.num

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

prepare:
	mkdir -p $(DEST_SRC_DIR)
	cp $(SRC_DIR)/*.{py,txt} $(DEST_SRC_DIR)/
	@date

# That generate lexer and parser from a grammar of ANTLR.
generate:
	java -jar $(ANTLR_APP).jar $(AFLAG) -o $(DEST_SRC_DIR)/ $(GRAMMAR).g4 
	@date

# In python, to uninstall a module is impossible. So, we have to make "uninstall".
uninstall:
	$(PYTHON) setup.py install --record log.txt
	cat log.txt | xargs rm -vf
	rm -f log.txt
	rm -f "/Library/Python/2.7/site-packages/UnitX-1.0.0-py2.7.egg"
	@echo "\nSUCCESS: The overall uninstallation is successful!"
	@date

unittest:
	$(PYTHON) setup.py test

demo0:
	$(TARGET) $(DEMO0)
	@date

demo1:
	$(TARGET) $(DEMO1)
	@date

inline:
	$(TARGET)

clean:
	rm -rf $(DEST_SRC_DIR)/
	rm -rf $(GARBAGE_DIRS)
	@date
	
# For backup of this module.
zip: clean
	cd ..; zip -r ${CURDIR}.zip ${CURDIR}
	@date
