PYTHON		= python
TARGET		= $(PYTHON) unitx/example.py
CURDIR		= UnitX
DEST_SRC_DIR	= ./unitx
GENERATED_DIRS	= ./build ./dist ./UnitX.egg-info
ANTLR_APP		= ./parser_generator/antlr-4.5.1-complete
SRC_DIR			= ./src
GRAMMAR			= UnitX
AFLAG			= -Dlanguage=Python2
INST_PACKS		= "antlr4-python2-runtime\nprettyprint"

DEMO0	= demo/demo_0.unit
DEMO1	= demo/demo_1.unit

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
	mkdir -p $(DEST_SRC_DIR)/data
	cp $(SRC_DIR)/*.py $(DEST_SRC_DIR)/
	cp $(SRC_DIR)/data/*.dat $(DEST_SRC_DIR)/data/
	@date

# That generate lexer and parser from a grammar of ANTLR.
generate:
	java -jar $(ANTLR_APP).jar $(AFLAG) -o $(DEST_SRC_DIR)/ $(GRAMMAR).g4 -visitor
	@date

# In python, to uninstall a module is impossible. So, we have to make "uninstall".
uninstall:
	$(PYTHON) setup.py install --record log.txt
	cat log.txt | xargs rm -vf
	rm -f log.txt
	rm -f "/Library/Python/2.7/site-packages/UnitX-1.0.0-py2.7.egg"
	@echo "\nSUCCESS: The almost uninstallation is successful!\n"
	@echo "------"
	@echo "If you would like to remove all, you should remove following modules by using pip command:"
	@echo $(INST_PACKS)
	@echo "It's like a 'pip uninstall {module name}'.\n"
	@date

test: all
	$(PYTHON) setup.py test
	@date

demo: all
	$(TARGET) demo/demo_0.unit
	@date

demo0: all
	$(TARGET) demo/demo_0.unit
	@date

demo1: all
	$(TARGET) demo/demo_1.unit
	@date

demox: all
	$(TARGET) demo/demo_x.unit
	@date

tmp: all
	$(TARGET) tests/tmp.unit
	@date
	
errtmp: all
	$(TARGET) tests/err_tmp.unit
	@date

inline: all
	$(TARGET)
	@date

clean:
	rm -rf $(DEST_SRC_DIR)/
	rm -rf $(GENERATED_DIRS)
	@date
	
# For backup of this module.
zip: clean
	cd ..; zip -r ${CURDIR}.zip ${CURDIR}
	@date

wc:
	wc -l UnitX.g4 src/*.py tests/*.py tests/*.unit
