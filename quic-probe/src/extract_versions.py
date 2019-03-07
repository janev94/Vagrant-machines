# -*- coding: utf-8 -*-

#! /bin/env python2
import json
import struct
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
import base64
import socket
# LD_PRELOAD=/usr/lib/libz.so



def decode_tag(tag, data):
    raw_data = base64.b64decode(data)

    try:
        if tag in ('VER ', 'SCFG_AEAD', 'SCFG_KEXS'):                         # List of tags
            return [raw_data[i:i+4] for i in range(0, len(raw_data), 4)]
       
        else:                                                                   # Unknown
            #print repr(tag)
            return data

    except Exception as e:
        pass
        #sys.stdout.write(u"Error decoding tag {}: {}\n".format(tag, e))
    return data


#TODO:
# Normalize tags before working with them
if __name__ == '__main__':
    REJ_MSG = "rejTags"
    SHLO_MSG = "shloTags"
    version = []
    for line in sys.stdin:
        jline = json.loads(line)
        #decode REJ_RESP
        if REJ_MSG in jline and 'VER ' in jline[REJ_MSG]:
            #Decode msg from rejection response            
            version.extend(decode_tag('VER ', jline[REJ_MSG]['VER ']))


        #decode SHLO_RESP
        if SHLO_MSG in jline and 'VER ' in jline[SHLO_MSG]:
            version.extend(decode_tag('VER ', jline[SHLO_MSG]['VER ']))

    print version

'''
    if version:
        print 'Extracted versions %s' % version
    else:
        print 'No versions found, server response was: %s' % json.dumps(jline)
'''
