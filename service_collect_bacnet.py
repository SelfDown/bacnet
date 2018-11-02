#!/usr/bin/env python
# -*- coding: utf_8 -

import sys
from collections import deque

from bacpypes.debugging import bacpypes_debugging, ModuleLogger
from bacpypes.consolelogging import ConfigArgumentParser

from bacpypes.core import run, stop, deferred
from bacpypes.iocb import IOCB

from bacpypes.pdu import Address
from bacpypes.apdu import ReadPropertyRequest

from bacpypes.app import BIPSimpleApplication
from bacpypes.object import get_object_class, get_datatype
from bacpypes.local.device import LocalDeviceObject


this_application = None

tag_list = None
tag_keys={}
result=[]

count = 0
class ReadPropertyApplication(BIPSimpleApplication):

  def __init__(self, *args):
    BIPSimpleApplication.__init__(self, *args)

  def requests(self):
    global tag_list,this_application,tag_keys,count
    for item in tag_list:
      tag_keys[item["device_address"]+"#"+item["object_types"]+"#"+item["object_instance"]+"#"+item["prop"]]={"tag":item["tag"],"prop":item["prop"]}
      request = ReadPropertyRequest(destination=Address(item["device_address"]),
      objectIdentifier=(item["object_types"],int(item["object_instance"])),
      propertyIdentifier=item["prop"])
      iocb = IOCB(request)
      iocb.add_callback(self.callback)
      this_application.request_io(iocb)


  def callback(self, iocb):
    try:
      global result,count,tag_keys
      import datetime
      dt = datetime.datetime.now()
      count+=1
      #print iocb.ioResponse,iocb.ioError
      if iocb.ioResponse:
        apdu = iocb.ioResponse
        key= str(apdu.pduSource)+"#"+str(apdu.objectIdentifier[0])+"#"+str(apdu.objectIdentifier[1])+"#"+apdu.apdu_contents()["propertyIdentifier"]
        tag = tag_keys.pop(key)
        timestamp=dt.strftime("%Y-%m-%d %H:%M:%S")
        datatype = get_datatype(apdu.objectIdentifier[0], apdu.apdu_contents()["propertyIdentifier"])
        if not datatype:
          raise TypeError("unknown datatype")
        
        value = apdu.propertyValue.cast_out(datatype)

        result.append({"timestamp":timestamp,"value":str(value),"item":tag["tag"],"quality":"Good"})

      if count == len(tag_list):
        stop()
    except Exception as e:
      print e,"=================================="
      raise e
    

#
#   __main__
#
# 
def getData(collection):
  global this_application, device_address, object_identifier, property_list
  # 清空数组
  global result,tag_list,tag_keys,count
  print collection
  result=[]
  tag_list=[]
  tag_keys={}
  count =0
  parser = ConfigArgumentParser(description=__doc__)
  args = parser.parse_args()
  
  tag_list = collection["bacnet_items"]
  try:
    this_device = LocalDeviceObject(ini=args.ini)
    this_application = ReadPropertyApplication(this_device, args.ini.address)
    deferred(this_application.requests)
    run()
    this_application.close_socket()

  except Exception as e:
    print str(e)
    return {"data":"采集失败","success":"false"}
  import datetime
  dt = datetime.datetime.now()
  timestamp=dt.strftime("%Y-%m-%d %H:%M:%S")
  for item in tag_keys:
    result.append({"timestamp":timestamp,"value":None,"item":tag_keys[item]['tag'],"quality":"Error"})
  return {"data":result,"success":"true"}

if __name__ == "__main__":
  #test = {"service_type":"service_collect_bacnet","service":"test_bacnet","backup":"test","bacnet_items":[{"device_address":"192.168.6.243","object_types":"analogInput","object_instance":"3000028","prop":"presentValue","tag":"tag_test"}]}
  test = {"service_type":"service_collect_bacnet","service":"test_bacnet","backup":"test","bacnet_items":[{"device_address":"192.168.6.243","object_types":"analogInput","object_instance":"3000028","prop":"objectName","tag":"tag1"},{"device_address":"192.168.6.243","object_types":"analogInput","object_instance":"3000028","prop":"presentValue","tag":"tag2"}]}
  #test = {"service_type":"service_collect_bacnet","service":"test_bacnet","backup":"test","bacnet_items":[{"device_address":"192.168.6.243","object_types":"analogInput","object_instance":"3000028","prop":"objectName","tag":"tag2"}]}
  print getData(test),"-----------------"
