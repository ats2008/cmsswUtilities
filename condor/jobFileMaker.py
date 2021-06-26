#!/usr/bin/env python3

import os

NJOBS_LAST = 0
NJOBS = 8
NEVENTS_PER_JOB=-1
NFILES_PER_JOB=1

fCSubmitScript=open('SubmitScript.sh','w')

source_server ='cms-xrd-global.cern.ch'
source_server = 'se01.indiacms.res.in'

f=open('cmsrunTemplate.py','r')
text=f.readlines()
f.close()

f=open('submitTemplate.jdl','r')
condor_submit_txt=f.readlines()
f.close()

f=open('executeTemplate.sh','r')
execute_script=f.readlines()
f.close()

f=open('fnames.txt')
source_fnames=f.readlines()
f.close()

def writeSourceToFile(fout, source_fnames, NFILES_PER_JOB):
    n=min(len(source_fnames),NFILES_PER_JOB)
    fout.write('process.source = cms.Source("PoolSource",\n')
    fout.write('    fileNames = cms.untracked.vstring(\n')
    
    for i in range(n):
        fname=source_fnames.pop()[:-1]
        l='           "root://'+source_server+'/'+fname+'",\n'
        fout.write(l)
    fout.write('    )\n)\n')        

for i in range(NJOBS_LAST,NJOBS_LAST+NJOBS):
    print("making the job  :  ",i)
    fout=open('cExecute_'+str(i)+".sh",'w')
    for l in execute_script:
        l=l.replace('!@#$',str(i))
        if '@@WD' in l:
            l=l.replace('@@WD',os.getenv('PWD'))
        if '@@VOMS_PROXY' in l:
            l=l.replace('@@VOMS_PROXY',os.getenv('VOMS_PROXY'))
        fout.write(l)
    fout.close()  
    
    fout=open('cSubmit_'+str(i)+".jdl",'w')
    for l in condor_submit_txt:
        l=l.replace('!@#$',str(i))
        fout.write(l)
    fout.close()
    
    fout=open('cmsrun_'+str(i)+"_cfg.py",'w')
    for l in text:
        l=l.replace('!@#$',str(i*NFILES_PER_JOB)+"To"+str(i*NFILES_PER_JOB+NFILES_PER_JOB-1))
        if "@@source" in l:
            k=len(source_fnames)
            writeSourceToFile(fout,source_fnames,NFILES_PER_JOB)
            print("adding ",k-len(source_fnames), "files to the job ")
            continue
        fout.write(l)
    fout.write("process.maxEvents.input = "+str(NEVENTS_PER_JOB)+"\n")
    fout.close()
    
    submitCommand="condor_submit  "+"cSubmit_"+str(i)+".jdl"
    fCSubmitScript.write(submitCommand+"\n")
    if len(source_fnames)==0:
        break
fCSubmitScript.close()
os.system('chmod 777 SubmitScript.sh')
os.system('chmod 777 cExecute_*')

