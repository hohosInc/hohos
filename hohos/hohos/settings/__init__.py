# this __init__.py  is initialization for the seetings folder, with this file the whole settings folder works as 
# settings.py  such folders or directories are called modules 

from .base import *

try:
	from .local import *
except:
	pass

try:
	from .production import *
except:
	pass
