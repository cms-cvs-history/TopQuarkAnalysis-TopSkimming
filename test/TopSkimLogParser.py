#!/usr/bin/env python

import sys
import os
from math import sqrt

def ParseLog(filename):
    """Opens and parses filename file looking for "Number of RECO" or "Number of HLT" strings to find the appropriate line. Splits the line with ":" and gets the numbers to calculate efficiency. It returns the 2 lines as 2 strings and the calculated efficiency""" 
    log=open(filename,'r')
    for line in log.readlines():
        if "Number of RECO" in line:
            Denominator=float(line.split(":")[1])
            DenLine=line.rstrip()
        if "Number of HLT" in line:
            Numerator=float(line.split(":")[1])
            NumLine=line.rstrip()
    SkimEfficiency=Numerator/Denominator*100
    print filename
    JobId=os.path.basename(filename).split(".")[0].split("_")[1]
    return DenLine,NumLine,SkimEfficiency,JobId

def GetFiles(projectdirname):
    """Opens projectdirname/res, checks for tgz files, if there are it opens them all with 'tar -zxvf archive.tgz'. Then it gets a list of .stdout filenames. It checks the names for consistency (e.g. CMSSW_n.stdout, for N jobs check that there is no missing n in [1-N]). Returns a list of all filenames."""
    logsdir=projectdirname+"/res"
    ListLogs=os.listdir(logsdir)
    ListLogsPaths=filter(lambda x: x.endswith('stdout'),[os.getcwd()+"/"+logsdir+"/"+x for x in ListLogs])
    return ListLogsPaths

def main(argv=sys.argv):
    #Could add "absolute skimming efficiency", max/min number of events per job
    ProjectDir=argv[1]
    print "Checking task directory %s"%ProjectDir
    Efficiencies=[]
    JobIds=[]
    for log in GetFiles(ProjectDir):
        (RECOLine,HLTLine,Efficiency,JobId)=ParseLog(log)
        Efficiencies.append(Efficiency)
        JobIds.append(JobId)
        print "%s\n%s\nSkimming Efficiency(%%) is: %6.2f"%(RECOLine,HLTLine,Efficiency) #'/afs/cern.ch/user/g/gbenelli/public/ForPuneeth/CMSSW_1.stdout')
    AverageEff=sum(Efficiencies)/len(Efficiencies)
    squaresum=0
    for value in Efficiencies:
        squaresum=squaresum+(value-AverageEff)**2
    sigma=sqrt(squaresum/len(Efficiencies))
    print "============================================"
    print "Summary results"
    print "============================================"
    print "Total number of jobs: %s"%len(Efficiencies)
    print "Overall task average efficiency: %s "%AverageEff
    print "Overall task efficiency standard deviation: %s"%sigma
    print "Maximum efficiency: %s at jobID %s"%(max(Efficiencies),JobIds[Efficiencies.index(max(Efficiencies))])
    print "Minimum efficiency: %s at jobID %s"%(min(Efficiencies),JobIds[Efficiencies.index(min(Efficiencies))])
    Efficiencies.remove(min(Efficiencies))
    JobIds.remove(JobIds[Efficiencies.index(min(Efficiencies))])
    print "Minimum efficiency eliminating above minimum: %s at jobID %s"%(min(Efficiencies),JobIds[Efficiencies.index(min(Efficiencies))])
if __name__ == "__main__":
    main()

