#!/usr/bin/python

import sys, getopt
import os, errno
import datetime
import shlex, subprocess

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def execCall(cmd):
   print 'Executing\n' + cmd
   args = shlex.split(cmd)
   subprocess.call(args)


def main(argv):
   url = ''
   start = ''
   dur = ''
   try:
      opts, args = getopt.getopt(argv,"hu:s:d:",["url=","start=","duration="])
   except getopt.GetoptError:
      print 'vidsplit.py -u <videourl> -s <start_time_in_sec> -d <duration_in_sec>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'vidsplit.py -u <videourl> -s <start_time_in_sec> -d <duration_in_sec>'
         sys.exit()
      elif opt in ("-u", "--url"):
         url = arg
      elif opt in ("-s", "--start"):
         start = arg
      elif opt in ("-d", "--duration"):
         dur = arg
   print 'url "', url
   print 'start "', start
   print 'duration "', dur
   today = datetime.date.today()
   datestr = today.strftime('%Y%b%d').strip()
   mkdir_p(datestr)
   #Getting filename
   cmd = 'youtube-dl --get-filename --get-title --get-description -o ' + datestr + '/tmp_vid.%(ext)s ' + url
   print 'Executing\n' + cmd
   args = shlex.split(cmd)
   output,error = subprocess.Popen(args,stdout = subprocess.PIPE, stderr= subprocess.PIPE,close_fds=True).communicate()
   filedesc, filetitle,dlfilename = output.splitlines()
   print "Title:", filetitle , "\nFilename:", dlfilename, "\nDesc:", filedesc
   dlfn, dlext = dlfilename.split('.')
   # Executing Actual command
   cmd = 'youtube-dl -q -o ' + datestr + '/tmp_vid.%(ext)s ' + url
   execCall(cmd)
   print 'Executing\n' + cmd
   args = shlex.split(cmd)
   subprocess.call(args)
   # Splittin with ffmpeg
   splitfilename = dlfn + '_' + start + '-' + dur + '.' + dlext
   cmd = 'ffmpeg -i ' + dlfilename + ' -ss ' + start + ' -t ' + dur + ' -vcodec copy -acodec copy ' + splitfilename
   execCall(cmd)
   # upload file
   #youtube-upload --email=pkpoliticsvideolib@gmail.com --password=eokvpzgoqwhljbhk  --title="Test" --description="Test Description" --category=Education --keywords="Yaseen, Snippet" ../part2.mp4 
   cmd = 'youtube-upload --email=pkpoliticsvideolib@gmail.com --password=eokvpzgoqwhljbhk --title="' + filetitle + '" --description="' + filedesc + '" --category="Education" --keywords="PTI" ' + splitfilename
   execCall(cmd)
   cmd = 'rm ' + dlfilename + ' ' + splitfilename
   execCall(cmd)

if __name__ == "__main__":
   main(sys.argv[1:])
