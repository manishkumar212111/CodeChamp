from flask import Flask

app = Flask(__name__)

# This line adds the hasura example routes form the hasura.py file.
# Delete these two lines, and delete the file to remove them from your project
#from .hasura import tsp
#app.register_blueprint(hasura_examples)
#from tsp import *

from .server import *
#from .data import *
#from .auth import *
#from .filestore import *
