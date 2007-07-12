# Standard library imports.
import glob, os, sys


# The stylesheet used in the generated HTML.
STYLESHEET = 'chilvers'

# A template for the command that runs 'rst2html'.
COMMAND_TEMPLATE = """

rst2html --stylesheet=%s.css "%s" > "html/%s.html"

"""

def main(argv=sys.argv):
    """ Application entry point. """

    # If an additional argument is specified then use it as tghe stylesheet
    # name.
    if len(argv) > 1:
        stylesheet = argv[1]

    else:
        stylesheet = STYLESHEET
        
    for filename in glob.glob('*.txt'):
        name, ext = os.path.splitext(filename)
        os.system(COMMAND_TEMPLATE % (stylesheet, filename, name))

    return


if __name__ == '__main__':
    main()

#### EOF ######################################################################
