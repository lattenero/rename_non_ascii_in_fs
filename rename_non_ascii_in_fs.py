#!/usr/bin/env python
# -*- coding: utf8 -*-

# Pythono3 code to rename multiple
# files or folder
import sys, getopt
import os
import re

init_path="/home/raoul/tmp"
duplicates=[]

def helper():
    print('path_check.py -p <path> -a action=list|test|rename -f special')
    sys.exit()

def is_ascii(s):
   return all(ord(c) < 128 for c in s)

def ascii_name(path,filename,filter={}):

    new_name = filename

    if filter['special'] == True:

      new_name = new_name.replace('à','a')
      new_name = new_name.replace('è','e')
      new_name = new_name.replace('é','e')
      new_name = new_name.replace('ù','u')
      new_name = new_name.replace('ò','o')
      new_name = new_name.replace('ì','i')
      new_name = new_name.replace('ç','c')

      new_name = new_name.replace('§','')
      new_name = new_name.replace('°','')
      new_name = new_name.replace(':','')
      new_name = new_name.replace(',','')
      new_name = new_name.replace(';','')
      new_name = new_name.replace('@','')
      new_name = new_name.replace('=','')

      new_name = new_name.replace('%','')
      new_name = new_name.replace('*','')
      new_name = new_name.replace('>','')
      new_name = new_name.replace('<','')
      new_name = new_name.replace('?','')
      new_name = new_name.replace('$','')
      new_name = new_name.replace('&','')
      new_name = new_name.replace('(','')
      new_name = new_name.replace(')','')

    new_name = re.sub(r'[^\x00-\x7F]+', '_', new_name)
    new_name = re.sub(r'^[\ ]+', '_', new_name)
    new_name = re.sub(r'__+', '_', new_name)
    new_name = re.sub(r'\ +', '\ ', new_name)
    new_name = re.sub(r'\.\.', '\.', new_name)

    return new_name

def check_path(path=None, action=None, filter={}):

   if os.path.exists(path) is not True:
      print("Path %s not found." % path)
      return None

   if os.path.isdir(path):
       if not path.endswith('/'):
           path = path + "/"

   for filename in os.listdir(path):
      new_name = ascii_name(path, filename, filter)
      if not new_name == filename:
          while os.path.exists(path + new_name):
              new_name = "_" + new_name

          if action == "rename":
              print("Rename: %s%s => %s%s" % (path, filename, path, new_name))
 #            os.rename(path + filename, path + new_name)
              sub_dir = path + new_name
          elif action == "test":
              print("Test: %s%s => %s%s" % (path, filename, path, new_name))
              sub_dir = path + filename

          elif action == "list":
              print("Found: %s%s" % (path, filename))
              sub_dir = path + filename

          if os.path.isdir(path + filename):
             check_path(sub_dir, action, filter)

          if os.path.isdir(path + new_name):
             check_path(sub_dir, action, filter)


def main(argv):
   path = ''
   filter={}
   action='list'
   filter['special'] = False
   try:
      opts, args = getopt.getopt(argv,"hp:a:f:",["path=","action=,filter="])
   except getopt.GetoptError:
      arg
      sys.exit(2)
   if opts == []:
      helper()
   for opt, arg in opts:
      if opt == '-h':
         helper()
      elif opt in ("-p", "--path"):
         path = arg
         if os.path.isdir(path):
             if not path.endswith('/'):
                 path = path + "/"
         else:
             print( path + "Is not a dir")
      elif opt in ("-a", "--action"):
         if arg in ('list','test','rename'):
            action = arg
         else:
            helper()
      elif opt in ("-f", "--filter"):
         if "special" in arg.split(","):
             filter['special'] = True


   print("Starting path is: %s " % path)
   check_path(path, action, filter)


if __name__ == "__main__":
   main(sys.argv[1:])