# This codes is for extracting ADR entries/ mentions from trainning corpus texts of TAC2017 task (https://bionlp.nlm.nih.gov/tac2017adversereactions/)
# Author: Kaiyin Zhou, Yingying Jiang
# Email to me: zhoukaiyinhzau@gmail.com 
# College of Informatics, Huazhong Agricultural University. Hubei province, China. P. R.
#############################################################################################
#################    Run our codes step by step                 #############################
#################    Please also find direction in codes lines  #############################
#################         2017/10/9/                            #############################
#############################################################################################



# Python enviroment requirement: Python 3 and higher is required.
# Levenshtein package is required for sentence comparison.  
# Use: $sudo pip3 install python-Levenshtein
##############################################################################################



Annotation phage:
Data: Tac 2017 ADR testing corpus.
Data extension format: xml
Data repo: 1_remove_section/test_xml  
____________________________________________________________________________________________________
# Step1. Insert PMID intentionally so as to meet the file input requirement from Metamap
# input directory is 1_remove_section/test_xml 
# output directory is 1_remove_section/insert_PMID_test
$python 1_remove_section/Jyy_1insert_PMID.py test_xml [train_xml/test_xml]

# Step2. To format the file structure, e.g., table formatting, blank removal, etc.
# input directory is 1_remove_section/insert_PMID_test
# output directory is 1_remove_section/formatted_pro_test
$python 1_remove_section/Jyy_2formatted_pro.py [train_xml/test_xml]

# Step3. Stitch (catenate) files in input directory to one file, so as to make it easy for Metamap task submission.
# input directory is 1_remove_section/formatted_pro_test
# output file is 2_MetaMap_process_result/Stitched_test.txt
$python 2_MetaMap_process_result/Zky_1stitching.py [train_xml/test_xml]

# Step4. Submist Stitched_test.txt to MetaMap, and receive its result. Saved as 2_MetaMap_process_result/text.out. https://mmtx.nlm.nih.gov/ --> Use batach Metamap.

# Step5. Split text.out, result obtained from Metamap, and map each back to orignial files.
# Input file is 2_MetaMap_process_result/Stitched_test.txt
# Output directory is 2_MetaMap_process_result/metamapoutput.test
$ python 2_MetaMap_process_result/zky_2get_finalout.py [train_xml/test_xml]

# Step 6. Annotation part. Collect metamap reporting files, extract candidate ADR entries and their phrase info, locate the ADR entries with their occurrence place in original XML file, and write the ADR entries/mentions into the new XML files.  
# Input directory is 2_MetaMap_process_result/metamapoutput.test
# Output directory is 3_standardization/result
$python3 3_standardization/zky_phase_compare.py [train_xml/test_xml]

________________________________________________________________________________________


Evaluation phage:
Data: Tac 2017 ADR training corpus.
Data extension format: xml
Data repo: 1_remove_section/train_xml  
#Step1:Get str from oringal xml file and predicted results that will help us to calulate the recall_rate and precision.
$python 4_evaluation/zky_getdata.py train.xml
$ python 4_evaluation/zky_evaluation.py train.xml
#step2:Visually display with a graph
$python 4_evaluation/zky_matplotlib.py train.xml

