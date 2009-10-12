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
process.load('TopQuarkAnalysis.TopSkimming.topEleSkimValidationOctoberX_cfi')

process.options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring('ProductNotFound')
)

process.source = cms.Source("PoolSource",
                            fileNames=cms.untracked.vstring('/store/mc/Summer09/Zee/GEN-SIM-RECO/MC_31X_V3_SD_Ele15-v1/0003/C62D4337-F1AB-DE11-A96B-0018F3D0970E.root')
                            )
# Number of events:
process.maxEvents = cms.untracked.PSet(
   input = cms.untracked.int32(200)
   )


#To get the trigger summary at the end of the log:
process.options=cms.untracked.PSet(wantSummary=cms.untracked.bool(True))


## define event selection
process.EventSelection = cms.PSet(
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('p1', 'p2', 'p3')
    )
)

process.p1 = cms.Path(process.topHLT_Ele20_LW_L1R_Seq)
process.p2 = cms.Path(process.topHLT_Ele15_LW_L1R_Seq)
process.p3 = cms.Path(process.topHLT_Ele15_SC10_LW_L1R_Seq)
process.ep = cms.Path(process.topElsSkimValidation)

process.output=cms.OutputModule("PoolOutputModule",
                                process.EventSelection,
                                process.AODSIMEventContent, #Dump AODSIM format
                                fileName=cms.untracked.string('test.root'),
                                )


#Run the output path:
process.outpath = cms.EndPath(process.output)

#Add the HLTSummaryFilter category (used in LogInfo in the HLTSummaryFilter)
process.MessageLogger.categories.append('HLTSummaryFilter')


