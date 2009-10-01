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

process.options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring('ProductNotFound')
)

process.source = cms.Source("PoolSource",
                            fileNames=cms.untracked.vstring("/store/mc/Summer09/InclusiveMu5_Pt50/GEN-SIM-RECO/MC_31X_V3_SD_Mu9-v1/0000/729B4827-2FAA-DE11-86B1-003048678BB8.root")
#                            fileNames = cms.untracked.vstring('dcap://cmsdca3.fnal.gov:24144/pnfs/fnal.gov/usr/cms/WAX/11/store/relval/CMSSW_3_1_3/RelValProdTTbar/GEN-SIM-RECO/MC_31X_V3-v1/0003/86B57E41-F2A9-DE11-BE4D-001D09F2905B.root')
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


process.p = cms.Path(process.hlt8e29Maker*process.topMuHLTSeq)

process.output=cms.OutputModule("PoolOutputModule",
                                process.EventSelection,
                               #process.AODEventContent, #Dump AOD format
                               fileName=cms.untracked.string('TTbar_AOD_313_IDEAL_skimmed_CMS2.root'),
                                )


process.output.outputCommands = cms.untracked.vstring( 'drop *' )
process.output.outputCommands.extend(cms.untracked.vstring('keep *_*Maker*_*_TOPSKIM*'))



#Run the output path:
process.outpath = cms.EndPath(process.output)

#Add the HLTSummaryFilter category (used in LogInfo in the HLTSummaryFilter)
process.MessageLogger.categories.append('HLTSummaryFilter')


