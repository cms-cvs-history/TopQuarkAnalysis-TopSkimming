#!/usr/bin/env python

import sys
import os
from math import sqrt

def ParseLog(filename):
    """Opens and parses filename file looking for "Number of RECO" or "Number of HLT" strings to find the appropriate line. Splits the line with ":" and gets the numbers to calculate efficiency. It returns the 2 lines as 2 strings and the calculated efficiency"""
    #Actual sample of log file lines to parse:
    #Number of RECO els with Pt > 20 is: 2451
    #Number of HLT Objects with pt > 18 matched to a RECO els with pt > 20 is: 2278
    #Number of events with at least one RECO els with Pt > 20 is: 2405
    #Number of events with at least one RECO 20 with Pt > 20 and at least one HLT object with pt > 18 is: 2268
    #Number of events with an HLT Objects with pt > 18 matched to a RECO els with pt > 20 is: 2245
    log=open(filename,'r')
    for line in log.readlines():
        if "Number of RECO" in line:
            Denominator=float(line.split(":")[1])
            DenLine=line.rstrip()
        if "Number of HLT" in line:
            Numerator=float(line.split(":")[1])
            NumLine=line.rstrip()
        if "Number of events with at least one RECO" in line:
            if "and at least one HLT object with pt > 18" in line:
                SkimEffNum=float(line.split(":")[1])
                SkimEffNumLine=line.rstrip()
            else:
                SkimEffDen=float(line.split(":")[1])
                SkimEffDenLine=line.rstrip()
        if "Number of events with an HLT Objects with pt > 18 matched to a RECO" in line:
            MatchSkimEffNum=float(line.split(":")[1])
            MatchSkimEffNumLine=line.rstrip()
    SkimEfficiency=SkimEffNum/SkimEffDen*100
    MatchSkimEfficiency=MatchSkimEffNum/SkimEffDen*100
    SkimmedLeptonEfficiency=Numerator/Denominator*100
    print filename
    JobId=os.path.basename(filename).split(".")[0].split("_")[1]
    return SkimEffDenLine,SkimEffNumLine,SkimEfficiency,MatchSkimEffNumLine,MatchSkimEfficiency,DenLine,NumLine,SkimmedLeptonEfficiency,JobId

def GetFiles(projectdirname):
    """Opens projectdirname/res, checks for tgz files, if there are it opens them all with 'tar -zxvf archive.tgz'. Then it gets a list of .stdout filenames. It checks the names for consistency (e.g. CMSSW_n.stdout, for N jobs check that there is no missing n in [1-N]). Returns a list of all filenames."""
    logsdir=projectdirname+"/res"
    ListLogs=os.listdir(logsdir)
    ListLogsPaths=filter(lambda x: x.endswith('stdout'),[os.getcwd()+"/"+logsdir+"/"+x for x in ListLogs])
    return ListLogsPaths

def AvgSigma(list):
    avg=sum(list)/len(list)
    squaresum=0
    for value in list:
        squaresum=squaresum+(value-avg)**2
    sigma=sqrt(squaresum/len(list))
    return avg,sigma
    

def main(argv=sys.argv):
    #Could add "absolute skimming efficiency", max/min number of events per job                                                         
    ProjectDir=argv[1]
    print "Checking task directory %s"%ProjectDir
    SkimEfficiencies=[]
    MatchSkimEfficiencies=[]
    LeptonEfficiencies=[]
    JobIds=[]
    for log in GetFiles(ProjectDir):
        (EvtRECOLine,EvtHLTLine,SkimEfficiency,EvtHLTMatchLine,MatchSkimEfficiency,RECOLine,HLTLine,LeptonEfficiency,JobId)=ParseLog(log)
        SkimEfficiencies.append(SkimEfficiency)
        MatchSkimEfficiencies.append(MatchSkimEfficiency)
        LeptonEfficiencies.append(LeptonEfficiency)
        JobIds.append(JobId)
        print "%s\n%s\nSkimming Efficiency(%%) is: %6.2f"%(EvtRECOLine,EvtHLTLine,SkimEfficiency) #'/afs/cern.ch/user/g/gbenelli/public/ForPuneeth/CMSSW_1.stdout')
        print "%s\n*MATCHED* Skimming Efficiency(%%) is: %6.2f"%(EvtHLTMatchLine,MatchSkimEfficiency) #'/afs/cern.ch/user/g/gbenelli/public/ForPuneeth/CMSSW_1.stdout') 
        print "%s\n%s\n*SKIMMED* lepton Efficiency(%%) is: %6.2f"%(RECOLine,HLTLine,LeptonEfficiency) #'/afs/cern.ch/user/g/gbenelli/public/ForPuneeth/CMSSW_1.stdout')
    (AverageSkimEff,SigmaSkimEff)=AvgSigma(SkimEfficiencies)
    (AverageMatchSkimEff,SigmaMatchSkimEff)=AvgSigma(MatchSkimEfficiencies)
    (AverageLeptonEff,SigmaLeptonEff)=AvgSigma(LeptonEfficiencies)
        
    print "============================================"
    print "Summary results"
    print "============================================"
    print "Total number of jobs: %s"%len(SkimEfficiencies)
    #Nasty kludge:
    EffType=["Skimming","*MATCHED* Skimming","Lepton Skimming"]
    i=0
    for Efficiencies in [SkimEfficiencies,MatchSkimEfficiencies,LeptonEfficiencies]:
        (AverageEff,SigmaEff)=AvgSigma(Efficiencies)
        NewEfficiencies=[]
        NewJobIds=[]
        print "Overall task average %s efficiency: %s "%(EffType[i],AverageEff)
        print "Overall task %s efficiency standard deviation: %s"%(EffType[i],SigmaEff)
        print "Maximum %s efficiency: %s at jobID %s"%(EffType[i],max(Efficiencies),JobIds[Efficiencies.index(max(Efficiencies))])
        print "Minimum %s efficiency: %s at jobID %s"%(EffType[i],min(Efficiencies),JobIds[Efficiencies.index(min(Efficiencies))])
        NewEfficiencies[:]=Efficiencies[:]
        NewEfficiencies.remove(min(Efficiencies))
        NewJobIds[:]=JobIds[:]
        NewJobIds.remove(JobIds[Efficiencies.index(min(Efficiencies))])
        print "Minimum %s efficiency eliminating above minimum: %s at jobID %s"%(EffType[i],min(NewEfficiencies),JobIds[NewEfficiencies.index(min(NewEfficiencies))])
        i=i+1
if __name__ == "__main__":
    main()

