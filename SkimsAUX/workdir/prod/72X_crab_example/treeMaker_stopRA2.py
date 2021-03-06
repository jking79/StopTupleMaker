import FWCore.ParameterSet.Config as cms

process = cms.Process("SUSY")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

## Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
      '/store/relval/CMSSW_3_8_0_pre8/RelValTTbar/GEN-SIM-RECO/START38_V6-v1/0004/847D00B0-608E-DF11-A37D-003048678FA0.root'
    )
)
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

# The following is make patJets, but EI is done with the above
process.load("PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff")
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

import os
import sys
import re

import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing ('standard')

options.register('ntpVersion', "Ntp_74X_20Jul2015_v1.1", VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "ntpVersion: to be same as the tag of the release. But can be used to produce 72X ntuple as well!")
options.register('GlobalTag', "PHYS14_25_V1", VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "74X PromptReco: 74X_dataRun2_Prompt_v0")
options.register('cmsswVersion', '72X', VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "'36X' for example. Used for specific MC fix")
options.register('specialFix', 'None', VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "special fixes ==>   JEC : use external JEC; IVF : fix IVF")
options.register('hltName', 'HLT', VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "HLT menu to use for trigger matching")

options.register('mcInfo', True, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "process MonteCarlo data, default is data")

options.register('addJetsForZinv', False, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "switch to add top projected jets for Zinv")

options.register('jetCorrections', 'L2Relative', VarParsing.VarParsing.multiplicity.list, VarParsing.VarParsing.varType.string, "Level of jet corrections to use: Note the factors are read from DB via GlobalTag")
options.jetCorrections.append('L3Absolute')

options.register('mcVersion', '', VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "'36X' for example. Used for specific MC fix")
options.register('dataVersion', '', VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "'36X' for example. Used for specific DATA fix")

options.register('jetTypes', 'AK4PF', VarParsing.VarParsing.multiplicity.list, VarParsing.VarParsing.varType.string, "Additional jet types that will be produced (AK4Calo and AK4PF, cross cleaned in PF2PAT, are included anyway)")
options.register('hltSelection', '*', VarParsing.VarParsing.multiplicity.list, VarParsing.VarParsing.varType.string, "hlTriggers (OR) used to filter events. for data: ''HLT_Mu9', 'HLT_IsoMu9', 'HLT_IsoMu13_v*''; for MC, HLT_Mu9")
options.register('addKeep', '', VarParsing.VarParsing.multiplicity.list, VarParsing.VarParsing.varType.string, "Additional keep and drop statements to trim the event content")

options.register('debug', False, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "switch on/off debug mode")

options.register('test', False, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "switch on/off debug mode")

options.register('doPtHatWeighting', False, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "PtHat weighting for QCD flat samples, default is False")

options.register('fileslist', '', VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "name of a file with input source list")

options.register('fastsim', False, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "fastsim sample or not, default is False")

options.register('doTopTagger', False, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "do top tagger or not, default is True")

options.register('usePhiCorrMET', False, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "use phi corrected MET or not, default is False")

options.register('reducedfilterTags', True, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "use phi corrected MET or not, default is True")

options.register('smsModel', 'T1tttt', VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "SMS model name")
options.register('smsMotherMass',  -1, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "SMS mother mass")
options.register('smsDaughterMass',  -1, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "SMS daughter mass")
options.register('selSMSpts', False, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "select model points")

options.register('pythia8', True, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "pythi8 or not, default True")

options.parseArguments()
options._tagOrder =[]

print options

#-- Message Logger ------------------------------------------------------------
process.MessageLogger.cerr.FwkReport.reportEvery = 100
if options.debug:
   process.MessageLogger.cerr.FwkReport.reportEvery = 1

#-- Input Source --------------------------------------------------------------
inputfiles = cms.untracked.vstring()
if options.fileslist:
   if os.path.exists(options.fileslist) == False or os.path.isfile(options.fileslist) == False:
      sys.exit(5)
   else:
      ifile = open(options.fileslist, 'r')
      for line in ifile.readlines():
         inputfiles.append(line)

print "inputfiles : \n", inputfiles, "\n"

if options.files:
   process.source.fileNames = options.files
elif options.fileslist:
   process.source.fileNames = inputfiles
else:
   process.source.fileNames = [
#       '/store/mc/RunIISpring15DR74/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v2/00000/06B5178E-F008-E511-A2CF-00261894390B.root',
#       '/store/mc/RunIISpring15DR74/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v2/00000/0836FE64-0F09-E511-9B0D-0025905B8572.root',
#       '/store/mc/RunIISpring15DR74/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v2/00000/0AF33010-F508-E511-808B-782BCB27F1F0.root',
#       '/store/mc/RunIISpring15DR74/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v2/00000/0C22259A-F008-E511-B7A9-003048FFCB84.root',
#       '/store/mc/RunIISpring15DR74/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v2/00000/108964AF-EF08-E511-8347-0025905A6080.root',
#       '/store/mc/RunIISpring15DR74/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v2/00000/129BA9CC-0009-E511-A0D7-842B2B185476.root',
#       '/store/mc/RunIISpring15DR74/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v2/00000/143F5E2F-F308-E511-9B9D-782BCB717588.root',
#       '/store/mc/Phys14DR/SMS-T1tttt_2J_mGl-1500_mLSP-100_Tune4C_13TeV-madgraph-tauola/MINIAODSIM/PU40bx25_PHYS14_25_V1-v1/00000/2281F34C-8475-E411-9E7D-00259073E450.root',
#       '/store/mc/Phys14DR/SMS-T1tttt_2J_mGl-1500_mLSP-100_Tune4C_13TeV-madgraph-tauola/MINIAODSIM/PU40bx25_PHYS14_25_V1-v1/00000/A6D4FF88-8275-E411-9259-20CF305616F4.root',
#       '/store/mc/Phys14DR/SMS-T1tttt_2J_mGl-1500_mLSP-100_Tune4C_13TeV-madgraph-tauola/MINIAODSIM/PU40bx25_PHYS14_25_V1-v1/00000/A6EFFE6A-9A75-E411-9218-002590D0B0D8.root',
#       '/store/mc/Phys14DR/SMS-T1tttt_2J_mGl-1500_mLSP-100_Tune4C_13TeV-madgraph-tauola/MINIAODSIM/PU40bx25_PHYS14_25_V1-v1/10000/E67905FE-8B75-E411-8D33-E0CB4E29C511.root', 
      '/store/mc/Phys14DR/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/MINIAODSIM/PU20bx25_PHYS14_25_V1-v1/00000/7CCE517B-0575-E411-877E-002590DB9214.root',
      '/store/mc/Phys14DR/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/MINIAODSIM/PU20bx25_PHYS14_25_V1-v1/10000/BECC9036-E875-E411-95E3-0025901D4B22.root'
   ]

process.maxEvents.input = options.maxEvents

from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag

#-- Calibration tag -----------------------------------------------------------
if options.GlobalTag:
#   process.GlobalTag.globaltag = options.GlobalTag
   process.GlobalTag = GlobalTag(process.GlobalTag, options.GlobalTag, '')

if options.mcInfo == False: options.jetCorrections.append('L2L3Residual')
options.jetCorrections.insert(0, 'L1FastJet')

#print "jetCorrections: "
#print options.jetCorrections

from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJets
from RecoJets.JetProducers.ak4GenJets_cfi import ak4GenJets
from RecoMET.METProducers.PFMET_cfi import pfMet

## --- Selection sequences ---------------------------------------------
# leptons
process.load("PhysicsTools.PatAlgos.selectionLayer1.muonCountFilter_cfi")
process.load("PhysicsTools.PatAlgos.selectionLayer1.electronCountFilter_cfi")

## Filter out neutrinos from packed GenParticles
process.packedGenParticlesForJetsNoNu = cms.EDFilter("CandPtrSelector", src = cms.InputTag("packedGenParticles"), cut = cms.string("abs(pdgId) != 12 && abs(pdgId) != 14 && abs(pdgId) != 16"))
## Define GenJets
from RecoJets.JetProducers.ak5GenJets_cfi import ak5GenJets
process.ak4GenJetsNoNu = ak4GenJets.clone(src = 'packedGenParticlesForJetsNoNu')

#do projections
process.pfCHS = cms.EDFilter("CandPtrSelector", src = cms.InputTag("packedPFCandidates"), cut = cms.string("fromPV"))

process.ak4PFJetsCHS = ak4PFJets.clone(src = 'pfCHS', doAreaFastjet = True) # no idea while doArea is false by default, but it's True in RECO so we have to set it
process.ak4GenJets = ak4GenJets.clone(src = 'packedGenParticles', rParam = 0.4)

process.pfMet = pfMet.clone(src = "packedPFCandidates")
process.pfMet.calculateSignificance = False # this can't be easily implemented on packed PF candidates at the moment

process.load("StopTupleMaker.SkimsAUX.prodMuons_cfi")
process.load("StopTupleMaker.SkimsAUX.prodElectrons_cfi")
process.pfNoMuonCHSNoMu =  cms.EDProducer("CandPtrProjector", src = cms.InputTag("pfCHS"), veto = cms.InputTag("prodMuons", "mu2Clean"))
process.ak4PFJetsCHSNoMu = ak4PFJets.clone(src = 'pfNoMuonCHSNoMu', doAreaFastjet = True) # no idea while doArea is false by default, but it's True in RECO so we have to set it


#from PhysicsTools.PatAlgos.producersLayer1.metProducer_cfi import patMETs
process.load('PhysicsTools.PatAlgos.producersLayer1.metProducer_cfi')
#from JetMETCorrections.Type1MET.pfMETCorrections_cff import *
from JetMETCorrections.Type1MET.correctionTermsPfMetType1Type2_cff import *
from PhysicsTools.PatUtils.patPFMETCorrections_cff import patPFJetMETtype1p2Corr

process.patMETs.addGenMET = cms.bool(False)

from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection

if options.cmsswVersion == "72X":
   addJetCollection(
      process,
      postfix = "",
      labelName = 'AK4PFCHS',
      jetSource = cms.InputTag('ak4PFJetsCHS'),
      pvSource = cms.InputTag('unpackedTracksAndVertices'),
      trackSource = cms.InputTag('unpackedTracksAndVertices'),
      svSource = cms.InputTag('unpackedTracksAndVertices','secondary'),
      jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'Type-2'),
      btagDiscriminators = [ 'combinedInclusiveSecondaryVertexV2BJetTags' ],
      genJetCollection = cms.InputTag('ak4GenJets'),
      algo = 'AK', rParam = 0.4
   )

   addJetCollection(
      process,
      postfix = "",
      labelName = 'AK4PFCHSNoMu',
      jetSource = cms.InputTag('ak4PFJetsCHSNoMu'),
      pvSource = cms.InputTag('unpackedTracksAndVertices'),
      trackSource = cms.InputTag('unpackedTracksAndVertices'),
      svSource = cms.InputTag('unpackedTracksAndVertices','secondary'),
      jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'Type-2'),
      btagDiscriminators = [ 'combinedInclusiveSecondaryVertexV2BJetTags' ],
      genJetCollection = cms.InputTag('ak4GenJets'),
      algo = 'AK', rParam = 0.4
   )

   #adjust MC matching
   process.patJetGenJetMatchAK4PFCHS.matched = "ak4GenJets"
   process.patJetPartonMatchAK4PFCHS.matched = "prunedGenParticles"

   process.patJetGenJetMatchAK4PFCHSNoMu.matched = "ak4GenJets"
   process.patJetPartonMatchAK4PFCHSNoMu.matched = "prunedGenParticles"

elif options.cmsswVersion == "74X":
   addJetCollection(
      process,
      postfix = "",
      labelName = 'AK4PFCHS',
      jetSource = cms.InputTag('ak4PFJetsCHS'),
      pvSource = cms.InputTag('offlineSlimmedPrimaryVertices'),
      pfCandidates = cms.InputTag('packedPFCandidates'),
      svSource = cms.InputTag('slimmedSecondaryVertices'),
      jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
      btagDiscriminators = [ 'pfCombinedInclusiveSecondaryVertexV2BJetTags' ],
      genJetCollection = cms.InputTag('ak4GenJetsNoNu'),
      genParticles = cms.InputTag('prunedGenParticles'),
      algo = 'AK', rParam = 0.4
   )
   
   addJetCollection(
      process,
      postfix = "",
      labelName = 'AK4PFCHSNoMu',
      jetSource = cms.InputTag('ak4PFJetsCHSNoMu'),
      pvSource = cms.InputTag('offlineSlimmedPrimaryVertices'),
      pfCandidates = cms.InputTag('packedPFCandidates'),
      svSource = cms.InputTag('slimmedSecondaryVertices'),
      jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
      btagDiscriminators = [ 'pfCombinedInclusiveSecondaryVertexV2BJetTags' ],
      genJetCollection = cms.InputTag('ak4GenJetsNoNu'),
      genParticles = cms.InputTag('prunedGenParticles'),
      algo = 'AK', rParam = 0.4
   )

#adjust MC matching
process.patJetPartons.particles = "prunedGenParticles"
process.patJetPartons.skipFirstN = cms.uint32(0) # do not skip first 6 particles, we already pruned some!
process.patJetPartons.acceptNoDaughters = cms.bool(True) # as we drop intermediate stuff, we need to accept quarks with no siblings

#adjust PV used for Jet Corrections
process.patJetCorrFactorsAK4PFCHS.primaryVertices = "offlineSlimmedPrimaryVertices"
process.patJetCorrFactorsAK4PFCHSNoMu.primaryVertices = "offlineSlimmedPrimaryVertices"

if options.specialFix == "JEC" and options.cmsswVersion == "74X":
   print "\nApplying fix to JEC issues in 74X ...\n"

#   inputDB = "sqlite_file:" + os.environ['CMSSW_BASE'] + "/src/StopTupleMaker/SkimsAUX/data/PY8_RunIISpring15DR74_bx25_MC.db"
#   print inputDB

   process.load("CondCore.DBCommon.CondDBCommon_cfi")
   from CondCore.DBCommon.CondDBSetup_cfi import *
   process.jec = cms.ESSource("PoolDBESSource",
      DBParameters = cms.PSet(
         messageLevel = cms.untracked.int32(0)
      ),
      timetype = cms.string('runnumber'),
      toGet = cms.VPSet(
         cms.PSet(
            record = cms.string('JetCorrectionsRecord'),
            tag    = cms.string('JetCorrectorParametersCollection_PY8_RunIISpring15DR74_bx25_MC_AK4PFchs'),
            label  = cms.untracked.string('AK4PFchs')
         ),
      ## here you add as many jet types as you need
      ## note that the tag name is specific for the particular sqlite file 
      ),
      # from page 19 on slides https://indico.cern.ch/event/405326/contribution/2/attachments/811719/1112498/Pythia8.pdf
      connect = cms.string('sqlite:PY8_RunIISpring15DR74_bx25_MC.db')
#      connect = cms.string(inputDB)
     # uncomment above tag lines and this comment to use MC JEC
   )
## add an es_prefer statement to resolve a possible conflict from simultaneous connection to a global tag
   process.es_prefer_jec = cms.ESPrefer('PoolDBESSource','jec')

   from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import patJetCorrFactorsUpdated
   process.patJetCorrFactorsReapplyJEC = patJetCorrFactorsUpdated.clone(
      src = cms.InputTag("slimmedJets"),
      levels = ['L1FastJet', 
           'L2Relative', 
           'L3Absolute'],
      payload = 'AK4PFchs' ) # Make sure to choose the appropriate levels and payload here!

   from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import patJetsUpdated
   process.patJetsReapplyJEC = patJetsUpdated.clone(
      jetSource = cms.InputTag("slimmedJets"),
      jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsReapplyJEC"))
   )
   process.fix74XJEC = cms.Sequence( process.patJetCorrFactorsReapplyJEC + process. patJetsReapplyJEC )
 
#recreate tracks and pv for btagging
process.load('PhysicsTools.PatAlgos.slimming.unpackedTracksAndVertices_cfi')

process.MessageLogger.suppressWarning = cms.untracked.vstring('ecalLaserCorrFilter','manystripclus53X','toomanystripclus53X')
process.options.allowUnscheduled = cms.untracked.bool(True)

#Analysis related configuration
import HLTrigger.HLTfilters.hltHighLevel_cfi as hlt
if options.hltSelection:
   process.hltFilter = hlt.hltHighLevel.clone(
      TriggerResultsTag = cms.InputTag("TriggerResults","",options.hltName),
      HLTPaths = cms.vstring(options.hltSelection),
      throw = True, # Don't throw?!
      andOr = True
   )

process.load("RecoJets.Configuration.GenJetParticles_cff")
process.genParticlesForJets.src = cms.InputTag("prunedGenParticles")

process.load("StopTupleMaker.SkimsAUX.simpleJetSelector_cfi")
process.selectedPatJetsRA2 = process.simpleJetSelector.clone()

process.load("PhysicsTools.PatAlgos.selectionLayer1.jetCountFilter_cfi")
# PFJets (with CHS)
process.ak4patJetsPFchsPt10     = process.selectedPatJetsRA2.clone()
process.ak4patJetsPFchsPt10.jetSrc = cms.InputTag('slimmedJets')
process.ak4patJetsPFchsPt10.pfJetCut = cms.string('pt > 10')

process.ak4patJetsPFchsPt30     = process.selectedPatJetsRA2.clone()
process.ak4patJetsPFchsPt30.jetSrc = cms.InputTag('slimmedJets')
process.ak4patJetsPFchsPt30.pfJetCut = cms.string('pt > 30')

process.ak4patJetsPFchsPt50Eta25     = process.selectedPatJetsRA2.clone()
process.ak4patJetsPFchsPt50Eta25.jetSrc = cms.InputTag('slimmedJets')
process.ak4patJetsPFchsPt50Eta25.pfJetCut = cms.string('pt > 50 & abs(eta) < 2.5')

process.patJetsAK4PFCHSPt10 = process.selectedPatJetsRA2.clone()
process.patJetsAK4PFCHSPt10.jetSrc = cms.InputTag("patJetsAK4PFCHS")
process.patJetsAK4PFCHSPt10.pfJetCut = cms.string('pt >= 10')

process.patJetsAK4PFCHSPt10NoMu = process.selectedPatJetsRA2.clone()
process.patJetsAK4PFCHSPt10NoMu.jetSrc = cms.InputTag("patJetsAK4PFCHSNoMu")
process.patJetsAK4PFCHSPt10NoMu.pfJetCut = cms.string('pt >= 10')

# PFJets - filters
process.countak4JetsPFchsPt50Eta25           = process.countPatJets.clone()
process.countak4JetsPFchsPt50Eta25.src       = cms.InputTag('ak4patJetsPFchsPt50Eta25')
process.countak4JetsPFchsPt50Eta25.minNumber = cms.uint32(3)

process.ra2PFchsJets = cms.Sequence( process.ak4patJetsPFchsPt10 * process.ak4patJetsPFchsPt30 * process.ak4patJetsPFchsPt50Eta25 )

# HT 
process.load("StopTupleMaker.Skims.htProducer_cfi")
process.load("StopTupleMaker.Skims.htFilter_cfi")
process.htPFchs = process.ht.clone()
process.htPFchs.JetCollection = cms.InputTag("ak4patJetsPFchsPt50Eta25")

process.htPFchsFilter = process.htFilter.clone()
process.htPFchsFilter.HTSource = cms.InputTag("htPFchs")

# MHT
process.load("StopTupleMaker.Skims.mhtProducer_cfi")
process.load("StopTupleMaker.Skims.mhtFilter_cfi")
process.mhtPFchs = process.mht.clone()
process.mhtPFchs.JetCollection = cms.InputTag("ak4patJetsPFchsPt30")

process.mhtPFchsFilter = process.mhtFilter.clone()
process.mhtPFchsFilter.MHTSource = cms.InputTag("mhtPFchs")

# Delta Phi
process.load("StopTupleMaker.Skims.jetMHTDPhiFilter_cfi")

process.ak4jetMHTPFchsDPhiFilter = process.jetMHTDPhiFilter.clone()
process.ak4jetMHTPFchsDPhiFilter.JetSource = cms.InputTag("ak4patJetsPFchsPt30")
process.ak4jetMHTPFchsDPhiFilter.MHTSource = cms.InputTag("mhtPFchs")

process.ra2Objects = cms.Sequence( 
                                   process.ra2PFchsJets *
                                   process.htPFchs *
                                   process.mhtPFchs
                                 )

process.load("PhysicsTools.PatAlgos.selectionLayer1.muonCountFilter_cfi")
process.load("PhysicsTools.PatAlgos.selectionLayer1.electronCountFilter_cfi")

############################# START SUSYPAT specifics ####################################
process.prefilterCounter        = cms.EDProducer("EventCountProducer")
process.postStdCleaningCounter  = cms.EDProducer("EventCountProducer")

# Standard Event cleaning 
process.load("StopTupleMaker.SkimsAUX.prodFilterOutScraping_cfi")
process.load("StopTupleMaker.SkimsAUX.prodGoodVertices_cfi")
#process.load("StopTupleMaker.Skims.noscraping_cfi")
#process.load("StopTupleMaker.Skims.vertex_cfi")

# The goodVertices is now moved in the prodGoodVertices_cfi for consistent maintainance!
#process.goodVertices = cms.EDFilter(
#  "VertexSelector",
#  filter = cms.bool(False),
#  src = cms.InputTag("offlineSlimmedPrimaryVertices"),
#  cut = cms.string("!isFake && ndof > 4 && abs(z) <= 24 && position.rho < 2")
#)

#process.ra2StdCleaning = cms.Sequence(
#                 process.noscraping *
#                 process.oneGoodVertex
#)

# an example sequence to create skimmed susypat-tuples
process.cleanpatseq = cms.Sequence(
#                      process.ra2StdCleaning          *
                      process.postStdCleaningCounter  #*
                      )
############################# EDN SUSYPAT specifics ####################################

process.dummyCounter = cms.EDProducer("EventCountProducer")

process.load('StopTupleMaker.SkimsAUX.prodJetIDEventFilter_cfi')
process.prodJetIDEventFilter.JetSource = cms.InputTag("slimmedJets")
process.prodJetIDEventFilter.MinJetPt  = cms.double(30.0)
process.prodJetIDEventFilter.MaxJetEta = cms.double(999.0)
# Adjust jets due to JEC in prodJetIDEventFilter filter
#if options.mcInfo == True:
#   process.prodJetIDEventFilter.JECLevel = cms.untracked.string('ak4PFJetsL1FastL2L3')
#else:
#   process.prodJetIDEventFilter.JECLevel = cms.untracked.string('ak4PFJetsL1FastL2L3Residual')
# End of the adjusting in the prodJetIDEventFilter filter

process.load('StopTupleMaker.SkimsAUX.weightProducer_cfi')
process.weightProducer.inputPUfileMC   = cms.untracked.string("")
process.weightProducer.inputPUfileData = cms.untracked.string("")
if options.doPtHatWeighting:
   process.weightProducer.Method     = cms.string("PtHat")
   process.weightProducer.Exponent   = cms.double(-4.5)
   process.weightProducer.XS         = cms.double(1.0)
   process.weightProducer.NumberEvts = cms.double(1.0)
   process.weightProducer.Lumi       = cms.double(1.0)
   process.weightProducer.weightWARNingUpThreshold  = cms.double(2.0)

from JetMETCorrections.Configuration.DefaultJEC_cff import *
process.ak4PFJetschsL1FastL2L3Residual = ak4PFJetsL1FastL2L3Residual.clone( algorithm = cms.string('AK4PFchs'), src = 'slimmedJets' )
process.ak4PFJetschsL1FastL2L3 = ak4PFJetsL1FastL2L3.clone( algorithm = cms.string('AK4PFchs'), src = 'slimmedJets' )

# Default is dR = 0.3, dz < 0.05, pt > 10, reliso < 0.1
process.load("StopTupleMaker.Skims.trackIsolationMaker_cfi")
process.trackIsolation = process.trackIsolationFilter.clone()
process.trackIsolation.pfCandidatesTag = cms.InputTag("packedPFCandidates")
process.trackIsolation.doTrkIsoVeto = cms.bool(False)

process.loosetrackIsolation = process.trackIsolation.clone()
process.loosetrackIsolation.minPt_PFCandidate = cms.double(5.0)
process.loosetrackIsolation.isoCut            = cms.double(0.5)

process.load('StopTupleMaker.Skims.StopJets_drt_from_AOD_cff')

process.load("StopTupleMaker.SkimsAUX.nJetsForSkimsRA2_cfi")
process.load("StopTupleMaker.SkimsAUX.jetMHTDPhiForSkimsRA2_cfi")

# ak4 jets
process.ak4stopJetsPFchsPt30 = process.stopJetsPFchsPt30.clone(jetSrc = "slimmedJets")
process.ak4stopJetsPFchsPt50Eta24 = process.stopJetsPFchsPt50Eta24.clone(jetSrc = "slimmedJets")

process.ak4nJetsForSkimsStop = process.nJetsForSkimsRA2.clone()
process.ak4nJetsForSkimsStop.JetSource = cms.InputTag("ak4stopJetsPFchsPt30")
process.ak4jetMHTDPhiForSkimsStop = process.jetMHTDPhiForSkimsRA2.clone()
process.ak4jetMHTDPhiForSkimsStop.MHTSource = cms.InputTag("slimmedMETs")
process.ak4jetMHTDPhiForSkimsStop.JetSource = cms.InputTag("ak4stopJetsPFchsPt30")

process.ak4stophtPFchs = process.htPFchs.clone()
process.ak4stophtPFchs.JetCollection = cms.InputTag("ak4stopJetsPFchsPt50Eta24")

process.ak4stopmhtPFchs = process.mhtPFchs.clone()
process.ak4stopmhtPFchs.JetCollection = cms.InputTag("ak4stopJetsPFchsPt30")
#

process.prepareCutvars_seq = cms.Sequence( process.ak4stopJetsPFchsPt30 * process.ak4stopJetsPFchsPt50Eta24 * process.ak4nJetsForSkimsStop * process.ak4jetMHTDPhiForSkimsStop * process.ak4stophtPFchs * process.ak4stopmhtPFchs )

process.load("StopTupleMaker.Skims.StopBTagJets_cff")
process.stopBJets.JetSrc = cms.InputTag("stopJetsPFchsPt30")

# Other sequence
process.comb_seq = cms.Sequence(
# All cleaning && all basic variables, e.g., mht, ht...     
   process.cleanpatseq *
# hlt requirement
   process.hltFilter *
   process.prodMuons * process.prodElectrons * 
   process.weightProducer *
   process.trackIsolation * process.loosetrackIsolation *
   process.stopPFJets * process.stopBJets *
   process.ra2Objects *
   process.prepareCutvars_seq
)

process.load("StopTupleMaker.Skims.StopDPhiSelection_cff")
process.jetsMETDPhiFilter.jetSrc = cms.InputTag("stopJetsPFchsPt30")
if options.usePhiCorrMET == True:
   process.jetsMETDPhiFilter.metSrc = cms.InputTag("slimmedMETs")
else:
   process.jetsMETDPhiFilter.metSrc = cms.InputTag("slimmedMETs")
process.jetsMETDPhiFilter.dPhiCuts = cms.untracked.vdouble(0.5, 0.5, 0.3)

process.stopCount1BJets = process.stopCountBJets.clone()
process.stopCount1BJets.minNumber = cms.uint32(1)

process.stopCount2BJets = process.stopCountBJets.clone()
process.stopCount2BJets.minNumber = cms.uint32(2)

process.load("StopTupleMaker.Skims.StopType3TopTagger_cff")
if options.usePhiCorrMET == True:
   process.type3topTagger.metSrc = cms.InputTag("slimmedMETs")
else:
   process.type3topTagger.metSrc = cms.InputTag("slimmedMETs")
process.type3topTagger.taggingMode = cms.untracked.bool(True)
process.type3topTagger.jetSrc = cms.InputTag("stopJetsPFchsPt30")

process.metPFchsFilter = process.mhtPFchsFilter.clone()
if options.usePhiCorrMET == True:
   process.metPFchsFilter.MHTSource = cms.InputTag("slimmedMETs")
else:
   process.metPFchsFilter.MHTSource = cms.InputTag("slimmedMETs")

process.met175PFchsFilter = process.metPFchsFilter.clone()
process.met175PFchsFilter.MinMHT = cms.double(175)

process.met200PFchsFilter = process.metPFchsFilter.clone()
process.met200PFchsFilter.MinMHT = cms.double(200)

process.met350PFchsFilter = process.metPFchsFilter.clone()
process.met350PFchsFilter.MinMHT = cms.double(350)

process.TFileService = cms.Service("TFileService",
   fileName = cms.string('stopFlatNtuples.root')
)

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

process.load("StopTupleMaker.SignalScan.genDecayStringMaker_cfi")
process.printDecay.src = cms.InputTag("prunedGenParticles")
process.printDecay.keyDecayStrs = cms.vstring("t", "tbar", "~chi_1+", "~chi_1-")
process.printDecay.printDecay = cms.untracked.bool(options.debug)

process.load("StopTupleMaker.SignalScan.genDecayStringMakerPythia8_cfi")
process.printDecayPythia8.src = cms.InputTag("prunedGenParticles")
process.printDecayPythia8.keyDecayStrs = cms.vstring("t", "tbar", "~chi_1+", "~chi_1-")
process.printDecayPythia8.printDecay = cms.untracked.bool(options.debug)

process.load("StopTupleMaker.SignalScan.smsModelFilter_cfi")
process.smsModelFilter.SusyScanTopology   = cms.string(options.smsModel)
process.smsModelFilter.SusyScanMotherMass = cms.double(options.smsMotherMass)
process.smsModelFilter.SusyScanLSPMass    = cms.double(options.smsDaughterMass)
process.smsModelFilter.SusyScanFracLSP    = cms.double(0.0)
process.smsModelFilter.Debug              = cms.bool(options.debug)

process.load("StopTupleMaker.TopTagger.groomProd_cfi")
process.groomProdak4 = process.groomProd.clone()
process.groomProdak4.jetSrc = cms.InputTag("ak4patJetsPFchsPt10")
process.groomProdak4.groomingOpt = cms.untracked.int32(1)
#process.groomProdak4.debug = cms.untracked.bool(options.debug)

process.load("StopTupleMaker.SkimsAUX.prodJets_cfi")
process.load("StopTupleMaker.SkimsAUX.prodMET_cfi")
process.load("StopTupleMaker.SkimsAUX.prodGenInfo_cfi")
process.load("StopTupleMaker.SkimsAUX.prodIsoTrks_cfi")
process.load("StopTupleMaker.SkimsAUX.prodEventInfo_cfi")

#Addition of Filter Decision Bits and Trigger Results
process.load("StopTupleMaker.SkimsAUX.prodTriggerResults_cfi")
process.load("StopTupleMaker.SkimsAUX.prodFilterFlags_cfi")

process.triggerProducer.trigTagSrc = cms.InputTag("TriggerResults","",options.hltName)

process.METFilters = process.filterDecisionProducer.clone( filterName  =   cms.string("Flag_METFilters") )
process.CSCTightHaloFilter = process.filterDecisionProducer.clone( filterName  =   cms.string("Flag_CSCTightHaloFilter") )
process.HBHENoiseFilter = process.filterDecisionProducer.clone( filterName  =   cms.string("Flag_HBHENoiseFilter") )
process.EcalDeadCellTriggerPrimitiveFilter = process.filterDecisionProducer.clone( filterName  =   cms.string("Flag_EcalDeadCellTriggerPrimitiveFilter") )

if options.cmsswVersion == "72X":
   process.prodJets.bTagKeyString = cms.string('combinedInclusiveSecondaryVertexV2BJetTags')
else:
   process.prodJets.bTagKeyString = cms.string('pfCombinedInclusiveSecondaryVertexV2BJetTags')

process.prodJets.jetOtherSrc = cms.InputTag('patJetsAK4PFCHS')

process.prodJetsNoMu = process.prodJets.clone()
process.prodJetsNoMu.jetSrc = cms.InputTag('patJetsAK4PFCHSPt10NoMu')
process.prodJetsNoMu.jetOtherSrc = cms.InputTag('patJetsAK4PFCHSPt10NoMu')

process.prodMuonsNoIso = process.prodMuons.clone()
process.prodMuonsNoIso.DoMuonIsolation = cms.bool(False)

process.prodElectronsNoIso = process.prodElectrons.clone()
process.prodElectronsNoIso.DoElectronIsolation = cms.bool(False)

process.load("StopTupleMaker.StopTreeMaker.stopTreeMaker_cfi")
process.stopTreeMaker.debug = cms.bool(options.debug)
process.stopTreeMaker.TreeName = cms.string("AUX")

process.ntpVersion = cms.EDFilter(
   "prodNtupleVersionString", 
   inputStr = cms.vstring(options.ntpVersion, options.GlobalTag, options.cmsswVersion, options.specialFix, options.hltName)
)

process.stopTreeMaker.vectorString.append(cms.InputTag("ntpVersion"))

process.stopTreeMaker.vectorInt.append(cms.InputTag("triggerProducer", "PassTrigger"))
process.stopTreeMaker.vectorString.append(cms.InputTag("triggerProducer", "TriggerNames"))

# prodGoodVertices has the same as vtxSize in prodEventInfo...
#process.stopTreeMaker.varsInt.append(cms.InputTag("prodGoodVertices"))
#process.stopTreeMaker.varsInt.append(cms.InputTag("prodFilterOutScraping"))
process.stopTreeMaker.varsInt.append(cms.InputTag("prodJetIDEventFilter"))
process.stopTreeMaker.varsInt.append(cms.InputTag("METFilters"))
process.stopTreeMaker.varsInt.append(cms.InputTag("CSCTightHaloFilter"))
process.stopTreeMaker.varsInt.append(cms.InputTag("HBHENoiseFilter"))
process.stopTreeMaker.varsInt.append(cms.InputTag("EcalDeadCellTriggerPrimitiveFilter"))

process.stopTreeMaker.varsInt.append(cms.InputTag("prodMuons", "nMuons"))
process.stopTreeMaker.varsIntNamesInTree.append("prodMuons:nMuons|nMuons_CUT")
process.stopTreeMaker.varsInt.append(cms.InputTag("prodMuonsNoIso", "nMuons"))
process.stopTreeMaker.vectorTLorentzVector.append(cms.InputTag("prodMuonsNoIso", "muonsLVec"))
process.stopTreeMaker.vectorDouble.extend([cms.InputTag("prodMuonsNoIso", "muonsCharge"), cms.InputTag("prodMuonsNoIso", "muonsMtw"), cms.InputTag("prodMuonsNoIso", "muonsRelIso"), cms.InputTag("prodMuonsNoIso", "muonsMiniIso")])

process.stopTreeMaker.varsInt.append(cms.InputTag("prodElectrons", "nElectrons"))
process.stopTreeMaker.varsIntNamesInTree.append("prodElectrons:nElectrons|nElectrons_CUT")
process.stopTreeMaker.varsInt.append(cms.InputTag("prodElectronsNoIso", "nElectrons"))
process.stopTreeMaker.vectorTLorentzVector.append(cms.InputTag("prodElectronsNoIso", "elesLVec"))
process.stopTreeMaker.vectorDouble.extend([cms.InputTag("prodElectronsNoIso", "elesCharge"), cms.InputTag("prodElectronsNoIso", "elesMtw"), cms.InputTag("prodElectronsNoIso", "elesRelIso"), cms.InputTag("prodElectronsNoIso", "elesMiniIso")])
process.stopTreeMaker.vectorBool.extend([cms.InputTag("prodElectronsNoIso", "elesisEB")])

process.stopTreeMaker.varsInt.append(cms.InputTag("prodJets", "nJets"))
process.stopTreeMaker.vectorTLorentzVector.append(cms.InputTag("prodJets", "jetsLVec"))
process.stopTreeMaker.vectorInt.append(cms.InputTag("prodJets", "recoJetsFlavor"))

process.stopTreeMaker.vectorDouble.append(cms.InputTag("prodJets", "recoJetschargedHadronEnergyFraction"))
process.stopTreeMaker.vectorDouble.append(cms.InputTag("prodJets", "recoJetschargedEmEnergyFraction"))
process.stopTreeMaker.vectorDouble.append(cms.InputTag("prodJets", "recoJetsneutralEmEnergyFraction"))

process.stopTreeMaker.vectorDouble.append(cms.InputTag("prodJets", "recoJetsBtag"))
process.stopTreeMaker.vectorDoubleNamesInTree.append("prodJets:recoJetsBtag|recoJetsBtag_0")

process.stopTreeMaker.vectorInt.append(cms.InputTag("prodJets", "muMatchedJetIdx"))
process.stopTreeMaker.vectorInt.append(cms.InputTag("prodJets", "eleMatchedJetIdx"))

if options.addJetsForZinv == True: 
   process.stopTreeMaker.vectorTLorentzVector.append(cms.InputTag("prodJetsNoMu", "jetsLVec"))
   process.stopTreeMaker.varsTLorentzVectorNamesInTree.append("prodJetsNoMu:jetsLVec|jetsLVecMuCleaned")
   process.stopTreeMaker.vectorDouble.append(cms.InputTag("prodJetsNoMu", "recoJetschargedHadronEnergyFraction"))
   process.stopTreeMaker.varsDoubleNamesInTree.append("prodJetsNoMu:recoJetschargedHadronEnergyFraction|recoJetschargedHadronEnergyFractionMuCleaned")
   process.stopTreeMaker.vectorDouble.append(cms.InputTag("prodJetsNoMu", "recoJetsneutralEmEnergyFraction"))
   process.stopTreeMaker.varsDoubleNamesInTree.append("prodJetsNoMu:recoJetsneutralEmEnergyFraction|recoJetsneutralEmEnergyFractionMuCleaned")
   process.stopTreeMaker.vectorDouble.append(cms.InputTag("prodJetsNoMu", "recoJetschargedEmEnergyFraction"))
   process.stopTreeMaker.varsDoubleNamesInTree.append("prodJetsNoMu:recoJetschargedEmEnergyFraction|recoJetschargedEmEnergyFractionMuCleaned")
   process.stopTreeMaker.vectorDouble.append(cms.InputTag("prodJetsNoMu", "recoJetsBtag"))
   process.stopTreeMaker.varsDoubleNamesInTree.append("prodJetsNoMu:recoJetsBtag|recoJetsBtag_0_MuCleaned")

if options.mcInfo == True:
   process.prodGenInfo.debug = cms.bool(options.debug)
   process.stopTreeMaker.vectorString.append(cms.InputTag("prodGenInfo", "genDecayStrVec"))
   process.stopTreeMaker.vectorInt.extend([cms.InputTag("prodGenInfo", "genDecayIdxVec"), cms.InputTag("prodGenInfo", "genDecayPdgIdVec"), cms.InputTag("prodGenInfo", "genDecayMomIdxVec"), cms.InputTag("prodGenInfo", "genDecayMomRefVec"), cms.InputTag("prodGenInfo", "WemuVec"), cms.InputTag("prodGenInfo", "WtauVec"), cms.InputTag("prodGenInfo", "WtauemuVec"), cms.InputTag("prodGenInfo", "WtauprongsVec"), cms.InputTag("prodGenInfo", "WtaunuVec")])
   process.stopTreeMaker.vectorIntNamesInTree.extend(["prodGenInfo:WemuVec|W_emuVec", "prodGenInfo:WtauVec|W_tauVec", "prodGenInfo:WtauemuVec|W_tau_emuVec", "prodGenInfo:WtauprongsVec|W_tau_prongsVec", "prodGenInfo:WtaunuVec|W_tau_nuVec"])
   process.stopTreeMaker.vectorTLorentzVector.append(cms.InputTag("prodGenInfo", "genDecayLVec"))

process.stopTreeMaker.vectorTLorentzVector.append(cms.InputTag("prodIsoTrks:trksForIsoVetoLVec"))
process.stopTreeMaker.vectorDouble.extend([cms.InputTag("prodIsoTrks:trksForIsoVetocharge"), cms.InputTag("prodIsoTrks:trksForIsoVetodz"), cms.InputTag("prodIsoTrks:looseisoTrkscharge"), cms.InputTag("prodIsoTrks:looseisoTrksdz"), cms.InputTag("prodIsoTrks:looseisoTrksiso"), cms.InputTag("prodIsoTrks:looseisoTrksmtw")])
process.stopTreeMaker.vectorDoubleNamesInTree.extend(["prodIsoTrks:trksForIsoVetocharge|trksForIsoVeto_charge", "prodIsoTrks:trksForIsoVetodz|trksForIsoVeto_dz", "prodIsoTrks:looseisoTrkscharge|loose_isoTrks_charge", "prodIsoTrks:looseisoTrksdz|loose_isoTrks_dz", "prodIsoTrks:looseisoTrksiso|loose_isoTrks_iso", "prodIsoTrks:looseisoTrksmtw|loose_isoTrks_mtw"])
process.stopTreeMaker.vectorInt.extend([cms.InputTag("prodIsoTrks:trksForIsoVetopdgId"), cms.InputTag("prodIsoTrks:trksForIsoVetoidx"), cms.InputTag("prodIsoTrks:looseisoTrkspdgId"), cms.InputTag("prodIsoTrks:looseisoTrksidx"), cms.InputTag("prodIsoTrks:forVetoIsoTrksidx")])
process.stopTreeMaker.vectorIntNamesInTree.extend(["prodIsoTrks:trksForIsoVetopdgId|trksForIsoVeto_pdgId", "prodIsoTrks:trksForIsoVetoidx|trksForIsoVeto_idx", "prodIsoTrks:looseisoTrkspdgId|loose_isoTrks_pdgId", "prodIsoTrks:looseisoTrksidx|loose_isoTrks_idx"])
process.stopTreeMaker.vectorTLorentzVector.append(cms.InputTag("prodIsoTrks:looseisoTrksLVec"))
process.stopTreeMaker.vectorTLorentzVectorNamesInTree.append("prodIsoTrks:looseisoTrksLVec|loose_isoTrksLVec")
process.stopTreeMaker.varsInt.extend([cms.InputTag("prodIsoTrks:loosenIsoTrks"), cms.InputTag("prodIsoTrks:nIsoTrksForVeto")])
process.stopTreeMaker.varsIntNamesInTree.extend(["prodIsoTrks:loosenIsoTrks|loose_nIsoTrks", "prodIsoTrks:nIsoTrksForVeto|nIsoTrks_CUT"])

process.stopTreeMaker.varsDouble.extend([cms.InputTag("ak4stopmhtPFchs:mht"), cms.InputTag("ak4stopmhtPFchs:mhtphi")])

process.stopTreeMaker.varsDouble.append(cms.InputTag("ak4stophtPFchs"))
process.stopTreeMaker.varsDoubleNamesInTree.append("ak4stophtPFchs|ht")

process.stopTreeMaker.varsInt.append(cms.InputTag("ak4nJetsForSkimsStop:nJets"))
process.stopTreeMaker.varsIntNamesInTree.append("ak4nJetsForSkimsStop:nJets|nJets_CUT")

process.stopTreeMaker.varsDouble.extend([cms.InputTag("prodMET:met"), cms.InputTag("prodMET:metphi")])

process.stopTreeMaker.varsDouble.extend([cms.InputTag("ak4jetMHTDPhiForSkimsStop:dPhi0"), cms.InputTag("ak4jetMHTDPhiForSkimsStop:dPhi1"), cms.InputTag("ak4jetMHTDPhiForSkimsStop:dPhi2")])
process.stopTreeMaker.varsDoubleNamesInTree.extend(["ak4jetMHTDPhiForSkimsStop:dPhi0|dPhi0_CUT", "ak4jetMHTDPhiForSkimsStop:dPhi1|dPhi1_CUT", "ak4jetMHTDPhiForSkimsStop:dPhi2|dPhi2_CUT"])

process.stopTreeMaker.varsInt.extend([cms.InputTag("prodEventInfo:vtxSize"), cms.InputTag("prodEventInfo:npv"), cms.InputTag("prodEventInfo:nm1"), cms.InputTag("prodEventInfo:n0"), cms.InputTag("prodEventInfo:np1")])
process.stopTreeMaker.varsDouble.extend([cms.InputTag("prodEventInfo:trunpv"), cms.InputTag("prodEventInfo:avgnpv"), cms.InputTag("prodEventInfo:storedWeight")])
process.stopTreeMaker.varsDoubleNamesInTree.extend(["prodEventInfo:trunpv|tru_npv", "prodEventInfo:avgnpv|avg_npv", "prodEventInfo:storedWeight|stored_weight"])

if options.doTopTagger == True:
   process.stopTreeMaker.varsInt.extend([cms.InputTag("type3topTagger:bestTopJetIdx"), cms.InputTag("type3topTagger:pickedRemainingCombfatJetIdx")])
   process.stopTreeMaker.varsDouble.extend([cms.InputTag("type3topTagger:bestTopJetMass"), cms.InputTag("type3topTagger:MT2"), cms.InputTag("type3topTagger:mTbestTopJet"), cms.InputTag("type3topTagger:mTbJet"), cms.InputTag("type3topTagger:linearCombmTbJetPlusmTbestTopJet"), cms.InputTag("type3topTagger:mTbestWJet"), cms.InputTag("type3topTagger:mTbestbJet"), cms.InputTag("type3topTagger:mTremainingTopJet")])
   process.stopTreeMaker.varsBool.append(cms.InputTag("type3topTagger:remainPassCSVS"))

process.stopTreeMaker.varsDouble.append(cms.InputTag("weightProducer:weight"))
process.stopTreeMaker.varsDoubleNamesInTree.append("weightProducer:weight|evtWeight")

process.trig_filter_seq = cms.Sequence( process.triggerProducer * process.METFilters * process.CSCTightHaloFilter * process.HBHENoiseFilter * process.EcalDeadCellTriggerPrimitiveFilter )

if options.selSMSpts == True:
   process.stopTreeMaker.vectorString.extend([cms.InputTag("smsModelFilter:fileNameStr"), cms.InputTag("smsModelFilter:smsModelStr")])
   process.stopTreeMaker.varsDouble.extend([cms.InputTag("smsModelFilter:smsMotherMass"), cms.InputTag("smsModelFilter:smsDaughterMass")])

process.ak4Stop_Path = cms.Path(
                                   process.comb_seq * 
                                   process.printDecayPythia8 * process.prodGenInfo * 
                                   process.prodMuonsNoIso * process.prodElectronsNoIso *  
                                   process.prodJets * process.prodMET * process.prodIsoTrks * process.prodEventInfo * process.trig_filter_seq * 
                                   process.type3topTagger *
                                   process.stopTreeMaker
)

if options.doTopTagger == False:
   process.ak4Stop_Path.remove(process.type3topTagger)

if options.mcInfo == False:
   process.ak4Stop_Path.remove(process.prodGenInfo)
   process.ak4Stop_Path.remove(process.printDecayPythia8)

if options.selSMSpts == True:
   process.ak4Stop_Path.replace(process.hltFilter, process.hltFilter*process.smsModelFilter)

if options.specialFix == "JEC" and options.cmsswVersion == "74X":
   process.comb_seq.replace(process.weightProducer, process.fix74XJEC*process.weightProducer)

   process.patJetsReapplyJECPt10 = process.selectedPatJetsRA2.clone()
   process.patJetsReapplyJECPt10.jetSrc = cms.InputTag("patJetsReapplyJEC")
   process.patJetsReapplyJECPt10.pfJetCut = cms.string('pt >= 10')

   process.prodJets.jetSrc = cms.InputTag('patJetsReapplyJECPt10')

   process.ak4patJetsPFchsPt10.jetSrc = cms.InputTag('patJetsReapplyJEC')
   process.ak4patJetsPFchsPt30.jetSrc = cms.InputTag('patJetsReapplyJEC')
   process.ak4patJetsPFchsPt50Eta25.jetSrc = cms.InputTag('patJetsReapplyJEC')
   process.prodJetIDEventFilter.JetSource = cms.InputTag("patJetsReapplyJEC")
   process.ak4stopJetsPFchsPt30.jetSrc = cms.InputTag("patJetsReapplyJEC")
   process.ak4stopJetsPFchsPt50Eta24.jetSrc = cms.InputTag("patJetsReapplyJEC")

###-- Dump config ------------------------------------------------------------
if options.debug:
   file = open('allDump_cfg.py','w')
   file.write(str(process.dumpPython()))
   file.close()
