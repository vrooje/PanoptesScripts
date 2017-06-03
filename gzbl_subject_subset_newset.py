#!/usr/bin/python

import panoptesPythonAPI
import csv
import os
import json
import pandas as pd


# TO DO
# add other users after they have created accounts

# ------------------
# FILES WITH CONTENT
# ------------------

subjectlistfile = "/Users/vrooje/Documents/Astro/Zooniverse/panoptes_analysis/data_out/barlengths_allwith_p_bar_gt_0p2.csv"
#manifestfile = "beta_manifest.csv"
#manifestfile = "beta_manifest_mini.csv"
#workflow_dir = "workflows/"
#linkfile = "subjectsets_and_workflows.csv"
auth = "authentication.txt"


project_id = 3
#workflow_id = 1623
subject_set_id = 4046







########
# MAIN #
########

# get token
with open(auth,'r') as authfile:
    areader = csv.reader(authfile,delimiter=',')
    row = areader.next()
    username = row[0]
    password = row[1]

token = panoptesPythonAPI.get_bearer_token(username,password)

subject_info = pd.read_csv(subjectlistfile) # this contains lots more than just subject ID
subject_list_int = subject_info.subject_id.tolist()
subject_list = [str(q) for q in subject_list_int]

# name of new subject set
#display_name = "All with p_bar geq 0.2"
display_name = "new-GZBL-subjects"

# this is very slow - better to create the empty subject set and then add the links to subjects to it
#subject_set_id = panoptesPythonAPI.create_subject_set(project_id,display_name,subject_list,token)


response_data = add_subjects_to_subject_set(subject_set_id, subject_list, token)

#projid_simp = panoptesPythonAPI.get_projectid_from_projectname(project_simple,username,token)
