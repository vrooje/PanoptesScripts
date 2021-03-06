#!/usr/bin/python

import panoptesPythonAPI
import csv
import os
import json


# TO DO
# add other users after they have created accounts

# ------------------
# FILES WITH CONTENT
# ------------------

#manifestfile = "beta_manifest.csv"
manifestfile = "beta_manifest_mini.csv"
workflow_dir = "workflows/"
linkfile = "subjectsets_and_workflows.csv"

byline = "metatext/byline.txt"
introduction = "metatext/introduction.txt"
science = "metatext/science_case.txt"
faq = "metatext/faq.txt"
education = "metatext/education_content.txt"
results = "metatext/results.txt"

logo = "https://raw.githubusercontent.com/mkosmala/SeasonSpotterLanding/gh-pages/projectimages/SeasonSpotter_logo_small.png"
background = "https://raw.githubusercontent.com/mkosmala/SeasonSpotterLanding/gh-pages/projectimages/tamaracks_fall_RNC_cropped_1024x768.jpg"


# ------------------------------
# PROJECT NAME AND COLLABORATORS
# ------------------------------

project = "Season Spotter Test31"
collaborators = ["imaginaryfriend"]

# -----------
# DEFINITIONS
# -----------

# vegetation type lookup
veg_lookup = { "AG":"Agriculture",
               "DB":"Deciduous Broadleaf Forest",
               "DN":"Deciduous Needle-leaf Forest",
               "EB":"Evergreen Broadleaf Forest",
               "EN":"Evergreen Needle-leaf Forest",
               "GR":"Grassland",
               "MX":"Mixed Forest",
               "SH":"Shrubland",
               "TN":"Tundra",
               "WL":"Wetland" }



#---
# Add collaborators
#---
def add_collaborators(projid,token):

    # add each collaborator
    for coll in collaborators:

        # look up their ID
        collid = panoptesPythonAPI.get_userid_from_username(coll,token)
        if collid == -1:
            print "Warning! User \"" + coll + "\" does not exist. Cannot add as collaborator."

        else:    
            print "Adding collaborator: " + coll + ", ID: " + str(collid)
            panoptesPythonAPI.add_collaborator(projid,collid,token)

    return


#---
# Create the workflows
#---
def create_workflows(projid,token):
    workflows = os.listdir(workflow_dir)

    # load in each workflow
    for wf in workflows:

        wf_path = workflow_dir + wf
        with open(wf_path,'r') as wffile:
            workflow = wffile.read().replace('\n', '')

            wfname = wf.split('.')[0]

            # and build it
            print "Building workflow: " + wfname
            wfid = panoptesPythonAPI.create_workflow(projid,wfname,workflow,token)
            print "   ID: " + wfid

    return

# ---
# Create subject sets and upload the images
# ---
def create_subject_sets_and_subjects(projid,token):
    # read the manifest
    with open(manifestfile,'r') as mfile:

        # discard header and get csv object
        mfile.readline()
    
        # for each image
        mreader = csv.reader(mfile,delimiter=',',quotechar='\"')
        for row in mreader:
            image = row[0]
            subjset = row[1]
            site = row[2]
            vegabbr = row[3]
            loc = row[4]
            lat = row[5]
            lon = row[6]
            ele = row[7]

            # look up the vegetation type
            if vegabbr in veg_lookup:
                vegtype = veg_lookup[vegabbr]
            else:
                vegtype = vegabbr

            # check to see if the subject set(s) exists; create it if not
            subjsetnum = panoptesPythonAPI.get_subject_set(projid,subjset,token)
            if subjsetnum == -1:
                print "Building SubjectSet: " + subjset
                subjsetnum = panoptesPythonAPI.create_empty_subject_set(projid,subjset,token)
                
            # create the metadata object
            meta = """ "Camera": \"""" + site + """\",
                       "Location": \"""" + loc + """\",
                       "Vegetation": \"""" + vegtype + """\",
                       "Latitute": \"""" + lat + """\",
                       "Longitude": \"""" + lon + """\",
                       "Elevation": \"""" + ele + """\" """

            # create the subject
            print "Adding Subject: " + image
            subjid = panoptesPythonAPI.create_subject(projid,meta,image,token)

            # add it to the subject set(s)
            print "Linking Subject " + image + " to Subject Set " + subjset
            panoptesPythonAPI.add_subject_to_subject_set(subjsetnum,subjid,token)
        
    return



# ---
# Link SubjectSets to Workflows
# ---
def link_subject_sets_and_workflows(projid,token):

    # initialize the link list
    linklist = []

    # read in the link file
    with open(linkfile,'r') as lfile:

        # ignore header line
        lfile.readline()

        # read in all the pairs
        lreader = csv.reader(lfile,delimiter=',')
        for row in lreader:
            linklist.append(row)

    # get all the subject sets in this project
    subjsetids = panoptesPythonAPI.get_project_subject_sets(projid,token)

    # for each one, link to workflow(s)
    for ssid in subjsetids:

        #print "\nssid = " + str(ssid)

        # get the subjectset name
        ssname = panoptesPythonAPI.get_subject_set_name(projid,ssid,token)

        #print "   " + ssname

        #foundmatch = False
        # look through the links for workflow matches
        for eachpair in linklist:

            filewf = eachpair[0]
            filess = eachpair[1]

            # and link the matches
            if filess == ssname:

                # get the workflow id
                wfid = panoptesPythonAPI.get_workflow(projid,filewf,token)

                # link
                print "Linking subject set " + ssname + " to workflow " + filewf
                panoptesPythonAPI.link_subject_set_and_workflow(ssid,wfid,token)
            
                #foundmatch = True    

       #if not foundmatch:
       #     print "   no matching workflow found for subjectset: " + ssname


    return
    

def build_project_info():

    info = {}
    info["display_name"] = project

    with open (byline, "r") as infile:
        info["description"] = infile.read()

    with open (introduction, "r") as infile:
        info["introduction"] = infile.read()

    with open (science, "r") as infile:
        info["science_case"] = infile.read()

    with open (faq, "r") as infile:
        info["faq"] = infile.read()

    with open (education, "r") as infile:
        info["education_content"] = infile.read()

    #with open (results, "r") as infile:
    #    info["result"] = infile.read()

    info["avatar"] = logo
    info["background_image"] = background
    info["primary_language"] = "en-us"
    info["private"] = False
    #info["beta"] = True
    #info["live"] = True

    # for testing
    info["configuration"] = {'user_chooses_workflow':True}

    # for production
    #info["configuration"] = {'user_chooses_workflow':False}

    return info


########
# MAIN #
########

# get token
token = panoptesPythonAPI.get_bearer_token("mkosmala","hard2guess")

# create a project for simple workflows
# check to see if it's already created. if not, create it
projid = panoptesPythonAPI.get_projectid_from_projectname(project,"mkosmala",token)
if projid==-1:
    print "Creating project: " + project
    project_info = build_project_info()
    projid = panoptesPythonAPI.create_user_project(project_info,token)
else:
    print "Project already exists"
    exit(0)
    
print "   ID: " + projid 

# add collaborators
#add_collaborators(projid,token)

# add workflows
create_workflows(projid,token)

# add subject sets
create_subject_sets_and_subjects(projid,token)

# link the subject sets and workflows
link_subject_sets_and_workflows(projid,token)


    


