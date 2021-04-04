import os

NJOBS_LAST = 0
NJOBS = 2
NEVENTS_PER_JOB=-1
NFILES_PER_JOB=10

fCSubmitScript=open('SubmitScript.sh','w')

f=open('cmsrunTemplate.py','r')
text=f.readlines()
f.close()

f=open('submitTemplate.jdl','r')
condor_submit_txt=f.readlines()
f.close()

f=open('executeTemplate.sh','r')
execute_script=f.readlines()
f.close()

for i in range(NJOBS_LAST,NJOBS_LAST+NJOBS):
    print("making the job  :  ",i)
    fout=open('cExecute_'+str(i)+".sh",'w')
    for l in execute_script:
        l=l.replace('!@#$',str(i))
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
        if "NoFilter_tsgWithPhotos_X.root" in l:
		l=""
		for j in range(NFILES_PER_JOB):
			l+="        'file:data/NoFilter_tsgWithPhotos_"+str(i*NFILES_PER_JOB+j)+".root',\n"
	fout.write(l)
    fout.write("process.maxEvents.input = "+str(NEVENTS_PER_JOB)+"\n")
    fout.close()
    
    submitCommand="condor_submit  "+"cSubmit_"+str(i)+".jdl"
    fCSubmitScript.write(submitCommand+"\n")
fCSubmitScript.close()
os.system('chmod 777 SubmitScript.sh')
os.system('chmod 777 cExecute_*')

