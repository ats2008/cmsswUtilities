import json
import numpy as np
import sys,os

fName=sys.argv[1]
f=open(fName, 'r')
txt=f.read()
f.close()
dTxt=""
for i in txt:
    dTxt+=i
data = json.loads(dTxt)
size=[]
name=[]
for blkCollection in data:
    for blk in blkCollection['block']:
        size.append(float(blk['size']))
        name.append(blk['name'])
        #print(blk['size'],"\t:\t",blk['name'])
size=np.asarray(size)
name=np.asarray(name)

sortedIdx=np.argsort(size)
sHere=0
for idx in sortedIdx:
    s=size[idx]/1e9
    sHere+=s
    if sHere>50e3:
        sHere=0
        print("\n###########################################\n")
    print("#  ",np.round(s,2)," GB \t",name[idx])
    print("rucio add-rule --ask-approval --lifetime 31536000 cms:dataset="+name[idx]+" 1 T2_IN_TIFR")
