#
# The __init__ file is used not only to import the sub-modules, but also to
# set everything up properly.
#

# Load sub-modules.
from .plot1d import *
from .plot2d import *
from .plot3d import *
from .colors import *

del(plot1d)
del(plot2d)
del(plot3d)
del(colors)