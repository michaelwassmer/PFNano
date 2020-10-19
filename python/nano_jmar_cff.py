import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoMET.addPFCands_cff import addPFCands
from PhysicsTools.NanoAOD.common_cff import Var

def JMARnano_customizeMC_allPF(process):
    addPFCands(process, True)
    process.NANOAODSIMoutput.fakeNameForCrab = cms.untracked.bool(True)  # needed for crab publication
    return process

#### DATA customization
def JMARnano_customizeData_allPF(process):
    addPFCands(process, False)
    process.NANOAODSIMoutput.fakeNameForCrab = cms.untracked.bool(True)  # needed for crab publication
    return process
