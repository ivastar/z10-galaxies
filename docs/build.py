import sys
from website.generate import Generator
Generator.from_file(sys.argv[1]).generate()

