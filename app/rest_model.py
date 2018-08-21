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

def moments_parser(data, label):
    ret = {}
    for moment in data:
        ret[moment["unixtime"]] = moment["moment"][label]
    return ret


###################################################
# Link Class

class Link:
    def __init__(self, instance_path):
        instance = json_from_path(instance_path)
        self.instance = instance["link"]["instance"]
        self.latest = instance["link"]["latest"]
        self.history = instance["link"]["history"]
        self.moments = instance["link"]["moments"]
        self.relations = instance["link"]["relations"]
        self.count = instance["link"]["count"]
        
###################################################
# Axis Class

class Axis:
    def __init__(self, instance_path):
        self._link = Link(instance_path)
        relations = json_from_path([self._link.relations])
        self._status = Link([relations["status_cnc_axis"][0]["link"]["instance"]])

        
        latest = json_from_path([self._link.latest])
        self.name = latest["axis_name"]
        self.type = latest["axis_type"]
        self.number = latest["axis_number"]
        self.path = latest["path_number"]
        self.path_axis_number = latest["path_axis_number"]
        
    def temperature(self):
        latest = json_from_path([self._status.latest])
        return latest["temperature"]
    
    def machine_position(self):
        latest = json_from_path([self._status.latest])
        return latest["machine_position"]
    
    def temperature_history(self, start, end, limit):
        url = self._status.moments + "?after=" + start + "&before=" + end + "&limit=" + limit + "&order=desc"
        moments_data = json_from_path([url])
        ret = moments_parser(moments_data, "temperature")
        return ret
        
    def moments_count(self, start, end):
        url = self._status.count + "?after=" + start + "&before=" + end
        count = json_from_path([url])
        return count["count"]
       
###################################################
# CNC Class

class CNC:
    def __init__(self, instance_path):
        self._link = Link(instance_path)
        self.axis = []
        self.controller = []

        relations = json_from_path([self._link.relations])
        
        for axis in relations["controller_cnc_axis"]:
            temp_axis = Axis([axis["link"]["instance"]])
            index = 0
            for axis in self.axis:
                if (axis.number < temp_axis.number):
                    index += 1
            self.axis.insert(index, temp_axis)

##################################################
# Node Class

class Node:
    def __init__(self, site):
        self.id = site["id"]
        self.name = site["name"]
        self.controller_id = site["controller_id"]
        self.level = site["level"]
        self.position = site["position"]
        self.parent_id = site["parent_id"]
        self.child_id = site["child_id"]
        self.tag_id = site["tag_id"]
        
    def is_type(self):
        ret = ""
        if isinstance(self.controller_id, str) and len(self.controller_id) > 0 :
            data = json_from_path(["class","controller","instance",self.controller_id,"relations"])
            ret = list(data)[0]
        return ret
        
        
##################################################
# Site Class

class Site:
    def __init__(self):
        self.nodes = []
        response = requests.get(SITE)
        jresp = json.loads(response.text)
        for node in jresp:
            temp_node = Node(node)
            self.nodes.append(temp_node)


        
