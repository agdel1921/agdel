import pandas as pd
import csv
import openpyxl as xl
import collections
from collections import defaultdict
from treelib import Tree, Node
import sys
import os
import pydot
import numpy as np
reload(sys)
sys.setdefaultencoding('utf-8')


### path to files individual data is stored
PATH='D:/training/TWG_overall/data_harmonisation/KR/Korea/Korea_Schema/'
os.chdir(PATH)

### path to individual data files
PATH_Data='D:/training/TWG_overall/data_harmonisation/KR/Korea/Korea_Schema/ind/'


### function to read in each individual table's Schema & store it as a DF
def sheetframes():
    wb = pd.ExcelFile('TWG_Scema.xlsx')
    path=PATH
    sheetNames=wb.sheet_names
    newSheet=list()
    for i in sheetNames:
        i=str(i)
        newSheet.append(i)
        sheet=wb.parse(i)
        csvName=path+i+'.csv'
        #with open(csvName,'wb') as f:
            #c = csv.writer(f)
            #for r in sheet.rows:
                #c.writerow([cell.value for cell in r])
    cnt=0
    numberList=list()
    for i in newSheet:
        numberList.append(cnt)
        cnt+=1
    d = {'col1': numberList, 'col2': newSheet}
    df = pd.DataFrame(data=d)
    df.to_csv('Sample.csv',index=None)
    # the actual tables start only from the 36th worksheet in TWG_Scema.xlsx. Hence, remove first 35 worksheet names
    sheetFrame=newSheet[36:]
    sheetFrame.append('ANINSP')
    return sheetFrame




### Importing Files

# import Anna's AEv3 WLS Contract mapping
annaTemplatedf=pd.read_csv("Anna_Contract_Template.csv")
# import Ms Kim's mapping of KR's data to AEv3
kimMappingdf=pd.read_csv("KIM_Mapping.csv")
# import Ajay's prepped version of KIM_Mapping
ajMappingdf=pd.read_csv("Mapping_Fields_Korea.csv")


### Removing the values that was not mapped by kim and going with Kim

# keep only those fields which Ms Kim says can be mapped to AEv3 i.e. remove fields with NA in the MR field
kimMappingdf=kimMappingdf.dropna(subset=['MR'])
# reset the index for this DF
kimMappingdf=kimMappingdf.reset_index(drop=True)
requiredHeaders=['AE FIELD NAME','MR','MR Field','FIELD TYPE','FIELD LENGTH']
kimMappingdf=kimMappingdf[requiredHeaders]


### Checking all tables present in the given schema files

kimTablesNotFound=list()
# find all tables mapped by Ms Kim from KR to AEv3
kimTablesrequied=kimMappingdf['MR'].tolist()

# find all tables present in KR Schema & store result as list in sample_list
sample_list=sheetframes()
sample_list=list(set(sample_list))

kimTablesrequied=list(set(kimTablesrequied))

# find tables used by Ms Kim in mapping, but not present in KR Schema
for i in kimTablesrequied:
    if i not in sample_list:
        kimTablesNotFound.append(i)

# remove these mismatching tables & the corresponding fields from Ms Kim's final mapping of KR to AEv3
for i in kimTablesNotFound:
    kimTablesrequied.remove(i)
    kimMappingdf = kimMappingdf[kimMappingdf.MR != i]
# AONA06 should not be there

"""
kimTables_tables=list()
kimTables_fields=list()
kimTables_tables=kimMappingdf['MR'].tolist()
kimTables_fields=kimMappingdf['MR Field'].tolist()
"""


### Extracting the fields from kim's template and cross matching with the schema
kimTables_tables=list()
kimTables_fields=list()
# the table the field originates from
kimTables_tables=kimMappingdf['MR'].tolist()
# the actual field name
kimTables_fields=kimMappingdf['MR Field'].tolist()
kimCleaned_field = []
kimCleaned_tbl = []
Counter=0
for i in kimTables_fields:
    if len(i)> 6:
        solutions=list()
        # case if there are multiple fields are present
        if str(i).find('||') != -1:
            text = str(i)
            text = text.split('||')
            for i in text:
                solutions.append(i)
        # case if a SUBSTR is present
        elif str(i).find('SUBSTR') != -1:
            text = str(i)
            idx = text.find('(')
            subs = text[idx + 1:idx + 7]
            solutions.append(subs)
        # case if multiple fields are present
        elif str(i).find(',') != -1 & str(i).find('SUBSTR') == -1 :
            text = str(i)
            text = text.split(',')
            for i in text:
                solutions.append(i)
        #case if only single field is present
        else:
            text=str(i)
            idx=text.find('(')
            text=text[idx-6:idx]
            solutions.append(text)
        for x in solutions:
            kimCleaned_field.append(str.strip(x))
            kimCleaned_tbl.append(str.strip(kimTables_tables[Counter]))
        Counter+=1
    else:
        kimCleaned_field.append(str.strip(i))
        kimCleaned_tbl.append(str.strip(kimTables_tables[Counter]))
        Counter += 1


len(kimTables_fields)
len(kimTables_tables)

Counter=0
del_cnt=0
fields=list()
tables=list()

for i in kimTables_fields:
    fields.append(i)

for i in kimTables_tables:
    tables.append(i)

# remove fields with multiple values / calculcations on fields
for i in kimTables_fields:
    if len(i)>8:
        Counter=Counter-del_cnt
        fields.remove(i)
        del tables[Counter]
        Counter+=1
        del_cnt= 1
    else:
        Counter+=1

newfields=list()
for i in fields:
    i = str(i).replace(' ', '')
    newfields.append(i)

new_tables=list(set(tables))


fieldsAndTables=zip(newfields,tables)
fieldsAndTablesdict=dict(fieldsAndTables)

# please ensure you do not sort either of the 'fields' or 'new_tables' lists - doing so will cause a mismatch in the two


# Validating fields present in the table
fieldsNotInTable=list()
fieldNames=list()
for i in newfields:
    if i=='AIDSCT':
        file_name='AONA09'
    else:
        file_name=fieldsAndTablesdict[i]
    actual_path = PATH_Data + file_name + '.csv'
    data = pd.read_csv(actual_path)
    # extract the 8th field of the Data File read in
    slicedFields = data[[8]]
    # the actual field names start after the 6th row, hence drop the first 5
    slicedFields = slicedFields[6:]
    # drop the fields with na
    slicedFields = slicedFields.dropna()
    slicedFields.columns = ['FieldName']
    slicedFields = slicedFields.reset_index(drop=True)
    list_slicedFields = slicedFields['FieldName'].tolist()
    if i not in list_slicedFields:
        fieldNames.append(i)
        name=i+' is not present in the table '+file_name
        fieldsNotInTable.append(name)
fieldsNotInTable=list(set(fieldsNotInTable))
fieldNames=list(set(fieldNames))
for i in fieldNames:
    newfields.remove(i)


# Mapping AE Names
for i in fieldNames:
    kimMappingdf = kimMappingdf[kimMappingdf['MR Field'] != i]

#  Field Type and specifications

kimTables_tables=kimMappingdf['MR'].tolist()
kimTables_fields=kimMappingdf['MR Field'].tolist()
kimTables_datatype=kimMappingdf['FIELD TYPE'].tolist()
Omit_Fields=list()
for i in kimTables_fields:
    if len(i) > 8:
        Omit_Fields.append(i)

for i in Omit_Fields:
    kimMappingdf = kimMappingdf[kimMappingdf['MR Field'] != i]

kimTables_tables=kimMappingdf['MR'].tolist()
kimTables_fields=kimMappingdf['MR Field'].tolist()
kimTables_datatype=kimMappingdf['FIELD TYPE'].tolist()
kimTables_datatype = ['VARCHAR(65355)' if (x=='CHAR') else x for x in kimTables_datatype]
kimTables_datatype = ['INT' if (x=='NUMERIC') else x for x in kimTables_datatype]
kimTables_datatype = ['INT' if (x=='NUMERIC ') else x for x in kimTables_datatype]
kimTables_datatype = ['DATE' if (x=='C') else x for x in kimTables_datatype]

fieldsDatatype=zip(kimTables_fields,kimTables_datatype)
fieldsAndTablesdict=dict(fieldsDatatype)


# Schema Generating CSV


nSlicedFields=list()
sheetFrame=sheetframes()
schemaStatement_List=list()
for i in sheetFrame:
    actual_path=PATH + i + '.csv'
    data=pd.read_csv(actual_path)
    schemaStatement='CREATE TABLE IF NOT EXISTS '+i+'('
    slicedFields = data[[8]]
    slicedFields = slicedFields[6:]
    slicedFields = slicedFields.dropna()
    slicedFields.columns = ['FieldName']
    slicedFields = slicedFields.reset_index(drop=True)
    list_slicedFields = slicedFields['FieldName'].tolist()
    maxFields = len(list_slicedFields)
    nSlicedFields.append(maxFields)
    counter = 0
    for i in list_slicedFields:
        counter += 1
        if i in kimTables_fields:
            dtype=fieldsAndTablesdict[i]
            if counter == maxFields:
                schemaStatement += i + " "+dtype + ") ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde' with serdeproperties ( 'separatorChar' = ',',  'quoteChar'     = '\"')   STORED AS TEXTFILE; "
            else:
                schemaStatement += i +" "+dtype + ','
        else:
            if counter == maxFields:
                schemaStatement += i + " VARCHAR(65355)) ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde' with serdeproperties ( 'separatorChar' = ',',  'quoteChar'     = '\"')   STORED AS TEXTFILE; "
            else:
                schemaStatement += i + ' VARCHAR(65355),'
    schemaStatement_List.append(schemaStatement)
schemaData= {'col1': sheetFrame, 'col2': schemaStatement_List}
schemaDataFrame = pd.DataFrame(data=schemaData)
schemaDataFrame.to_csv('SchemaKorea.csv',index=None)
validateData= {'col1': sheetFrame, 'col2': nSlicedFields}
validateDataFrame = pd.DataFrame(data=validateData)
validateDataFrame.to_csv('validateFieldsKorea2.csv',index=None)

schemaData= {'col1': schemaStatement_List}
schemaDataFrame = pd.DataFrame(data=schemaData)
schemaDataFrame.to_csv('SchemaKorea_123.csv',index=None)




data_pk=pd.read_csv('C:\Users\Sam\PycharmProjects\Korea_Schema\primarykeys.csv')
listPrimaryKey = data_pk.values.tolist()
defaultpk = defaultdict(list)
for k, v in listPrimaryKey:
    v=str(v)
    v=v[2:]
    defaultpk[k].append(v)
dictPrimaryKeys = dict((k, tuple(v)) for k, v in defaultpk.iteritems())

''' DIRECT CONNECTIONS'''
table_list=list(set(data_pk['Table'].tolist()))
mapped_tables=list()
primary_table=list()

for i in table_list:
    keylist=dictPrimaryKeys[i]
    file=str(i)
    newlist=list()
    for j in keylist:
        newlist.append(j)
    for j in sheetFrame:
            if j!=file:
                actual_path = PATH + j + '.csv'
                data = pd.read_csv(actual_path)
                slicedFields = data[[8]]
                slicedFields = slicedFields[6:]
                slicedFields = slicedFields.dropna()
                slicedFields.columns = ['FieldName']
                slicedFields = slicedFields.reset_index(drop=True)
                list_slicedFields = slicedFields['FieldName'].tolist()
                counter=0
                for k in newlist:
                    for l in list_slicedFields:
                        l=str(l)
                        l=l[2:]
                        if l==k:
                         counter+=1
                        if counter==len(newlist):
                            counter=0
                            primary_table.append(file)
                            mapped_tables.append(j)
FirstConnection= {'Primary Table': primary_table, 'Mapped Table': mapped_tables}
FirstConnection = pd.DataFrame(data=FirstConnection)
FirstConnection.to_csv('Connection12.csv',index=None)
identifier=list()
counter=0
for i in sheetFrame:
    counter+=1
    identifier.append(counter)
fieldsIdentifier=zip(sheetFrame,identifier)
fieldsIdentifierdict=dict(fieldsIdentifier)
listtree = FirstConnection.values.tolist()
listtreedict = defaultdict(list)
for v,k in listtree:
    listtreedict[k].append(v)
dicttree = dict((k, tuple(v)) for k, v in listtreedict.iteritems())


def treeBuild(parent,dicttree,IdentifierDict,tree,AddedTree):
    while True:
        newAdded=list()
        try:
            childs=dicttree[parent]
            for i in childs:
                if i not in AddedTree:
                    tree.create_node(i,IdentifierDict[i],parent=IdentifierDict[parent])
                    AddedTree.append(i)
                    newAdded.append(i)
                    for j in newAdded:
                        tree, AddedTree, newAdded = treeBuild(i, dicttree, IdentifierDict, tree, AddedTree)
            break
        except KeyError,e:
            print e
            break
    return tree,AddedTree,newAdded

def treeBuildParent(parent,IdentifierDict,AddedTree):
    tree.create_node(parent,IdentifierDict[parent])
    AddedTree.append(parent)
    return tree,AddedTree


depth=list()
depth1=list()
sheet=list()
tablestocount=list()
table_counts=list()
tablestocount=list(set(kimTables_tables))
for i in tablestocount:
    table_counts.append(kimTables_tables.count(i))
kimcount=dict(zip(tablestocount,table_counts))
count_list=list()
sheetFrame_new=list()
sheetFrame_new = list(dicttree.keys())
sheet_do=list()
for k in sheetFrame_new:
    addedTree = list()
    count=0
    d_list=dicttree[k]
    tree=Tree()
    tree,addedTree=treeBuildParent(k,fieldsIdentifierdict,addedTree)
    tree,addedTree,newAdded=treeBuild(k,dicttree,fieldsIdentifierdict,tree,addedTree)
    depth.append(tree.size())
    depth1.append(len(addedTree))
    sheet.append(k)
    for i in addedTree:
        if i in tablestocount:
            count+=kimcount[i]
    count_list.append(count)
    sheet_do.append(k)
treedataframe= {'Name': sheet_do,'Count':count_list,'Depth':depth}
treedataframe = pd.DataFrame(data=treedataframe)
treedataframe.to_csv('tree.csv',index=None)
max_value = max(depth)
max_index = depth.index(max_value)

addedTree=list()
k='ANADJP'
tree=Tree()
tree, addedTree = treeBuildParent(k, fieldsIdentifierdict, addedTree)
tree, addedTree, newAdded = treeBuild(k, dicttree, fieldsIdentifierdict, tree, addedTree)

listallpk=list()
for i in addedTree:
    j=dictPrimaryKeys[i]
    for k in j:
        listallpk.append(k)
listallpk=list(set(listallpk))
newlymapped=list()
for i in sheetFrame:
    count=0
    if i not in addedTree:
        print i
        try:
            keys=dictPrimaryKeys[i]
        except KeyError,e:
            continue
        for j in keys:
            if j in listallpk:
                count+=1
        if count==len(keys):
            newlymapped.append(i)





addedTree.append(k)
for i in d_list:
    if i not in addedTree:
        tree.create_node(i,fieldsIdentifierdict[i],parent=fieldsIdentifierdict[k])
        addedTree.append(i)
for i in d_list:
    d_list_new = dicttree[i]
    for j in d_list_new:
        if j not in addedTree:
            tree.create_node(j, fieldsIdentifierdict[j], parent=fieldsIdentifierdict[i])
            addedTree.append(j)


tree.create_node("Harry","harry") # root node
tree.create_node("Jane", "jane", parent="harry")
tree.create_node("Bill", "bill", parent="harry")
tree.create_node("Diane", "diane", parent="jane")
tree.create_node("Mary", "mary", parent="diane")
tree.create_node("Mark", "mark", parent="jane")

tree.show()

tree.display("Harry")
print("***** DEPTH-FIRST ITERATION *****")
for node in tree.traverse("Harry"):
    print(node)
print("***** BREADTH-FIRST ITERATION *****")
for node in tree.traverse("Harry", mode=_BREADTH):
    print(node)




def createtree():


''' Second Level Conncetions'''
all_mapped_fields = list()
for i in mapped_tables:
    actual_path = PATH + i + '.csv'
    data = pd.read_csv(actual_path)
    slicedFields = data[[8]]
    slicedFields = slicedFields[6:]
    slicedFields = slicedFields.dropna()
    slicedFields.columns = ['FieldName']
    slicedFields = slicedFields.reset_index(drop=True)
    list_slicedFields = slicedFields['FieldName'].tolist()
    for i in list_slicedFields:
        all_mapped_fields.append(i)
new_table_list=list()
new_table_list=list(set(table_list)-set(mapped_tables))
for i in new_table_list:
    keylist = dictPrimaryKeys[i]
    file = str(i)
    newlist = list()
    counter=0
    for j in keylist:
        newlist.append(j)
        for k in newlist:
            for l in all_mapped_fields:
                    if l == k:
                        print l

                        print i
                        counter += 1
                    if counter == len(newlist):
                        counter = 0
                        print i
                        mapped_tables.append(i)

