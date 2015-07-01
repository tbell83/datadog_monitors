from datadog import initialize, api
from os import walk
import yaml

options = {
    'api_key': 'd7ce8fdf7ff28617caf8f041c375ec58',
    'app_key': '62242ee5b9d7cfb79e20ae11fa6198d2db1f2d0a'
}

config_path = './'

initialize(**options)

# Read some YAML
def read_yaml(filename):
    fo = open(filename, 'r')
    yaml_file = yaml.load_all(fo)
    return yaml_file


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


# Deletes all existing monitors from datadog
def del_all_monitors():
    monitors = get_all_monitors()
    monitor_ids = []
    for monitor in monitors:
        monitor_ids.append(monitor['id'])

    for id in monitor_ids:
        del_monitor(id)


def validate_monitor(monitor):
    if monitor['type'] is None:
        return False
    elif monitor['query'] is None:
        return False
    else:
        return True


def compare_monitor(monitor1, monitor2):
    if (not validate_monitor(monitor1)) or (not validate_monitor(monitor2)):
        return False

    mon_match = False

    if (monitor1['query'] == monitor2['query']) and (monitor1['type'] == monitor2['type']) and (monitor1['name'] == monitor2['name']):
        mon_match = True

    if (monitor1 == monitor2):
        mon_match = True

    return mon_match


def get_additions(yaml_monitors, dd_monitors):
    to_be_added = []

    # print "Determining monitors to add:"
    for cfg_monitor in yaml_monitors:
        add_mon = False

        for dd_monitor in dd_monitors:
            # print "Comparing", cfg_monitor['name'], "to", dd_monitor['name']
            if not compare_monitor(cfg_monitor, dd_monitor):
                add_mon = True
            else:
                add_mon = False
                break

        if add_mon:
            to_be_added.append(cfg_monitor)

    return to_be_added


def get_removals(yaml_monitors, dd_monitors):
    to_be_removed = []

    # print "\nDetermining monitors to remove:"
    for dd_monitor in dd_monitors:
        remove_mon = False

        for cfg_monitor in yaml_monitors:
            # print "Comparing", cfg_monitor['name'], "to", dd_monitor['name']
            if not compare_monitor(cfg_monitor, dd_monitor):
                remove_mon = True
            else:
                remove_mon = False
                break

        if remove_mon:
            to_be_removed.append(dd_monitor['id'])

    return to_be_removed


def print_all_monitors(cfg_monitors, dd_monitors):
    print '\n'
    print 'Here\'s the YAML\n---------------\n'
    for file in cfg_monitors:
        for yaml_doc in read_yaml(file):
            print yaml_doc
            print 'message: ', yaml_doc['message'], type(yaml_doc['message'])
            print 'query:   ', yaml_doc['query'], type(yaml_doc['query'])
            print 'type:    ', yaml_doc['type'], type(yaml_doc['type'])
            print 'name:    ', yaml_doc['name'], type(yaml_doc['name'])
            print 'options: ', type(yaml_doc['options'])
            for item in yaml_doc['options']:
                print '\t', item, ': ', yaml_doc['options'][item], type(yaml_doc['options'][item])
            print '\n'

    print 'Here\'s the API output\n---------------\n'
    for monitor in dd_monitors:
        print monitor
        print 'message: ', monitor['message'], type(monitor['message'])
        print 'query:   ', monitor['query'], type(monitor['query'])
        print 'type:    ', monitor['type'], type(monitor['type'])
        print 'name:    ', monitor['name'], type(monitor['name'])
        print 'options: ', type(monitor['options'])
        for item in monitor['options']:
            print '\t', item, ': ', monitor['options'][item], type(monitor['options'][item])
        print '\n'


dd_monitors = get_all_monitors()
cfg_monitors = get_file_list(config_path)
yaml_monitors = []

for file in cfg_monitors:
    for yaml_doc in read_yaml(file):
        yaml_monitors.append(yaml_doc)

# print_all_monitors(cfg_monitors, dd_monitors)

print "YAML Monitors:"
for item in yaml_monitors:
    print item['name']

print "\nDatadog Monitors:"
for item in dd_monitors:
    print item['name']

print "\nMonitors to be added:"
for item in get_additions(yaml_monitors, dd_monitors):
    print item['name']

print "\nMonitors to be removed:"
for item in get_removals(yaml_monitors, dd_monitors):
    print item

additions = get_additions(yaml_monitors, dd_monitors)
if len(additions) > 0:
    for item in additions:
        print "\nAdding ", item['name'], " to DataDog"
        create_monitor(item)
else:
    print "Nothing to Add"

removals = get_removals(yaml_monitors, dd_monitors)
if len(removals) > 0:
    for item in get_removals(yaml_monitors, dd_monitors):
        print "\nRemoving", item, "from Datadog"
        del_monitor(item)
else:
    print "Nothing to remove"
