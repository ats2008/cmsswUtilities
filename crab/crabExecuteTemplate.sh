cmsrel CMSSW_11_0_2
cd CMSSW_11_0_2/src
cmsenv
cp ../../code.tar .
tar -xf code.tar
scram b
cp ../../* .
cmsRun -j FrameworkJobReport.xml -p PSet.py
mv FrameworkJobReport.xml ../../
mv *.root ../../
