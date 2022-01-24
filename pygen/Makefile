# Usage
# Just type 'make' or 'make install'

install:
ifeq ($(OS),Windows_NT)
	@pip install pyinstaller
	@pyinstaller .\main.py --onefile
	@COPY ".\dist\main.exe" ".\gen.exe"
# Set environment variable here
	@echo "PyGen Compilation Succeeded"
	@echo "Type 'gen'"
else
	@pip install pyinstaller
	@pyinstaller ./main.py --onefile
	@cp ./dist/main /usr/local/bin/gen
	@cp ../editor/gen.vim ~/.vim/syntax
	@echo "autocmd BufRead,BufNewFile *.gen set filetype=gen" >> ~/.vimrc
	@echo "\033[0;32mPyGen Compilation Succeeded"
	@echo "\033[0;32mType 'gen'"
endif
