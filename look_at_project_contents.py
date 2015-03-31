#!/usr/bin/python

import panoptesPythonAPI


# get token
token = panoptesPythonAPI.get_bearer_token("mkosmala","hard2guess")


#panoptesPythonAPI.dump_all_projects("mkosmala",token)

#panoptesPythonAPI.delete_project(153,token)


panoptesPythonAPI.dump_project("Season Spotter Alpha3","mkosmala",token)
print "--- contents ---"
panoptesPythonAPI.dump_project_contents(204,token)
print "--- workflows ---"
for ind in range(550,560):
    print ind
    panoptesPythonAPI.dump_workflow(ind,token)
print "--- subject sets ---"
for ind in range(1011,1034):
    print ind
    panoptesPythonAPI.dump_subject_set(ind,token)

print "\n"
#panoptesPythonAPI.dump_project("Builder_2015_03_27","mkosmala",token)
#panoptesPythonAPI.dump_workflow(178,token)
#panoptesPythonAPI.dump_subject_set(399,token)
#panoptesPythonAPI.dump_subject_set(400,token)

#panoptesPythonAPI.dump_project_contents(170,token)
