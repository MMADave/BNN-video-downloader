"""
MMADave 2015
How to use BNNvideofetch.py
This version is for windows system.
Dependencies are wget to download the 2nd m3u8 file.

Usage

1. Find a video from http://m.bnn.ca/video/ you'd like to download.
http://m.bnn.ca/video/-/f/RZo3/click?itemId=668997&p_p_lifecycle=1 for example.
2. download the manifest.m3u8
Video comes in a variety of video qualities ranging from 2-16 (lowest to best), even numbers only.
3. Run script like so: "python BNNvideofetch.py manifest.m3u8 16 optionalcustomfilename"

A second m3u8 specific to the video quality will be downloaded. 
An html will be created with links to video fragment files.
A delete batch file will be created for file clean-up except for the video file.
A copy batch file will be created to stitch video fragment files together.
4. Download the video fragments using your favourite download manager like DownThemAll.
5. Run the copy batch file to do the stitching.
6. Run the Delete batch file to clean-up the files.
7. Watch the video using your favourite media player!
"""
import sys
import re
import os
import Tkinter

def downloadm3u8(manifestfilename):
    manifestfile= open(manifestfilename)
    lines=manifestfile.readlines()
    quality = int(sys.argv[2])
    if quality%2 or quality<2 or quality>16:
        print "video quality argument choices are 2-16, even numbers only"
        sys.exit()
    m3u8link=lines[quality]

    manifestfile.close()
    os.system("wget -c " + m3u8link)
    m3u8filename = re.split("[/ \n \r]",m3u8link)
    Tkinter.Tk().clipboard_append(m3u8filename[7])
    if quality == 16:
        videofragmenturl=m3u8link.replace(m3u8filename[7],"") #get url to video frags
    else:
        videofragmenturl=m3u8link.replace(m3u8filename[7]+"\n","") #get url to video frags
    return (videofragmenturl, m3u8filename[7])

def getfragments(videofragmenturl, m3u8filename):
    m3u8file= open(m3u8filename)
    m3u8line=m3u8file.readlines()
    htmllist= open(m3u8filename+".html","w")
    counter=0
    for x in xrange(6,len(m3u8line),2):
	counter+=1
	filepath=videofragmenturl+m3u8line[x]
	#create html links to video fragment files
	htmllist.write("<a href=\"%s\">%d</a>\n" % (filepath[:-1],counter))
    htmllist.close()
    #create delete batch file for file clean-up
    deletebat= open("DELETE"+m3u8filename+".bat","w")
    deletebat.write("del " + m3u8line[x][:-12] +"*ts "+m3u8filename+" "+m3u8filename+".html "+m3u8filename+".bat DELETE"+m3u8filename+".bat")
    deletebat.close()
    #create copy batch file to stitch video fragment files together
    copybat= open(m3u8filename+".bat","wb+")
    copybat.write("copy /b ")
    for x in xrange(6,len(m3u8line),2):
        copybat.write("%s + " % m3u8line[x][:-1])
    copybat.seek(-2, os.SEEK_END)
    copybat.truncate() #remove last "+ " 
    if len(sys.argv)<4: #if condition for custom video file naming
        copybat.write("%s" % m3u8filename[:-5])
    else:
        copybat.write("\"%s BNN.mp4\"" % str(sys.argv[3]))
    copybat.close()
    useragent="\"Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SPH-L710 Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30\""
    #os.system("pb "+m3u8filename+".html") #open video fragment files links in Firefox
    m3u8file.close()

def main():
    (videofragmenturl, m3u8filename)=downloadm3u8(sys.argv[1])
    getfragments(videofragmenturl, m3u8filename)

if __name__ == '__main__':
    main()
