import sys
import os

def setup_path():
    modules = ['requests', 'envoy', 'sugargame2/sugargame2', 'spyral/spyral']
    for module in modules:
        sys.path.insert(0, os.path.abspath('libraries/%s/' % module))