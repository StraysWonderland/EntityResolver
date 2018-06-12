import xml.etree.ElementTree as ET
import time
import numpy as np

# timestamp with start time
timestamp_start = time.time()

# parse xml into python element
tree = ET.parse('cora-all-id.xml')
root = tree.getroot()

# threshold for similarity calculation
threshold = 0.35

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
    current_attributes = []
    title = []
    for element in child:
        if(element.tag == 'author'): # store the author ids into the list
            current_attributes.append(element.attrib['id']) # collect all authors in a local list first 
        elif(element.tag == 'venue'):
            for ven in element:
                for item in ven:
                    current_attributes.append(item.text)
        elif(element.tag == 'title'):
            title.append(element.text)
    if(title != ""):
        full_title = ''.join(title)
        current_attributes.append(full_title)
    list_ids.append(child.attrib['id']) # store the id of the current publication in a list
    publications.append(current_attributes) # append the list with the collected authors to the publications

print("retrieved data entries")

##############
# GOLD STANDART
#--------------
golden_duplicates = []
gold_lookup = set()
# first loop to store the relevant data into lists
pos_comp = 0
for child in root:
    pos = 0
    for child_comp in root:
        if(child_comp.attrib['id'] == child.attrib['id'] and pos != pos_comp and (pos, pos_comp) not in gold_lookup):
            golden_duplicates.append((pos_comp,pos))
            gold_lookup.add((pos_comp,pos))
        pos += 1
    pos_comp += 1
    
print("retrieved golden duplicates")

################
#FIND DUPLICATES
#---------------
duplicates = [] # list with the publication ids of the duplicates
dup_lookup = set()

for j in range(0, len(publications)):
    list_buffer = [] # collect all duplicates in the local list first
    for i in range(0, len(publications)):
        diff = calculateSimilarity(publications[j], publications[i])
        if( diff < ( threshold* len(publications[j])) and i != j  and (i, j) not in dup_lookup):
            duplicates.append((j, i)) # add tuple of pair to evaluation list
            dup_lookup.add((j, i)) # add tuple of pair to evaluation list


print("retrieved duplicates")

###############
#PRECISION, RECALL & F1 SCORE
#---------------
true_positive = 0
false_positive = 0
false_negative = 0

for dup in duplicates:
    if(dup in gold_lookup):
        true_positive += 1
    else:
        false_positive += 1

for gold in gold_lookup:
    if gold not in dup_lookup:
        false_negative += 1

precision = true_positive / (true_positive + false_positive)
recall = true_positive / (true_positive + false_negative)
f1_score = 2*true_positive / (2*true_positive + false_positive + false_negative)

print("evaluation completed")
########################################
# PRINTING
print ('### {0} - {1}'.format("golden standart", "found duplicates"))
for i in range(200):    
    print('{:10} - {:>10}'.format(str(golden_duplicates[i]), str(duplicates[i])))

print("#######################################")
num_gold_duplicates = len(golden_duplicates)
num_found_duplicates = len(duplicates)
print(str(num_gold_duplicates) + " #duplicates in gold-standart"  )
print(str(num_found_duplicates) + " #retrieved duplicates " )
print("#######################################")
print("Evaluation")
print("True positives: " + str(true_positive))
print("False positives: " + str(false_positive))
print("false negative: " + str(false_negative))
print("...")
print("Precision: " + str(precision))
print("Recall: " + str(recall))
print("F1 Score: " + str(f1_score))
print("#######################################")
timestamp_end = time.time() - timestamp_start
print("Calculation Finished")
print('Time passed: ' + str(timestamp_end))
print("#######################################")