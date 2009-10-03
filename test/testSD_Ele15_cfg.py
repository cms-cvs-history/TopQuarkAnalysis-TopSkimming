#set up a process , for e.g. RECO in this case
import FWCore.ParameterSet.Config as cms

process = cms.Process("TOPSKIM")

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = ''
process.MessageLogger.cerr.FwkReport.reportEvery = 1

# import of standard configurations
process.load('Configuration/StandardSequences/Services_cff')
process.load('FWCore/MessageService/MessageLogger_cfi')
process.load('Configuration/EventContent/EventContent_cff')
process.load("TopQuarkAnalysis.TopSkimming.topEleSkimFilterOctoberX_cff")
#process.load("CMS2.NtupleMaker.hltMaker_cfi")
#process.load("OctoberExercise.TopSkimValidation.topSkimValidation_cfi")

process.options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring('ProductNotFound')
)

process.source = cms.Source("PoolSource",
                            fileNames=cms.untracked.vstring('/store/mc/Summer09/TTbar/GEN-SIM-RECO/MC_31X_V3_SD_Ele15-v1/0003/A6127C58-F0AB-DE11-89B9-00237DA13C16.root',
        '/store/mc/Summer09/TTbar/GEN-SIM-RECO/MC_31X_V3_SD_Ele15-v1/0003/A43A086A-F0AB-DE11-863E-00237DA10D06.root',
        '/store/mc/Summer09/TTbar/GEN-SIM-RECO/MC_31X_V3_SD_Ele15-v1/0003/70FE322B-F2AB-DE11-A39E-00237DA1FD7C.root',
        '/store/mc/Summer09/TTbar/GEN-SIM-RECO/MC_31X_V3_SD_Ele15-v1/0003/38177E5B-F0AB-DE11-B0E4-001CC4116E30.root')
                            )
# Number of events:
process.maxEvents = cms.untracked.PSet(
   input = cms.untracked.int32(2500)
   )


#To get the trigger summary at the end of the log:
process.options=cms.untracked.PSet(wantSummary=cms.untracked.bool(True))


## define event selection
process.EventSelection = cms.PSet(
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('p1', 'p2', 'p3')
    )
)

##process.TFileService = cms.Service("TFileService", 
##      fileName = cms.string("SD_Ele15_histos.root")
##)

process.p1 = cms.Path(process.topHLT_Ele20_LW_L1R_Seq)# * process.topSkimValidation)
process.p2 = cms.Path(process.topHLT_Ele15_LW_L1R_Seq)# * process.topSkimValidation)
process.p3 = cms.Path(process.topHLT_Ele15_SC10_LW_L1R_Seq)# * process.topSkimValidation)

process.output=cms.OutputModule("PoolOutputModule",
                                process.EventSelection,
                               #process.AODEventContent, #Dump AOD format
                               fileName=cms.untracked.string('TTbarSD_Ele15_HLTPtFilter.root'),
                                )


process.output.outputCommands = cms.untracked.vstring( 'drop *' )
process.output.outputCommands.extend(cms.untracked.vstring('keep *_*Maker*_*_TOPSKIM*'))



#Run the output path:
process.outpath = cms.EndPath(process.output)

#Add the HLTSummaryFilter category (used in LogInfo in the HLTSummaryFilter)
process.MessageLogger.categories.append('HLTSummaryFilter')


