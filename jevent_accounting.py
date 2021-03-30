import os,sys,time
import string
import re
import argparse
import textwrap
from operator import itemgetter

os.system('env -i KRB5CCNAME="$KRB5CCNAME" cern-get-sso-cookie -u https://cms-pdmv.cern.ch/mcm/ -o cookiefile.txt --krb --reprocess')
#os.system('source /afs/cern.ch/cms/PPD/PdmV/tools/McM/getCookie.sh')
#os.system('cern-get-sso-cookie -u https://cms-pdmv.cern.ch/mcm/ -o ~/private/prod-cookie.txt --krb --reprocess')
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')

from rest import McM
from json import dumps,load
import numpy as np
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



dataMode="rest"
#dataMode="json"
FULL_DETAILS =False
#FULL_DETAILS =True
HSO6_CONVERSION_FACTOR = 21.0
tot_kevt = 0
tot_cpu_ksec = 0
f = open("Revised20Jan2021genstudyDavid.txt",'r')

Lines = f.readlines()
itemCount=0

data={}
if dataMode=="json":
	with open('mcmResponse.json', 'r') as fp:
    		data = load(fp)

exception_prepids =["SUS-RunIISummer20UL18wmLHEGEN-00044","EXO-RunIISummer20UL18wmLHEGEN-00130","SUS-RunIISummer20UL18GEN-00013","SUS-RunIISummer20UL18wmLHEGEN-00018","EXO-RunIISummer20UL18GEN-00075"]

compiledTags = {
'all' : 'ALL',
'lo': 'MG5/PY',
'madgraph':'MG5_aMC',
'madgraphmlm':'madgraphMLM',
'pythia':'pythia8',
'pythiamlm':'pythiaMLM',
'nlo' : 'PW/amc@nlo/FxFx/Herwig',
'herwig' : 'Herwig',
'powheg' : 'Powheg',
'amcatnlo':'amc@nlo',
'mlm' : 'mlm',
'openloops' : 'openloops',
'fxfx' : 'FxFx',
'comphep' : 'comphep',
'photos' : 'PHOTOS',
'minnlo' : 'minnlo',
'nnlo' : '~~', 
}

#   ----------------------------------------------------- #

# ADD NEW TAG HERE and then add the corresponging update cmd in parsing the loop
heads = ['ttv','st','vv','qcd','VpJets']
#   ----------------------------------------------------- #

tires=['lo','nlo','nnlo']
compiledData={}
for head in heads:
	compiledData[head]={}
	compiledData[head][head+'_all']={'prepids':[],'datasets':[],'totalEvents' : 0, 'totalCpuSec' :0 , 'cpuSecPerEvent' : -1,'hs06':-1}
	compiledData[head]['lo']   = {'pythia':{},'madgraph':{}}
	compiledData[head]['nlo']     = {'powheg':{},'amcatnlo':{},'herwig':{},'fxfx':{},'mlm':{},'pythiamlm':{},'madgraphmlm':{},'minnlo':{},'photos':{}}
	compiledData[head]['nnlo']    = {}
	for kys in tires:
		compiledData[head][kys+'_all']={'prepids':[],'datasets':[],'totalEvents' : 0, 'totalCpuSec' :0 , 'cpuSecPerEvent' : -1,'hs06':-1}
		for kkys in compiledData[head][kys]:
			compiledData[head][kys][kkys]={'prepids':[],'datasets':[],'totalEvents' : 0, 'totalCpuSec' :0 , 'cpuSecPerEvent' : -1,'hs06':-1}

compiledGeneratorStats={}
for head in compiledTags:
	compiledGeneratorStats[head]={'prepids':[],'datasets':[],'totalEvents' : 0, 'totalCpuSec' :0 , 'cpuSecPerEvent' : -1,'hs06':-1}

def updateCompiledStats( stats,compiledData ):
	compiledData['totalEvents']+=stats['events']
	compiledData['totalCpuSec']+=stats['cpuTime']
	compiledData['prepids'].append(stats['prepid'])
	compiledData['datasets'].append(stats['dataset'])
	if compiledData['totalEvents'] > 0 :
		compiledData['cpuSecPerEvent'] = compiledData['totalCpuSec']/compiledData['totalEvents']
		compiledData['hs06']           = compiledData['cpuSecPerEvent']*HSO6_CONVERSION_FACTOR

def compileStats( stats,cStats,tag):
	updateCompiledStats(stats,cStats[tag][tag+'_all'])
	for preci in tires:
		isPreci=False
		
		for genMachine in cStats[tag][preci]:
			isPreci = isPreci or stats[genMachine]
			if stats[genMachine]:
				updateCompiledStats(stats,cStats[tag][preci][genMachine])
		if isPreci:
			updateCompiledStats(stats,cStats[tag][preci+'_all'])
stats={}

for line in Lines:
    if line.startswith("#") is False:
        split_strings = line.split()    
        pid = split_strings[1].strip()
	if dataMode=="rest":
		print("doing  : ",pid)
	        res=get_request(pid)
        elif dataMode=="json":
		res = data[pid]

	res = [res]
        for r in res:
            stats[pid]={}
            if pid in exception_prepids:    
                split_strings.insert(19,"?????????? | ???????") 
#            elif "SUS-RunIISummer20UL18wmLHEGEN-00044" not in pid and "EXO-RunIISummer20UL18wmLHEGEN-00130" not in pid and "SUS-RunIISummer20UL18GEN-00013" not in pid: 
#            elif "SUS-RunIISummer20UL18wmLHEGEN-00044" not in pid and "EXO-RunIISummer20UL18wmLHEGEN-00130" not in pid and "SUS-RunIISummer20UL18GEN-00013" not in pid: 
            else:
                split_strings.insert(19,r['dataset_name'])
                split_strings.insert(20,"")
                final_string = ' '.join(split_strings)
                
		stats[pid]['dataset'] = r['dataset_name']
	        stats[pid]['prepid']  = pid
                stats[pid]['events'] 		= int(split_strings[3])*1000
                stats[pid]['cpuPerEvent'] 	= float(split_strings[5])
                stats[pid]['cpuPerSimEvent'] 	= float(split_strings[9])
                stats[pid]['initTime'] 		= float(split_strings[13])
                stats[pid]['cpuTime'] 		= float(split_strings[15])*1e3
                stats[pid]['hs06']  		= HSO6_CONVERSION_FACTOR*stats[pid]['cpuTime']/stats[pid]['events']
 
		dsetname= stats[pid]['dataset'].lower()
   
                if 'herwig' in dsetname: 	stats[pid]['herwig']=True
		else :				stats[pid]['herwig']=False		
                
                if 'minnlo' in dsetname: 	stats[pid]['minnlo']=True
		else :				stats[pid]['minnlo']=False		
                
		if 'comphep' in dsetname: 	stats[pid]['comphep']=True
		else :				stats[pid]['comphep']=False		
                
                if 'openloops' in dsetname: 	stats[pid]['openloops']=True
		else :				stats[pid]['openloops']=False		
                
                if 'powheg' in dsetname: 	stats[pid]['powheg']=True
		else :				stats[pid]['powheg']=False		
                
                if 'fxfx' in dsetname: 		stats[pid]['fxfx']=True
		else :				stats[pid]['fxfx']=False		
 
                if 'amcatnlo' in dsetname: 	stats[pid]['amcatnlo']=True
		else :				stats[pid]['amcatnlo']=False		

                if 'pythia8' in dsetname: 	stats[pid]['pythia']=True
		else :				stats[pid]['pythia']=False
  
                if 'madgraph-' in dsetname:	stats[pid]['madgraph']=True
		else :				stats[pid]['madgraph']=False
  
                if 'pythiamlm' in dsetname:	stats[pid]['pythiamlm']=True
		else :				stats[pid]['pythiamlm']=False
  
                if 'madgraphmlm' in dsetname:	stats[pid]['madgraphmlm']=True
		else :				stats[pid]['madgraphmlm']=False
  
    		if 'mlm' in dsetname: 		stats[pid]['mlm']=True
		else :				stats[pid]['mlm']=False
		
    		if 'photos' in dsetname: 	stats[pid]['photos']=True
		else :				stats[pid]['photos']=False
		
    		if 'minnlo' in dsetname: 	stats[pid]['minnlo']=True
		else :				stats[pid]['minnlo']=False
		
                
		stat=stats[pid]
		
		if stat['amcatnlo'] :	updateCompiledStats(stat,compiledGeneratorStats['amcatnlo'])
		if stat['mlm'] :	updateCompiledStats(stat,compiledGeneratorStats['mlm'])
		if stat['powheg'] :	updateCompiledStats(stat,compiledGeneratorStats['powheg'])
		if stat['openloops'] :	updateCompiledStats(stat,compiledGeneratorStats['openloops'])
		if stat['fxfx'] :	updateCompiledStats(stat,compiledGeneratorStats['fxfx'])
		if stat['madgraph'] :	updateCompiledStats(stat,compiledGeneratorStats['madgraph'])
		if stat['madgraphmlm']:	updateCompiledStats(stat,compiledGeneratorStats['madgraphmlm'])
		if stat['pythia'] :	updateCompiledStats(stat,compiledGeneratorStats['pythia'])
		if stat['pythiamlm'] :	updateCompiledStats(stat,compiledGeneratorStats['pythiamlm'])
		if stat['comphep'] :	updateCompiledStats(stat,compiledGeneratorStats['comphep'])
		if stat['minnlo'] :	updateCompiledStats(stat,compiledGeneratorStats['minnlo'])
		if stat['photos'] :	updateCompiledStats(stat,compiledGeneratorStats['photos'])


		if dsetname.startswith('ttz') or dsetname.startswith('ttw'):
			compileStats(stat,compiledData,'ttv')        
		if dsetname.startswith("st_"):
			compileStats(stat,compiledData,'st')        
		if ('ww' in dsetname) or  ('wz' in dsetname) or ('wzjj_ewk' in dsetname) or  ('wwg' in dsetname) or ('wzg' in dsetname):
			compileStats(stat,compiledData,'vv')
		if dsetname.startswith("qcd_"):
			compileStats(stat,compiledData,'qcd')
		if ("wjet" in dsetname) or ("zjet" in dsetname) or ("dyjets" in dsetname):
			compileStats(stat,compiledData,'VpJets')
	
#                print " | "+split_strings[1].center(36)+" | "+split_strings[3].rjust(8)+" | "+split_strings[5].rjust(7)+" | "+split_strings[7].rjust(6)+" | "+split_strings[9].rjust(8)+" | "+split_strings[11].rjust(5)+" | "+split_strings[13].rjust(8)+" | "+split_strings[15].rjust(18)+" | "+str((21)*float(split_strings[15])/(float(split_strings[3]))).rjust(18)+"[ "+str(stats[pid]['hs06'])+"] | "+split_strings[19].ljust(95)

tabS="  "

def printLinearTable(compiledData):
	
	fstring  ="|"+"TAG".center(20)+" | "
	fstring +="Total Events [1e6]".rjust(18)+" | "
	fstring +="Total cpu s [1e9]".rjust(18)+" | "
	fstring +="HS06".center(18)+" | "
	fstring +="Remarks".center(30) + " |"
	print("".center(len(fstring),"-"))
	print(fstring)
	print("".center(len(fstring),"-"))
	for tag in compiledData:
		if compiledData[tag]['totalEvents']<1:
			continue
		fstring  ="|"+(tabS+tag).ljust(20)+" | "
		fstring +="{0:0.2f}".format(compiledData[tag]['totalEvents']/1e6).rjust(18)+" | "
		fstring +="{0:0.2f}".format(compiledData[tag]['totalCpuSec']/1e9).rjust(18)+" | "
		fstring +="{0:0.2f}".format(compiledData[tag]['hs06']).rjust(18)+" | "
		fstring +=compiledTags[tag].center(30) + " |"
		print(fstring)
	print("".center(len(fstring),"-"))
	print("")
	
def printTableOfCompiledData(compiledData,tires,printDetails=False):
	
	fstring  ="|"+"TAG".center(20)+" | "
	fstring +="Total Events [1e6]".rjust(18)+" | "
	fstring +="Total cpu s [1e9]".rjust(18)+" | "
	fstring +="HS06".center(18)+" | "
	fstring +="Remarks".center(30) + " |"
	print("".center(len(fstring),"-"))
	print(fstring)
	print("".center(len(fstring),"-"))

	for tag in compiledData:
		fstring  ="|"+(tabS+tag).ljust(20)+" | "
		fstring +="{0:0.2f}".format(compiledData[tag][tag+'_all']['totalEvents']/1e6).rjust(18)+" | "
		fstring +="{0:0.2f}".format(compiledData[tag][tag+'_all']['totalCpuSec']/1e9).rjust(18)+" | "
		fstring +="{0:0.2f}".format(compiledData[tag][tag+'_all']['hs06']).rjust(18)+" | "
		fstring +=compiledTags['all'].center(30) + " |"
		print(fstring)
		for preci in tires:
			if compiledData[tag][preci+'_all']['totalEvents']<1:
				continue
			fstring  ="|"+(tabS*2+preci).ljust(20)+" | "
			fstring +="{0:0.2f}".format(compiledData[tag][preci+'_all']['totalEvents']/1e6).rjust(18)+" | "
			fstring +="{0:0.2f}".format(compiledData[tag][preci+'_all']['totalCpuSec']/1e9).rjust(18)+" | "
			fstring +="{0:0.2f}".format(compiledData[tag][preci+'_all']['hs06']).rjust(18)+" | "
			fstring +=compiledTags[preci].center(30) + " |"
			print(fstring)
		
			for genMachine in compiledData[tag][preci]:
				if compiledData[tag][preci][genMachine]['totalEvents'] <1 :
					continue
				fstring  ="|"+(tabS*3+genMachine).ljust(20)+" | "
				fstring +="{0:0.2f}".format(compiledData[tag][preci][genMachine]['totalEvents']/1e6).rjust(18)+" | "
				fstring +="{0:0.2f}".format(compiledData[tag][preci][genMachine]['totalCpuSec']/1e9).rjust(18)+" | "
				fstring +="{0:0.2f}".format(compiledData[tag][preci][genMachine]['hs06']).rjust(18)+" | "
				fstring +=compiledTags[genMachine].center(30) + " |"
				print(fstring)
	print("".center(len(fstring),"-"))
	print("\n")
	if not printDetails:
		return
	
	def printDetailsOfItem(cTag,compiledStats):
	        print("\n")
		fstring=(" ~ ~   "+cTag+"   ~ ~").center(81)
		print("".center(len(fstring),"-"))
		print(fstring)
		print("".center(len(fstring),"-"))
		
		idxs=np.argsort(compiledStats['datasets'])
		i=0
		for idx in idxs:
			i+=1
			fstring=str(i).ljust(3)+" , "+compiledStats['datasets'][idx].ljust(60)+" ( "
			fstring+=compiledStats['prepids'][idx].center(30)+" )"
			print(fstring)

       	for tag in compiledData:
		printDetailsOfItem(tag+"_all",compiledData[tag][tag+'_all']);
		for preci in tires:
			if compiledData[tag][preci+'_all']['totalEvents']<1:
				continue
			printDetailsOfItem(tag+"_"+preci+"_all",compiledData[tag][preci+'_all']);
			for genMachine in compiledData[tag][preci]:
				if compiledData[tag][preci][genMachine]['totalEvents'] <1 :
					continue
				printDetailsOfItem(tag+"_"+preci+"_"+genMachine,compiledData[tag][preci][genMachine]);

printTableOfCompiledData(compiledData,tires,FULL_DETAILS)    
printLinearTable(compiledGeneratorStats)
