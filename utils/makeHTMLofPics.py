#!/usr/bin/env python3

"""
    Makes a html webpage with all the images in a source folder ( pathToDir ).
    By default the images will be copied to a new directory '_src' and index.html will created pointing those copied images
    the folder and index.hml could be moved to the cms www area for public acess
    
    For setting image with/height pass  --width / --height [ -w / -h ]
    For setting the page header pass --title [ -t ]
    For setting the image type to look for pass --suffix -p ]


Usage  : ./makeHTMLofPics.py <pathToDir>  < other args >

"""

import  os,sys

import argparse,datetime

html_beg="<!DOCTYPE html>\n\
<html>\n\
<head>\n\
<style>\n\
img {\n\
  width: 100%;\n\
}\n\
</style>\n\
</head>\n\
<body>\n\
"

html_end="\n\
</body>\n\
</html>\n\
"

if __name__ =="__main__":

    parser = argparse.ArgumentParser(description='example png to HTML maker')
    parser.add_argument('source',nargs="+",help='source folder')
    parser.add_argument('--suffix','-p',default='.png',help='filetype [extn : png,jpg,jpeg ..] ')
    parser.add_argument('--out','-o',default="index",help='output fname')
    parser.add_argument('--unique','-u',default="0",help='get name from the datetime')
    parser.add_argument('--width','-w',default="300",help='pic width')
    parser.add_argument('--height','-l',default="300",help='pic height')
    parser.add_argument('--title','-t',default="plots",help='page title')
    args = parser.parse_args()

    source=args.source
    ftype=args.suffix
    uniqueName=args.unique=="True"
    h=args.height
    w=args.width
    title=args.title

    print(uniqueName,args.unique)
    

    plotNames=[]
    for directory in source:
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            if os.path.isfile(f):
                if ftype in f:
                    plotNames.append(f)
    uname=args.out
    uniqID=''
    now=datetime.datetime.now()
    if uniqueName:
        uniqID=str(now).replace(' ','').replace(':','').replace('-','').replace('.','')
        uname+=uniqID
    print(uname)

    os.system('rm -rf '+uname)
    os.system('mkdir '+uname)

    
    for pname in plotNames:
        os.system('cp '+pname+' ' + uname )               
    
    foutname=args.out
    fout=open(foutname+'.html','w')
    fout.write(html_beg)
    fout.write('<br>Aravind T S, TIFR, Mumbai<br>\n')
    fout.write('<hr>\n')
    fout.write('<br><h1>'+title+'</h1><br>\n')

    for filename in os.listdir(uname):
        f = os.path.join(uname,filename)
        if not os.path.isfile(f): continue
        print("adding ",f)
        imgCMD='<img src="{}" alt="HTML5 Icon" style="width:{}px;height:{}px;">'.format(f,w,h)
        fout.write(imgCMD+"\n")

    fout.write('<hr>\n')
    fout.write("<em> Created at : " +  now.strftime("%c")+ " </em>\n")
    fout.write('<hr>\n')
    fout.write(html_end)
    fout.close()
