import sys,os

from flask import Flask, Blueprint

from . import community_generation

from community_detection.community_detection import *
from community_detection.fetch_data import *


#sys.path.append('../../Community-Detection-Exploration')

def create_app():
   app = Flask(__name__)
   app.register_blueprint(community_generation.bp)
   print(os.getcwd())
   return app

if __name__ == '__main__':
   app = create_app()
   app.run()
