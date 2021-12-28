from os import path
import json

'''
Mock migration path, create DB table if it doesn't exist
'''
def create_if_not_exists():
    curr_dir = path.dirname(__file__)
    filename = path.join(curr_dir, 'task_table.json')
    if not path.exists(filename):
        with open(filename, 'w') as output_file:
            json.dump({}, output_file)
