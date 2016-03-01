




# Python script to merge root files together

import sys
import os
from ROOT import *

# ==== Choose a task ====
clean = False
#clean = True

merge = False
merge = True

# ======================


if merge:

    target_file = 'root://eoscms.cern.ch//eos/cms/store/user/dcurry/EMTF/rate_v7/zeroBias_merge_v7.root'

    source_dir = '/store/user/dcurry/EMTF/rate_v7/ZeroBias1/crab_20160301_112136/160301_102212/0000/'

    os.system('rm hadd')
 
    print '----> Printing file names/paths to hadd...'
    
    temp_string = "cmsLs "+source_dir+" | grep root >> hadd"

    os.system(temp_string)
    #os.system("cmsLs /store/user/dcurry/EMTF/rate_v6/ZeroBias1/crab_20160301_105807/160301_095832/0000/ | grep root | awk '{print ""$5""}' >> hadd")

    input_file = ''
    with open('hadd') as file:
    
        for i, line in enumerate(file):
            
            if i is 20: break
            
            line = 'root://eoscms.cern.ch//eos/cms' + source_dir + line 
            
            x = line.replace('\n', ' ') 
            
            input_file += x

    merge = "hadd -f %s %s" % (target_file, input_file) 
    
    print '----> Merging Files into', target_file,'.  This may take a while....'

    os.system(merge)



# ====== For cleaning EOS ========
if clean: 

    print '----> Cleaning EOS Files...'
    
    os.system('rm clean')

    # make a list of files to be removed
    clean_dir = '/store/user/dcurry/rpc/2012D_MinBias_Raw_Reco_1_11_15/MinimumBias/crab_20150113_223829/150113_213900/0000/'
    os.system("cmsLs "+clean_dir+" | grep root | awk '{print ""$5""}' >> clean")
    
    with open('clean') as file:

        for i, line in enumerate(file):
            
            temp = 'cmsRm %s' % (line)
            
            print temp
            os.system(temp)


    print '----> Cleaning Finished.'
