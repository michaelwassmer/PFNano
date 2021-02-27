#!/usr/bin/env python
"""
This is a small script that submits a config over datasets
"""
import os

mc_samples = [
    ('/ZJetsToNuNu_HT-100To200_13TeV-madgraph/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 3),
    ('/ZJetsToNuNu_HT-200To400_13TeV-madgraph/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 5),
    ('/ZJetsToNuNu_HT-400To600_13TeV-madgraph/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 5),
    ('/ZJetsToNuNu_HT-600To800_13TeV-madgraph/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 8),
    ('/ZJetsToNuNu_HT-800To1200_13TeV-madgraph/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 10),
    ('/ZJetsToNuNu_HT-1200To2500_13TeV-madgraph/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 15),
    ('/ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 30),
    ('/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 10),
    ('/TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 10)
]

config_dir = 'crab_configs'

if not os.path.isdir( config_dir ) :
    os.mkdir(config_dir )

submit_commands = []

for path, nfiles in mc_samples:
    base_name = path.split('/')[1]

    fname = '%s/%s.py'%(config_dir, base_name)

    ofile = open(fname, 'w')

    file_entries = []

    file_entries.append('from CRABClient.UserUtilities import config')
    file_entries.append('config = config()')

    file_entries.append('')
    file_entries.append('config.section_("General")')
    file_entries.append('config.General.requestName = "production_v2_%s"' %(base_name))
    file_entries.append('config.General.workArea = "crab_projects"')
    file_entries.append('config.General.transferLogs = False')
    file_entries.append('config.General.transferOutputs = True')

    file_entries.append('')
    file_entries.append('config.section_("JobType")')
    file_entries.append('config.JobType.pluginName = "Analysis"')
    file_entries.append('config.JobType.psetName = "106X_2018_mc_NANO.py"')
    file_entries.append('config.JobType.maxMemoryMB = 4000 # Default is 2500 : Max I have used is 13000')
    file_entries.append('config.JobType.numCores = 8')
    file_entries.append('config.JobType.allowUndistributedCMSSW = True')

    file_entries.append('')
    file_entries.append('config.section_("Data")')
    file_entries.append('config.Data.inputDataset = "%s"'%path)
    file_entries.append('config.Data.splitting = "FileBased"')
    file_entries.append('config.Data.unitsPerJob = 1')
    file_entries.append('config.Data.totalUnits = %d'%nfiles)
    file_entries.append('config.Data.ignoreLocality = False')
    file_entries.append('config.Data.publication = False')
    file_entries.append('config.Data.outputDatasetTag= "NanoAOD_0125"')
    file_entries.append('config.Data.outLFNDirBase = "/store/user/yofeng/GraphMET_MoreEvents/"')

    file_entries.append('')
    file_entries.append('config.section_("Site")')
    file_entries.append('config.Site.storageSite = "T3_US_FNALLPC"')

    for line in file_entries :
        ofile.write( line + '\n' )

    ofile.close()

    submit_commands.append( 'crab submit --config %s' %( fname ) )


submit_file = open('submit_crab.sh', 'w' )
submit_file.write( '#!/bin/bash\n' )

for cmd in submit_commands :
    submit_file.write(cmd + '\n' )


submit_file.close()
os.system('chmod +x submit_crab.sh')

