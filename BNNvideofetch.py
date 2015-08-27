"""
MMADave 2015
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
