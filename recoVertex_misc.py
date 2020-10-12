ValidationRawFile = "RawCUDAVertexValidation.root"

import DataFormats.FWLite as fwlite
from ROOT import TFile, TTree, TH1D, TCanvas
from array import array
import numpy as np


def d2(v1,v2):
    return (v1[0]-v2[0])**2+(v1[1]-v2[1])**2+(v1[2]-v2[2])**2

def printVertex(vertex): 
    print "        x = ",vertex[0]
    print "        y = ",vertex[1]
    print "        z = ",vertex[2]
    print "     chi2 = ",vertex[3]
    print "    nchi2 = ",vertex[5]
    print "     ndof = ",vertex[4]
    print "trackSize = ",vertex[6]
   
def getComparison(vertexA,vertexB):
    ma=[False for va in vertexA]
    mb=[False for vb in vertexB]
    
    for i in range(len(vertexA)):
        for j in range(len(vertexB)):
            if mb[j]:
                continue
            d=d2(vertexA[i],vertexB[j])
            if d<1e-8:
                ma[i]=True
                mb[j]=True
    return ma,mb               

def DoMatchingTest(ValidationRawFile,VertexCollectionA,VertexCollectionB,printVtx=False):
    
    print "doing for  File              : ",ValidationRawFile
    print "doing for  VertexCollection  : ",VertexCollectionA," , ",VertexCollectionB

    events = fwlite.Events("file:"+ValidationRawFile)

    vertexCollectionA_ =fwlite.Handle("std::vector<reco::Vertex>")
    vertexCollectionB_ =fwlite.Handle("std::vector<reco::Vertex>")
    
    print "Total Number of Events = ",events.size()
    vertexCountA=0
    vertexCountB=0
    evtId=0
    missCount=0
    addlCount=0
    for i, event in enumerate(events):
        evtId+=1
        if i%1000==0:
            print "At event : ",i
        
        event.getByLabel(VertexCollectionA,vertexCollectionA_)
        event.getByLabel(VertexCollectionB,vertexCollectionB_)

        if not vertexCollectionA_.isValid():
            continue

        verticesA= vertexCollectionA_.product()
        verticesB= vertexCollectionB_.product()

        vertexCountA+=verticesA.size()
        vertexCountB+=verticesB.size()

        vtxsA,vtxsB=[],[]
        for vtx in verticesA:
            vtxsA.append([vtx.x(),vtx.y(),vtx.z(),vtx.chi2(),vtx.ndof(),vtx.normalizedChi2(),vtx.tracksSize()])
        for vtx in verticesB:
            vtxsB.append([vtx.x(),vtx.y(),vtx.z(),vtx.chi2(),vtx.ndof(),vtx.normalizedChi2(),vtx.tracksSize()])
     #   print vtxsA
     #   print vtxsB

    #   print "Matching for evtId ",evtId
        ma,mb=getComparison(vtxsA,vtxsB);
    
        if False in ma  and False in mb:
            print "\n"
            #continue
        if False not in ma  and False not in mb:
            continue
        if False in ma :
            print "Misses in  ", evtId," = " , [ma.count(False) ], "  len(vtxsA)  = ",len(vtxsA)  
            for i in range(len(vtxsA)):
                if not ma[i] and printVtx:
                    printVertex(vtxsA[i])
            missCount+=ma.count(False) 
        if False in mb :
            print "Additionals at  ", evtId, " = " , [mb.count(False) ]
            for i in range(len(vtxsB)):
                if not mb[i] and printVtx:
                    printVertex(vtxsB[i])
            addlCount+=mb.count(False)
    print "Miss count = ",missCount
    print "Additional count = ",addlCount

def makeVertexNtuples(ValidationRawFile,VertexCollection,recreateFile=False,fOutName="VertexNtuples.root"):
    
    print "doing for  File              : ",ValidationRawFile
    print "doing for  VertexCollection  : ",VertexCollection

    events = fwlite.Events("file:"+ValidationRawFile)

    vertexCollection_ =fwlite.Handle("std::vector<reco::Vertex>")
   
 
    if recreateFile:
        afile=TFile(fOutName,"RECREATE")
    else : 
        afile=TFile(fOutName,"update")

    afile.cd()
    currDir = afile.mkdir(VertexCollection);    
    currDir.cd()
    
    
    vertexTree=TTree("vertices","Vertices")
    
    vx   = array('d',[0])
    vy   = array('d',[0])
    vz   = array('d',[0])
    vrho = array('d',[0])
    chi2  = array('d',[0])
    ndof  = array('d',[0])
    nchi2 = array('d',[0])
    nTracks=array('I',[0])
    evtId=array('i',[0])
    
    
    vertexTree.Branch("x",vx,"x/D")
    vertexTree.Branch("y",vy,"y/D")
    vertexTree.Branch("z",vz,"z/D")
    vertexTree.Branch("rho",vrho,"rho/D")
    vertexTree.Branch("chi2",chi2,"chi2/D")
    vertexTree.Branch("ndof",ndof,"ndof/D")
    vertexTree.Branch("nchi2",nchi2,"nchi2/D")
    vertexTree.Branch("nTracks",nTracks,"nTracks/i")
    vertexTree.Branch("event_id",evtId,"event_id/i")
    
    print "Total Number of Events = ",events.size()
    trigEvtCount=0
    vertexCount=0
    for i, event in enumerate(events):
        evtId[0]+=1
        if i%1000==0:
            print "At event : ",i
        
        event.getByLabel(VertexCollection,vertexCollection_)
        if not vertexCollection_.isValid():
            continue

        trigEvtCount+=1
        
        vertices= vertexCollection_.product()
        vertexCount+=vertices.size()
        for vtx in vertices:
            vx[0]   =vtx.x()
            vy[0]   =vtx.y()
            vz[0]   =vtx.z()
            vrho[0] =(vtx.x()**2+vtx.y()**2)**0.5
            chi2[0] =vtx.chi2()
            ndof[0] =vtx.ndof()
            nchi2[0]=vtx.normalizedChi2()
            nTracks[0]=vtx.tracksSize()

            vertexTree.Fill()
 
    print "VeretexCollection                        :   ",VertexCollection
    print "Total number of events processed         :    ",evtId[0]
    print "Total number of events triggered evts    :    ",trigEvtCount
    print "Total number of Vertices                 :    ",vertexCount
    
    currDir.cd()
    vertexTree.Write()




if __name__== "__main__" :
    
    DO_EVENT_BY_EVENT_MATCH=True
    DO_CONVERSION_TO_NTUPLETS=True

    if(DO_EVENT_BY_EVENT_MATCH):
        print(" Doing Event by event matching of the collections ")
        DoMatchingTest(ValidationRawFile,'hltTrimmedPixelVertices','hltTrimmedPixelVerticesValidation',printVtx=True)
        #DoMatchingTest(ValidationRawFile,'hltTrimmedPixelVerticesCPUValidation','hltTrimmedPixelVerticesValidation',printVtx=True)
        #DoMatchingTest(ValidationRawFile,'hltTrimmedPixelVertices','hltTrimmedPixelVerticesCPUValidation',printVtx=True)

    if(DO_CONVERSION_TO_NTUPLETS):
        makenewFile=True
        count=0
        verticesofInterest=['hltPixelVertices','hltTrimmedPixelVertices','hltTrimmedPixelVerticesValidation','hltTrimmedPixelVerticesCPUValidation']
        print("CONVERTING TO ROOT NTUPLETS ")
        for verexCol in verticesofInterest:
            count+=1
            print "\n\n doing  ",count,"  / ",len(verticesofInterest)
            makeVertexNtuples(ValidationRawFile,verexCol,makenewFile)
            makenewFile=False
