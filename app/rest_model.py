
################################################
# Imports
################################################

import requests
import json
import halogen
from urllib.parse import urlunsplit


################################################
# Constants
################################################

# REST API Server
IP = '192.168.1.1'
PORT = '9999'
API = 'api/base/location'


################################################
# API Calls
################################################

def concat_paths(sequence):
        result = []
        for path in sequence:
            result.append(path)
            if path.startswith('/'):
                break
        return '/'.join(result)

def easy_url(path):
    scheme = 'http'
    netloc = IP + ':' + PORT + '/' + API
    hpath = concat_paths(path)
    query = ''
    fragment = ''
    return urlunsplit((scheme, netloc , hpath , query, fragment))

def get_json(path):
    response = requests.get(easy_url(path))
    return json.loads(response.text)


#**************************************************************
# CONTROLLER_CNC
#
# Halogen Schema and object template
#**************************************************************
class Any_instance(object):
    id = ""
    link = ""

class Any_instance_schema(halogen.Schema):
    id = halogen.Attr()
    link = halogen.Attr()

#********************** Example Usage *************************
# assignment
cnc_instance = Any_instance()

# deserialize data to specified object
Any_instance_schema.deserialize(get_json(('class', 'controller_cnc', 'instance', 'controller_cnc00001')), cnc_instance)

# using the object
cnc_instance.id
cnc_instance.link['instance']
easy_url([cnc_instance.link['relations']])
#**************************************************************


#**************************************************************
# CONTROLLER_CNC_RELATIONS
#
# Halogen Schema and object template
#**************************************************************
class Controller_cnc_relations(object):
    status = ""
    status_cnc = ""
    event_alarm = ""
    archive_maintenance_compress_file_info = ""
    controller = ""
    controller_cnc_axis = ""
    controller_cnc_path = ""

class Controller_cnc_relations_schema(halogen.Schema):
    status = halogen.Attr()
    status_cnc = halogen.Attr()
    event_alarm = halogen.Attr()
    archive_maintenance_compress_file_info = halogen.Attr()
    controller = halogen.Attr()
    controller_cnc_axis = halogen.Attr()
    controller_cnc_path = halogen.Attr()

#********************** Example Usage *************************
# object creation
cnc_relations = Controller_cnc_relations()

# deserialize data to specified object
Controller_cnc_relations_schema.deserialize(get_json([cnc00001.link['relations']]), cnc_relations)

# using the object
cnc_relations.status
cnc_relations.status[0]['link']['instance']
#**************************************************************


#**************************************************************
# CONTROLLER_CNC_AXIS_RELATIONS
#
# Halogen Schema and object template
#**************************************************************
class Controller_cnc_axis_relations(object):
    status_cnc_axis = ""
    controller_cnc = ""


class Controller_cnc_axis_relations_schema(halogen.Schema):
    status_cnc_axis = halogen.Attr()
    controller_cnc = halogen.Attr()


#********************** Example Usage *************************
# object creation
axis_relations = Controller_cnc_axis_relations()

# deserialize data to specified object
Controller_cnc_axis_relations_schema.deserialize(get_json([cnc_relations.controller_cnc_axis[0]['link']['relations']]), axis_relations)

# using the object
axis_relations.status_cnc_axis
axis_relations.status_cnc_axis[0]['link']['instance']
#**************************************************************


#**************************************************************
# CONTROLLER_CNC_AXIS_LATEST
#
# Halogen Schema and object template
#**************************************************************
class Controller_cnc_axis_latest(object):
    axis_name = ""
    axis_type = ""
    axis_number = ""
    path_number = ""
    path_axis_number = ""


class Controller_cnc_axis_latest_schema(halogen.Schema):
    axis_name = halogen.Attr()
    axis_type = halogen.Attr()
    axis_number = halogen.Attr()
    path_number = halogen.Attr()
    path_axis_number = halogen.Attr()


#********************** Example Usage *************************
# object creation
axis_latest = Controller_cnc_axis_latest()

# deserialize data to specified object
Controller_cnc_axis_latest_schema.deserialize(get_json([cnc_relations.controller_cnc_axis[0]['link']['latest']]), axis_latest)

# using the object
axis_latest.axis_name
#**************************************************************

