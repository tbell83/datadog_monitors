__author__ = 'thomasb'
from datadog import initialize, api
from os import walk

options = {
    'api_key': 'd7ce8fdf7ff28617caf8f041c375ec58',
    'app_key': '62242ee5b9d7cfb79e20ae11fa6198d2db1f2d0a'
}

initialize(**options)


# Read config from file
def read_yaml_cfg(filename):
    fo = open(filename, 'r')
    poops = fo.readlines()
    config = {}
    options = {}
    option = False
    for item in poops:
        item = item.replace('"', '').replace('\n', '').replace(',', '')

        if (item == '  options: {') and (option == False):
            option = True
            config['options'] = options
        elif item == '  }':
            option = False
        elif (item != '{') and (item != '}') and option == False:
            key, value = item.split(': ')
            config[key.replace('  ', '')] = value

        if option and (item != '  options: {'):
            key, value = item.split(': ')
            options[key.replace('    ', '')] = value

    return config


# Get list of data dog monitor config files
def get_file_list(monitor_cfg_dir):
    filelist = []
    cfg_path = monitor_cfg_dir

    for dirpath, dirnames, filenames in walk(monitor_cfg_dir):
        filelist.extend(filenames)
        break

    cfg_files = []
    for filename in filelist:
        if filename.split('.')[-1] == 'yaml':
            cfg_files.append(cfg_path + filename)

    return cfg_files


# Creates new monitor
def create_monitor(item):
    multi = item['multi']
    name = item['name']
    options = item['options']
    query = item['query']
    message = item['message']
    type = item['type']
    api.Monitor.create(type=type, query=query, name=name, message=message, options=options)


def get_all_monitors():
    return api.Monitor.get_all()


def get_monitor(id):
    return api.Monitor.get(id)


def del_monitor(id):
    api.Monitor.delete(id)


# Prints all existing monitors from datadog
def print_all_monitors():
    for monitor in get_all_monitors():
        for key, value in monitor.iteritems():
            print "{0} : {1}".format(key, value)
        print ""


# Deletes all existing monitors from datadog
def del_all_monitors():
    monitors = get_all_monitors()
    monitor_ids = []
    for monitor in monitors:
        monitor_ids.append(monitor['id'])

    for id in monitor_ids:
        del_monitor(id)


#print get_monitor()

#create_monitor()

print_all_monitors()

#del_all_monitors()

# for thing in get_file_list('/Users/thomasb/PycharmProjects/datadog_monitors/'):
#     print read_yaml_cfg(thing)
#     create_monitor(read_yaml_cfg(thing))