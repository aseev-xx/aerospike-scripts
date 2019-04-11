#!/usr/bin/python

import json
import subprocess
import re

AE_VERSION_FORMAT = {
    'new': '3.15',
    'old': '3.10',
    'oldest': '3.8.5'
}

def convert_tpl(version):

    tpl = tuple(int(n) for n in version.split('.'))
    return tpl

def get_raw_object():

    cmd = '/usr/bin/aql -c "show sets" -o json'
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    return process.communicate()
    
def ae_tool():

    cmd = '/usr/bin/aql -V'
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = process.communicate()

    for ver in out.split('\n'):
        if re.match(r'Version', ver):
	    vr = ver.split(' ')[1]

    ver_control = 0

    if convert_tpl(vr) < convert_tpl(AE_VERSION_FORMAT['old']):
    	#print 'current: ' + vr + ', oldest: ' + AE_VERSION_FORMAT['oldest']
    	ver_control = 1
    elif convert_tpl(vr) < convert_tpl(AE_VERSION_FORMAT['new']):
    	#print 'current: ' + vr + ', old: ' + AE_VERSION_FORMAT['old']
    	ver_control = 1
    else:	
    	#print 'current: ' + vr + ', new: ' + AE_VERSION_FORMAT['new']
    	ver_control = 0
    
    return ver_control

def get_json_object(raw_object, old_version):
    new_str = ""

    for str in raw_object.split("\n"):

	if old_version:
	    str = re.sub('^]$', '],', str)

	if not ( re.match(r'$', str) or re.match(r'\w+', str)):
	    new_str = new_str + str

    if old_version:
        new_str = re.sub('],$',']',new_str)
	new_str = '[' + new_str + ']'

    return  json.loads(new_str)

def prepare_graphite_metrics(obj, old_version):
    node_obj = get_json_object(obj, old_version)

    message = node_obj[0] # first element is current node 127.0.0.1
  
    if not old_version:
        if message[-1]['node']:
    	    message = message[:-1] # last element is node  local

    for elem in message:
	
	msg = ''
	# backward compatibility for oldest version (like 3.8.3 and oldest)
	if 'ns_name' in elem:
	    value = 'ae.' + elem['ns_name'] + '.' + elem['set_name']
            msg = '%s %s' % (value, elem['n_objects'])
	else:
	    value = 'ae.' + elem['ns'] + '.' + elem['set']
            msg = '%s %s' % (value, elem['objects'])

        print msg

def main():
    version = ae_tool()
    obj, err = get_raw_object()
    prepare_graphite_metrics(obj, version)


if __name__ == '__main__':
    main()
