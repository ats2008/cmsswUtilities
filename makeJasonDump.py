import os,sys,time
import string
import re
import argparse
import textwrap
import json  

from operator import itemgetter

os.system('env -i KRB5CCNAME="$KRB5CCNAME" cern-get-sso-cookie -u https://cms-pdmv.cern.ch/mcm/ -o cookiefile.txt --krb --reprocess')
#os.system('source /afs/cern.ch/cms/PPD/PdmV/tools/McM/getCookie.sh')
#os.system('cern-get-sso-cookie -u https://cms-pdmv.cern.ch/mcm/ -o ~/private/prod-cookie.txt --krb --reprocess')
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')

from rest import McM
from json import dumps
from itertools import groupby
from textwrap import dedent
import pandas as pd

#mcm = McM(cookie='cookiefile.txt', dev=False, debug=False)
mcm = McM(id='no-id', dev=False, debug=False)
mcm_link = "https://cms-pdmv.cern.ch/mcm/"

def get_request(prepid):
    result = mcm._McM__get('public/restapi/requests/get/%s' % (prepid))
    if not result:
        return {}

    result = result.get('results', {})
    return result

tot_kevt = 0
tot_cpu_ksec = 0
#f = open("Jan2021_application_assessment.txt",'r')
f = open("Revised20Jan2021genstudyDavid.txt",'r')
Lines = f.readlines()
itemCount=0

mcmRestResponses={}

for line in Lines:
    if line.startswith("#") is False:

        itemCount+=1
        split_strings = line.split()    
        pid = split_strings[1].strip()
        res = get_request(pid)
	print(itemCount," / ",len(Lines),"  : ",pid)
	mcmRestResponses[pid]=res
f.close()
f=open("mcmResponse.json",'w')
json.dump(mcmRestResponses, f)
f.close()
