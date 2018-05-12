"""Main function."""

import sys
from html import unescape
import datetime



def main():
    """Perform main function."""
    if len(sys.argv) != 2:
        return None
    print("Cleaning!")

    inputfile = open(sys.argv[1]).read()
    target = open('./output/cleaned-season-{}.csv'.format(sys.argv[1]), 'w')

    data = inputfile.split("\n")[:-1]

    for item in data:
        target.write('{}\n'.format(unescape(item)))

    print("Complete!")


if __name__ == "__main__":
    main()
