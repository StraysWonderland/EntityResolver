import xml.etree.ElementTree as ET
import time
import numpy as np

# timestamp with start time
timestamp_start = time.time()

# parse xml into python element
tree = ET.parse('cora-all-id.xml')
root = tree.getroot()

# threshold for similarity calculation
threshold = 3

########################################################
def getDiff(attributes_1, attributes_2):
    sim = 0
    for att_1 in attributes_1:
        for att_2 in attributes_2:
            if(att_1==att_2):
                sim += 1
    delta = len(attributes_1) - sim 
    return delta
########################################################

########################################################
# modified version of hamming distance
def calculateSimilarity(pub_comp, pub):
    diff = 0
    l_pub = len(pub)
    l_pub_comp = len(pub_comp)
    if(l_pub_comp < l_pub):
        diff = getDiff(pub, pub_comp)
    elif(l_pub_comp > l_pub):
        diff = getDiff(pub_comp, pub)
    elif(l_pub_comp == l_pub):
        diff = getDiff(pub_comp, pub)
    return diff
########################################################

publications = []   # list with the author ids for each publication
list_ids = []       # list with the ids of the publications

# first loop to store the relevant data into lists
for child in root:
    list_local_authors = []
    title = []
    for element in child:
        if(element.tag == 'author'): # store the author ids into the list
            list_local_authors.append(element.attrib['id']) # collect all authors in a local list first 
        elif(element.tag == 'venue'):
            for ven in element:
                for item in ven:
                    list_local_authors.append(item.text)
        elif(element.tag == 'title'):
            title.append(element.text)
    if(title != ""):
        full_title = ''.join(title)
        list_local_authors.append(full_title)
    list_ids.append(child.attrib['id']) # store the id of the current publication in a list
    publications.append(list_local_authors) # append the list with the collected authors to the publications


##############
# GOLD STANDART
#--------------
golden_duplicates = []
# first loop to store the relevant data into lists
for child in root:
    list_local_golden = []
    pos = 0
    for child_comp in root:
        if(child_comp.attrib['id'] == child.attrib['id']):
            list_local_golden.append(pos)
        pos += 1
    golden_duplicates.append(list_local_golden)
# uniquify golden duplicates
golden_duplicates = np.unique(golden_duplicates)


################
#FIND DUPLICATES
#---------------
duplicates = [] # list with the publication ids of the duplicates
for pub in publications:
    list_buffer = [] # collect all duplicates in the local list first
    for i in range(0, len(publications)):
        diff = calculateSimilarity(publications[i], pub)
        if(diff < threshold):
            list_buffer.append(i) # add the id of the publication to the pairs entry if they are similar
    duplicates.append(list_buffer)

# uniquify duplicates
duplicates = np.unique(duplicates)


########################################
# PRINTING
print("#### gold-standart duplicates ###")
for i in range(17):
    print(golden_duplicates[i])

print("#### retrieved duplicates ###")
for i in range(17):
    print(duplicates[i])

print("#######################################")
print(str(len(golden_duplicates)) + " #duplicates in gold-standart"  )
print(str(len(duplicates)) + " #retrieved duplicates " )
print("#######################################")

# timestamp for termination time
timestamp_end = time.time() - timestamp_start
print("Calculation Finished")
print('Time passed: ' + str(timestamp_end))
print("#######################################")