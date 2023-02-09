## Copy Files from EOS to Local Disc / T2

Make the filelist to be copied from the eos area. The accesible eos area are those that are accesible ib `crab checkwrite` [ so , the common eos area of the DPG/POG/PAGs in lxplus ]

A sample filelist may be seen from the `srcFiles` folder

Customise `misc/sampleScript.sh` to point to the correct filelists and destination folders

Execute 
```
./misc/sampleScript.sh <TOTAL JOBS TO BE MADE> <FILES PER JOB> 
```
