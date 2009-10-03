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
process.load("TopQuarkAnalysis.TopSkimming.topMuSkimFilterOctoberX_cff")
process.load("CMS2.NtupleMaker.hltMaker_cfi")
#process.load("OctoberExercise.TopSkimValidation.topSkimValidation_cfi")

process.options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring('ProductNotFound')
)

process.source = cms.Source("PoolSource",
                            fileNames=cms.untracked.vstring('/store/mc/Summer09/Wmunu/GEN-SIM-RECO/MC_31X_V3_SD_Mu9-v2/0000/FCB993DE-86AC-DE11-88C5-002481DE4A28.root',
'/store/mc/Summer09/Wmunu/GEN-SIM-RECO/MC_31X_V3_SD_Mu9-v2/0000/FC1AF249-8EAC-DE11-A722-0025B3268576.root',	
'/store/mc/Summer09/Wmunu/GEN-SIM-RECO/MC_31X_V3_SD_Mu9-v2/0000/FADB2F4F-87AC-DE11-A31A-001E4F32F7B6.root',	
'/store/mc/Summer09/Wmunu/GEN-SIM-RECO/MC_31X_V3_SD_Mu9-v2/0000/FAC5839F-85AC-DE11-B7E8-001E4F33E1FD.root',	
'/store/mc/Summer09/Wmunu/GEN-SIM-RECO/MC_31X_V3_SD_Mu9-v2/0000/FAB06DAB-86AC-DE11-95F9-0025B3268576.root',	
'/store/mc/Summer09/Wmunu/GEN-SIM-RECO/MC_31X_V3_SD_Mu9-v2/0000/FA08484A-C4AC-DE11-91DC-0025B3268672.root',	
'/store/mc/Summer09/Wmunu/GEN-SIM-RECO/MC_31X_V3_SD_Mu9-v2/0000/F8D64CEE-86AC-DE11-AE4D-001E4F339C72.root',	
'/store/mc/Summer09/Wmunu/GEN-SIM-RECO/MC_31X_V3_SD_Mu9-v2/0000/F819FA07-82AC-DE11-A2B7-001E4F2ACF64.root')
)
# Number of events:
process.maxEvents = cms.untracked.PSet(
   input = cms.untracked.int32(-1)
   )


#To get the trigger summary at the end of the log:
process.options=cms.untracked.PSet(wantSummary=cms.untracked.bool(True))


## define event selection
process.EventSelection = cms.PSet(
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('p')
    )
)

##process.TFileService = cms.Service("TFileService", 
##      fileName = cms.string("SD_Mu9_histos.root")
##)


process.p = cms.Path(process.hlt8e29Maker*process.topMuHLTSeq)#*process.topSkimValidation)

process.output=cms.OutputModule("PoolOutputModule",
                                process.EventSelection,
                               #process.AODEventContent, #Dump AOD format
                               fileName=cms.untracked.string('TTbarSD_Mu9_HLTPtFilter.root'),
                                )


process.output.outputCommands = cms.untracked.vstring( 'drop *' )
process.output.outputCommands.extend(cms.untracked.vstring('keep *_*Maker*_*_TOPSKIM*'))



#Run the output path:
process.outpath = cms.EndPath(process.output)

#Add the HLTSummaryFilter category (used in LogInfo in the HLTSummaryFilter)
process.MessageLogger.categories.append('HLTSummaryFilter')


