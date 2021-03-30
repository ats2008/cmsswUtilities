import os,sys,time
import string
import re
import argparse
import textwrap
from operator import itemgetter

from json import dumps,load
import numpy as np
from itertools import groupby
from textwrap import dedent
import pandas as pd


FULL_DETAILS =False
#FULL_DETAILS =True
HSO6_CONVERSION_FACTOR = 21.0
tot_kevt = 0
tot_cpu_ksec = 0
f = open("Revised20Jan2021genstudyDavid.txt",'r')

Lines = f.readlines()
itemCount=0

data={}
with open('mcmResponse.json', 'r') as fp:
    data = load(fp)

exception_prepids =["SUS-RunIISummer20UL18wmLHEGEN-00044","EXO-RunIISummer20UL18wmLHEGEN-00130","SUS-RunIISummer20UL18GEN-00013","SUS-RunIISummer20UL18wmLHEGEN-00018","EXO-RunIISummer20UL18GEN-00075"]

compiledTags = {
#'amcatnlo':'amcatnlo',
#'mlm':'mlm',
#'fxfx':'fxx',
#'madgraph':'madgraph',
#'openloops':'openloops',
#'powheg':'powheg',
#'pythia':'pythia',
#'comphep':'COMPHEP',
'ttv_all':'MLM/FxFx/amc@nlo',
'ttv_lo':'MLM',
'ttv_nlo':"FxFx/amc@nlo",
'ttv_fxfx':'FxFx',
'ttv_amcatnlo':'amc@nlo',
'st' : 'PW/amc@nlo/ch',
'st_ch' : 'comphep',
'st_nlo' : 'PW/amc@nlo',
'st_pw' : 'Powheg',
'st_amcatnlo' : 'amc@nlo',
'vv_all' : 'PW/amc@nlo/FxFx/MG5/PY',
'vv_lo': 'MG5/PY',
'vv_madgraph':'MG5_aMC',
'vv_pythia':'pythia8',
'vv_nlo' : 'PW/amc@nlo/FxFx',
'vv_pw' : 'Powheg',
'vv_amcatnlo':'amc@nlo',
'vv_fxfx' : 'FxFx',
'qcd_all' : 'PW/amc@nlo/FxFx/MG5/PY',
'qcd_lo': 'MG5/PY',
'qcd_madgraph':'MG5_aMC',
'qcd_pythia':'pythia8',
'qcd_nlo' : 'PW/amc@nlo/FxFx/Herwig',
'qcd_herwig' : 'Herwig',
'qcd_pw' : 'Powheg',
'qcd_amcatnlo':'amc@nlo',
'qcd_fxfx' : 'FxFx',
}



compiledStats ={}
for tag in compiledTags:
	compiledStats[tag]= {'prepids':[],'datasets':[],'totalEvents' : 0, 'totalCpuSec' :0 , 'cpuSecPerEvent' : -1,'hs06':-1};
def updateCompiledStats( stats,cStats ):
	cStats['totalEvents']+=stats['events']
	cStats['totalCpuSec']+=stats['cpuTime']
	cStats['prepids'].append(stats['prepid'])
	cStats['datasets'].append(stats['dataset'])
	if cStats['totalEvents'] > 0 :
		cStats['cpuSecPerEvent'] = cStats['totalCpuSec']/cStats['totalEvents']
		cStats['hs06']           = cStats['cpuSecPerEvent']*HSO6_CONVERSION_FACTOR

stats={}

for line in Lines:
 #   itemCount+=1
 #   if itemCount >5:
 #	break
    if line.startswith("#") is False:
        split_strings = line.split()    
        pid = split_strings[1].strip()
#        res = get_request(pid)
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

                if 'pythia8' in dsetname: 		stats[pid]['pythia']=True
		else :				stats[pid]['pythia']=False
  
                if 'madgraph' in dsetname: 		stats[pid]['madgraph']=True
		else :				stats[pid]['madgraph']=False
  
    		if 'mlm' in dsetname: 		stats[pid]['mlm']=True
		else :				stats[pid]['mlm']=False
		
                stats[pid]['events'] 		= int(split_strings[3])*1000
                stats[pid]['cpuPerEvent'] 	= float(split_strings[5])
                stats[pid]['cpuPerSimEvent'] 	= float(split_strings[9])
                stats[pid]['initTime'] 		= float(split_strings[13])
                stats[pid]['cpuTime'] 		= float(split_strings[15])*1e3
                stats[pid]['hs06']  		= HSO6_CONVERSION_FACTOR*stats[pid]['cpuTime']/stats[pid]['events']

		stat=stats[pid]
		
		#if stat['amcatnlo'] :	updateCompiledStats(stat,compiledStats['amcatnlo'])
		#if stat['mlm'] :	updateCompiledStats(stat,compiledStats['mlm'])
		#if stat['powheg'] :	updateCompiledStats(stat,compiledStats['powheg'])
		#if stat['openloops'] :	updateCompiledStats(stat,compiledStats['openloops'])
		#if stat['fxfx'] :	updateCompiledStats(stat,compiledStats['fxfx'])
		#if stat['madgraph'] :	updateCompiledStats(stat,compiledStats['madgraph'])
		#if stat['pythia'] :	updateCompiledStats(stat,compiledStats['pythia'])
		#if stat['comphep'] :	updateCompiledStats(stat,compiledStats['comphep'])


		if dsetname.startswith('ttz') or dsetname.startswith('ttw'):
			updateCompiledStats(stat,compiledStats['ttv_all'])
			if stat['mlm'] :
				updateCompiledStats(stat,compiledStats['ttv_lo'])
			if stat['fxfx'] or stat['amcatnlo'] :
				updateCompiledStats(stat,compiledStats['ttv_nlo'])
			if stat['fxfx'] :
				updateCompiledStats(stat,compiledStats['ttv_fxfx'])
			if stat['amcatnlo'] :
				updateCompiledStats(stat,compiledStats['ttv_amcatnlo'])
	        
		if dsetname.startswith("st_"):
	      		updateCompiledStats(stat,compiledStats['st'])
			if stat['amcatnlo'] or stat['powheg']:
				updateCompiledStats(stat,compiledStats['st_nlo'])
			if stat['amcatnlo']:
				updateCompiledStats(stat,compiledStats['st_amcatnlo'])
			if stat['comphep']:
				updateCompiledStats(stat,compiledStats['st_ch'])
			if stat['powheg']:
				updateCompiledStats(stat,compiledStats['st_pw'])
	
		if ('ww' in dsetname) or  ('wz' in dsetname) or ('wzjj_ewk' in dsetname) or  ('wwg' in dsetname) or ('wzg' in dsetname):
			updateCompiledStats(stat,compiledStats['vv_all'])
		
			if stat['madgraph'] or stat['pythia'] :
				updateCompiledStats(stat,compiledStats['vv_lo'])
			if stat['fxfx'] or stat['amcatnlo'] or stat['powheg']:
				updateCompiledStats(stat,compiledStats['vv_nlo'])
			if stat['fxfx'] :
				updateCompiledStats(stat,compiledStats['vv_fxfx'])
			if stat['amcatnlo'] :
				updateCompiledStats(stat,compiledStats['vv_amcatnlo'])
			if stat['powheg'] :
				updateCompiledStats(stat,compiledStats['vv_pw'])
			if stat['madgraph'] :
				updateCompiledStats(stat,compiledStats['vv_madgraph'])
			if stat['pythia'] :
				updateCompiledStats(stat,compiledStats['vv_pythia'])
				
		if dsetname.startswith("qcd_"):
			updateCompiledStats(stat,compiledStats['qcd_all'])

			if stat['madgraph'] or stat['pythia']:
				updateCompiledStats(stat,compiledStats['qcd_lo'])
			
			if stat['amcatnlo'] or stat['fxfx'] or stat['powheg'] or stat['herwig']:
				updateCompiledStats(stat,compiledStats['qcd_nlo'])
	
			if stat['madgraph'] :
				updateCompiledStats(stat,compiledStats['qcd_madgraph'])
			
			if stat['pythia'] :
				updateCompiledStats(stat,compiledStats['qcd_pythia'])
			
			if stat['amcatnlo'] :
				updateCompiledStats(stat,compiledStats['qcd_amcatnlo'])
			
			if stat['powheg'] :
				updateCompiledStats(stat,compiledStats['qcd_pw'])
			
			if stat['herwig'] :
				updateCompiledStats(stat,compiledStats['qcd_herwig'])
			
			if stat['fxfx'] :
				updateCompiledStats(stat,compiledStats['qcd_fxfx'])
			


	
#                print " | "+split_strings[1].center(36)+" | "+split_strings[3].rjust(8)+" | "+split_strings[5].rjust(7)+" | "+split_strings[7].rjust(6)+" | "+split_strings[9].rjust(8)+" | "+split_strings[11].rjust(5)+" | "+split_strings[13].rjust(8)+" | "+split_strings[15].rjust(12)+" | "+str((21)*float(split_strings[15])/(float(split_strings[3]))).rjust(12)+"[ "+str(stats[pid]['hs06'])+"] | "+split_strings[19].ljust(95)

           

fstring  ="|"+"TAG".center(20)+" | "
fstring +="Total Events".rjust(12)+" | "
fstring +="Total cpu s".rjust(12)+" | "
fstring +="HS06".center(12)+" | "
fstring +="Remarks".center(30) + " |"
print("".center(len(fstring),"-"))
print(fstring)
print("".center(len(fstring),"-"))

tags=list(compiledStats.keys())
tags.sort()
for cTag in tags:
	fstring  ="|"+cTag.center(20)+" | "
	fstring +="{0:0.2f}".format(compiledStats[cTag]['totalEvents']/1e6).rjust(12)+" | "
	fstring +="{0:0.2f}".format(compiledStats[cTag]['totalCpuSec']/1e9).rjust(12)+" | "
	fstring +="{0:0.2f}".format(compiledStats[cTag]['hs06']).rjust(12)+" | "
	fstring +=compiledTags[cTag].center(30) + " |"
	print(fstring)
print("".center(len(fstring),"-"))

print("\n")

if  FULL_DETAILS:
	print("Datasets and More".center(81))
	
	for cTag in compiledStats:
		print("\n")
		fstring=(" ~ ~   "+cTag+"   ~ ~").center(81)
		print("".center(len(fstring),"-"))
		print(fstring)
		print("".center(len(fstring),"-"))
		
		idxs=np.argsort(compiledStats[cTag]['datasets'])
		i=0
		for idx in idxs:
			i+=1
			fstring=str(i).ljust(3)+" , "+compiledStats[cTag]['datasets'][idx].ljust(60)+" ( "
			fstring+=compiledStats[cTag]['prepids'][idx].center(30)+" )"
			print(fstring)

#while len(res) !=0:
#    for r in res:
#        print str(r['prepid'])+"  "+str(r['dataset_name'])+"  "+str(r['status']+"   "+str(r['completed_events']))  
#        ntotalrequests += 1
#        ntotalevents += r['total_events']
#        ntotalcompletevents += r['completed_events']
#    page += 1
##    res = mcm.get('requests',query='member_of_campaign=RunIISummer19UL16wmLHEGEN&status=done', page=page)
