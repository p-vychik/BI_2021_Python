## Some Unix command line tools implemented with python
wc.py - counts lines in stdin or file provided by user
usage: wc.py [--l] [--w] [--c] [file]
--l - count lines
--w - count words 
--c - count bytes

ls.py - lists directory content
usage: ls.py [--a] [directory]
--a - show hidden files and directories in output

rm.py - deletes files or directories provided py user
usage: rm.py [-h] [--r] source
--r - remove directories recursively

sort.py - sorts lines of text files, supports read from stdin
usage: sort.py [file]

tail.py - outputs the last lines of file or stdin 
usage: tail.py [--n N] [file]
--n - number of last lines to output, default value 10

uniq.py - outputs unique values in text file or stdin
usage: uniq.py [file]

grep.py - outputs lines if it matches a regex pattern
usage: grep.py reg_pattern [file]
reg_pattern - string representing python regEx
