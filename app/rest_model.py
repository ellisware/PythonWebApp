################################################
# Imports
################################################

import requests
import json
from urllib.parse import urlunsplit


################################################
# Constants
################################################

# REST API Server
IP = '192.168.2.241'
PORT = '8083'
API = 'field_api/v3'


################################################
# Helpers
################################################

def concat_paths(sequence):
        result = []
        for path in sequence:
            result.append(path)
            if path.startswith('/'):
                break
        return '/'.join(result)

def easy_url(path_parts):
    scheme = 'http'
    netloc = IP + ':' + PORT + '/' + API
    hpath = concat_paths(path_parts)
    query = ''
    fragment = ''
    return urlunsplit((scheme, netloc , hpath , query, fragment))

def json_from_path(path):
    response = requests.get(easy_url(path))
    return json.loads(response.text)



###################################################
# CNC
###################################################
#
#   cnc.id
#      .path
#      .axis[n].name
#              .type
#              .number
#              .path
#              .path_axis_number
#              .status_instance
#              .status_latest
#              .status_history
#              .temperature()
#              .machine_position()
#       .controller[n].manufacturer
#                     .type
#                     .model
#                     .ip_address
#
#

class Axis:
    def __init__(self, axis_latest):
        self.name = axis_latest["axis_name"]
        self.type = axis_latest["axis_type"]
        self.number = axis_latest["axis_number"]
        self.path = axis_latest["path_number"]
        self.path_axis_number = axis_latest["path_axis_number"]
        self.status_instance = ""
        self.status_latest = ""
        
    def temperature(self):
        latest = json_from_path([self.status_latest])
        return latest["temperature"]
    
    def machine_position(self):
        latest = json_from_path([self.status_latest])
        return latest["machine_position"]
        
        
class Controller:
    def __init__(self, controller_latest):
        self.manufacturer = controller_latest["manufacturer"]
        self.type = controller_latest["controller_type"]
        self.model = controller_latest["model"]
        self.ip_address = controller_latest["ip_address"]

class CNC:
    def __init__(self, instance_path):
        self.path = instance_path
        self.raw_instance = json_from_path(instance_path)
        self.id = self.raw_instance["id"]
        self.axis = []
        self.controller = []

        relations = json_from_path([self.raw_instance["link"]["relations"]])
        #self.name = relations["controller"]["name"]
        
        for axis in relations["controller_cnc_axis"]:
            temp_axis = Axis(json_from_path([axis["link"]["latest"]]))
            axis_relations = json_from_path([axis["link"]["relations"]]) 
            temp_axis.status_instance = axis_relations["status_cnc_axis"][0]["link"]["instance"]
            temp_axis.status_latest = axis_relations["status_cnc_axis"][0]["link"]["latest"]
            self.axis.append(temp_axis)
        
        for controller in relations["controller"]:
            self.controller.append(Controller(json_from_path([controller["link"]["latest"]])))
        
        
