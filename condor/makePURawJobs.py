#!/usr/bin/env python3

import os

NJOBS=64
NEVETS_PER_JOBS = -1
ZERO_OFFSET=0
PU_FNAMES_PER_JOB=2
PU_NEVENTS=-1

puPremixRaw_cfg='puRAWProduction_cfg.py'
puFileList ="pufilesCM1.txt"

gsFileNameTemplate='file:BsToMMG_GENSIM_@@IDX.root'
flowFileNameTemplate='file:BsToMMG_GENSIM-DIGI-RAW_pu30To80CM_@@IDX.root'

pwd=os.environ['PWD']
proxy_path=os.environ['X509_USER_PROXY']

xrdRedirector="root://cms-xrd-global.cern.ch/"

PUFnames=open(puFileList,'r')
pileUpFiles=PUFnames.readlines()
PUFnames.close()


puCfg_=open(puPremixRaw_cfg,'r')
puCfg=puCfg_.readlines()

if not os.path.exists('Jobs'):
    os.system('mkdir Jobs')
print("Making ",NJOBS," Jobs ")
for ii in range(NJOBS):
    i=ii+ZERO_OFFSET
    dirName= 'Jobs/Job_'+str(i)
    print(i," Job Made")
    if os.path.exists(dirName):
        k=True
    else:
        os.system('mkdir '+dirName)
    

    #TODO : make gensim fout name to be based on flowFileNameTemplate
    flowFileName_GS_OUT=flowFileNameTemplate.replace("@@IDX",str(i)) + '.root'

   ## PU PREMIX Step
    flowFileName_GS_OUT =gsFileNameTemplate.replace("@@IDX",str(i))
    flowFileName_PUPreMix_OUT=flowFileNameTemplate.replace("@@IDX",str(i))
    runScriptName=dirName+'/puRaw_run'+str(i)+'.sh'
    cfgFileName=dirName+'/puRaw_cmsConfig.py'
    cfgFile=open(cfgFileName,'w')
    for l in puCfg:
        if '@@COUNT' in l:
            l=l.replace('@@COUNT',str(PU_NEVENTS))
        if '@@GS_SOURCE' in l:
            l=l.replace('@@GS_SOURCE',flowFileName_GS_OUT)
        if '@@RAW_OUT' in l:
            l=l.replace('@@RAW_OUT',flowFileName_PUPreMix_OUT)
        if '@@PU_FLIST' in l:
             tmp=" "
             if len(pileUpFiles)<PU_FNAMES_PER_JOB:
                 print("PU fname count less than required .. assigning the PU files again ")
                 PUFnames=open(puFileList,'r')
                 pileUpFiles_=PUFnames.readlines()
                 PUFnames.close()
                 for ff in pileUpFiles_:
                     pileUpFiles.append(ff)
             
             for j in range(PU_FNAMES_PER_JOB):
                tmp+= "'"+xrdRedirector+pileUpFiles.pop(0)[:-1]+"',"
             tmp=tmp[:-1]
             l=l.replace("@@PU_FLIST",tmp)
        cfgFile.write(l)
    cfgFile.close()   
    
    runScript=open(runScriptName,'w')
    runScript.write('#!/bin/bash\n')
    runScript.write('set -x\n')
    runScript.write('source /cvmfs/cms.cern.ch/cmsset_default.sh \n')
    runScript.write('export X509_USER_PROXY='+proxy_path+'\n')
    runScript.write('cd '+pwd+'/'+dirName+'\n')
    runScript.write('eval `scramv1 runtime -sh`'+'\n')
    runScript.write('cmsRun puRaw_cmsConfig.py'+'\n')
    runScript.close()
    os.system('chmod +x '+runScriptName)

 
