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
process.load('TopQuarkAnalysis.TopSkimming.topMuSkimFilterOctoberX_cff')
process.load('TopQuarkAnalysis.TopSkimming.topMuSkimValidationOctoberX_cfi')

process.options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring('ProductNotFound')
)

process.source = cms.Source("PoolSource",
                            fileNames=cms.untracked.vstring('/store/mc/Summer09/InclusiveMu15/GEN-SIM-RECO/MC_31X_V3_SD_Mu9-v1/0000/003A7526-F6AD-DE11-AA05-0018F3D096CE.root')
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
        SelectEvents = cms.vstring('p')
    )
)

process.p = cms.Path(process.topMuHLTSeq)
process.ep = cms.EndPath(process.topMuSkimValidation)

process.output=cms.OutputModule("PoolOutputModule",
                                process.EventSelection,
                                process.AODSIMEventContent, #Dump AODSIM format
                                fileName=cms.untracked.string('test.root'),
                                )

#Run the output path:
process.outpath = cms.EndPath(process.output)

#Add the HLTSummaryFilter category (used in LogInfo in the HLTSummaryFilter)
process.MessageLogger.categories.append('HLTSummaryFilter')


