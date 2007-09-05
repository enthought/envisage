# Standard library imports.
import glob, os, shutil, sys


# The stylesheet used in the generated HTML.
STYLESHEET = 'rest'

# A template for the command that runs 'rst2html'.
COMMAND_TEMPLATE = """

rst2html --stylesheet=%s.css "%s" > "html/%s.html"

"""


def make_text_docs(stylesheet):
    """ Make the text documentation. """

    # Put all the generated documents in here.
    try:
        os.mkdir('html')
        
    except:
        pass

    shutil.copyfile('%s.css' % stylesheet, 'html/%s.css' % stylesheet)

    # Convert all text files (actually, reST documents!) into HTML.
    for filename in glob.glob('*.txt'):
        name, ext = os.path.splitext(filename)
        print 'Processing %s...' % filename,
        os.system(COMMAND_TEMPLATE % (stylesheet, filename, name))
        print 'Done.'

    # Copy over any iamges.
    if os.path.isdir('images'):
        # Put all the generated documents in here.
        try:
            os.mkdir('html/images')
            
        except:
            pass

        # Copy any images.
        for filename in os.listdir('images'):
            if filename == '.svn':
                continue
        
            shutil.copyfile('images/%s' % filename,'html/images/%s' % filename)
    
    return

def make_api_docs():
    """ Make the API documentation. """

    try:
        os.makedirs('html/api')

    except:
        pass
    
    # Now make the API documentation.
    print 'Making API documentation...',
    os.system('endo --rst -d html/api -r ..\enthought')
    print 'Done.'

    return


def main(argv=sys.argv):
    """ Application entry point. """

    # If an additional argument is specified then use it as tghe stylesheet
    # name.
    if len(argv) > 1:
        stylesheet = argv[1]

    else:
        stylesheet = STYLESHEET

    make_text_docs(stylesheet)
    make_api_docs()

    return


if __name__ == '__main__':
    main()

#### EOF ######################################################################
