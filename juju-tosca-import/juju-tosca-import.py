#!/usr/bin/python
'''
  Copyright 2014 IBM Corporation 
  Michael Chase-Salerno(bratac@linux.vnet.ibm.com)

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
'''
import yaml
import pprint
import getopt
import sys
import zipfile
import tempfile
import os.path
import logging
from inspect import currentframe, getframeinfo

try:
    from yaml import CSafeLoader as Loader
except ImportError:
    from yaml import SafeLoader as Loader


def usage():
    print 'juju-tosca-import.py [--help] [--description] <CSAR zip file>'

def parse_yaml(yamlfile):
  #open the yaml file, and load the content
  try:
    yf=open(yamlfile,"r")
  except:
    print "Unable to open yaml file", yamlfile
    sys.exit(1)

  content=yf.read()
  yc=yaml.load(content, Loader=Loader)
  logger.debug("Yaml content:")
  pprint.pprint(yc)

def unpack_zip(zipfn):
  #zip file needs to be in the TOSCA CSAR format
  try:
    zip = zipfile.ZipFile(zipfn, 'r') 
  except:
    print "Unable to open zip file", zipfn
    usage()
    sys.exit(2)
 
  logger.debug(zip.namelist())
  tmpdir=tempfile.mkdtemp(prefix="CSAR_", dir="./")
  zip.extractall(tmpdir)
  return tmpdir

def parse_metafile(tmpdir):
  if not os.path.isfile(tmpdir+"/TOSCA-Metadata/TOSCA.meta"):
    print "TOSCA.meta not found in CSAR file"
    sys.exit(1)
  tfile = open(tmpdir+'/TOSCA-Metadata/TOSCA.meta', 'r')
  tlines = tfile.readlines()
  for line in tlines:
    if (line.startswith("Name")):
      attr,value = line.split(":",2)
      # if it's a yaml file pointer, need to find it here, and parse it?
      logger.debug(tmpdir+"/"+value.strip())
      parse_yaml(tmpdir+"/"+value.strip())

def create_charms():
  #create charms based on yaml file
  pass

def create_relations():
  # create relations based on yaml file
  pass

#Main
def main():
  #setup debug logging  
  global logger
  logger = logging.getLogger('root')
  FORMAT = "[%(filename)s:%(lineno)s-%(funcName)s()]%(message)s"
  logging.basicConfig(format=FORMAT)
  logger.setLevel(logging.DEBUG)
   
  #input params
  zipfn=''
  yamlfile=''
  try:
    opts, args = getopt.getopt(sys.argv[1:], "hd", ["help", "description"])
  except getopt.GetoptError as err:
    print str(err)
    usage()
    sys.exit(2)

  for opt,arg in opts:
    if opt in ("-h", "--help"):
      usage()
      sys.exit()
    elif opt in ("-d", "--description"):
      print "Juju plugin to import a orchestration specification from a CSAR file containing YAML files"
      sys.exit()
    else:
        assert False, "unhandled option"

  if not (len(args) == 1):
    usage()
    sys.exit(2)

  # Unpack the zip file into a tmp directory
  zipfn=sys.argv[1] 
  tmpdir=unpack_zip(zipfn)

  # Read the TOSCA.meta file
  yamls=parse_metafile(tmpdir)
    
  create_charms()
  create_relations()


if __name__ == "__main__":
  main()

