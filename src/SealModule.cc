//includes
#include "PluginManager/ModuleDef.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/EgammaCandidates/interface/PixelMatchGsfElectron.h"
#include "PhysicsTools/UtilAlgos/interface/ObjectCountFilter.h"
#include "PhysicsTools/UtilAlgos/interface/PtMinSelector.h"
#include "TopQuarkAnalysis/TopSkimming/interface/TopDiLeptonFilter.h"
#include "TopQuarkAnalysis/TopSkimming/interface/JetTagCountFilter.h"
#include "TopQuarkAnalysis/TopSkimming/interface/TopDecayChannelFilter.h"
#include "TopQuarkAnalysis/TopSkimming/interface/TtDecayChannelSelector.h"

typedef TopDecayChannelFilter<TtDecayChannelSelector>
                              TtDecayChannelFilter;

typedef ObjectCountFilter<
          reco::PixelMatchGsfElectronCollection,
          PtMinSelector<reco::PixelMatchGsfElectron>
        > PtMinPixelMatchGsfElectronCountFilter;

//macros
// define seal modules
DEFINE_SEAL_MODULE();
// define each module separately
DEFINE_ANOTHER_FWK_MODULE(JetTagCountFilter);
DEFINE_ANOTHER_FWK_MODULE(PtMinPixelMatchGsfElectronCountFilter);
DEFINE_ANOTHER_FWK_MODULE(TopDiLeptonFilter);
DEFINE_ANOTHER_FWK_MODULE(TtDecayChannelFilter);

