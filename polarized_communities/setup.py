from distutils.core import setup
from distutils.extension import Extension
from shutil import copyfile

if __name__ == '__main__':
    # files to be included in the extensions
    paths = [
        'algorithms/subroutines/commons',
        'algorithms/bansal',
        'algorithms/eigensign',
        'algorithms/greedy_degree_removal',
        'algorithms/local_search',
        'algorithms/random_eigensign',
        'signed_graph/signed_graph',
        'utilities/print_console',
        'utilities/time_measure'
    ]

    # import Cython if available
    USE_CYTHON = True
    try:
        from Cython.Build import cythonize
    except ImportError:
        cythonize = None
        USE_CYTHON = False

    # if Cython is available
    if USE_CYTHON:
        # set the .pyx extension
        ext = '.pyx'

        # create the new .pyx files
        for path in paths:
            copyfile(path + '.py', path + ext)
    # otherwise
    else:
        # set the .c extension
        ext = '.c'

    # build the extensions list
    extensions = [Extension(path.replace('/', '.'), [path + ext]) for path in paths]

    # if Cython is available
    if USE_CYTHON:
        # cythonize the extensions
        extensions = cythonize(extensions)

    # run the setup
    setup(
         ext_modules=extensions
    )
