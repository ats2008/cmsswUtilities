#!/usr/bin/bash

NJOBS=${1-5}
FILES_PER_JOB=${2-1}
MAXEVENTS=${3--1}
echo NJOBS : $NJOBS
echo FILES_PER_JOB : $FILES_PER_JOB
echo MAXEVENTS : $MAXEVENTS
echo ""

declare -a SourceFiles=(\
   "srcFiles/eraC_unpacked.fls" \
)

declare -a tagArr=(\
"eraC_unpackedL1EG" \
)

declare -a Destination=(\
"root://se01.indiacms.res.in:1094//dpm/indiacms.res.in/home/cms/store/user/athachay/l1egamma/store/unpacked2022/eraC/" \
)

for i in "${!tagArr[@]}"; do 
    echo $i : ${jobArr[$i]}
    src=${SourceFiles[$i]}
    TAG=${tagArr[$i]}
    DEST=${Destination[$i]}
    echo ./misc/makeT2CopiesWithCustomNaming.py \
        $src \
        $DEST \
        $FILES_PER_JOB \
        $NJOBS \
        $TAG
done    
