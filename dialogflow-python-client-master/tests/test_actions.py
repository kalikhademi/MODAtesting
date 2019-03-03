# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import sys
import os
import json
import os.path
import re
import csv

try:
    import apiai
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
    import apiai

CLIENT_ACCESS_TOKEN = '51d0c44c7a414dc282db633eceaf1e1a'
 
class TestActions(unittest.TestCase):
    def setUp(self):
        self.ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    def load_text_request_with_quiery(self, query=None, resetContexts=False, entities=None):
        if not query:
            self.assertTrue(False)

        text_requset = self.ai.text_request()
        text_requset.query = query

        text_requset.resetContexts = resetContexts

        text_requset.entities = entities

        response = text_requset.getresponse()
        #print(response)
        
        return json.loads(response.read().decode())
       

    def test_hello(self):
        query = 'Hello'

        response = self.load_text_request_with_quiery(query)

        result = response['result']

        self.assertEqual(result['resolvedQuery'].lower(), query.lower())

        self.assertEqual(result['action'], 'input.welcome')
        self.assertEqual(result['fulfillment']['speech'], 'Welcome to our store. Are you looking for something particular today?')
        #print(result)

    def test_you_name(self):
        query = 'I am looking for an air filter'

        response = self.load_text_request_with_quiery(query)

        result = response['result']

        self.assertEqual(result['resolvedQuery'].lower(), query.lower())
        self.assertEqual(result['action'], 'searchFilterWithoutAttr')
        self.assertTrue(len(result['contexts']) == 2)

        context = result['contexts'][0]

        self.assertEqual(context['name'], 'search-filter-without-attribute')
        self.assertTrue(len(context['parameters']) == 2)
        #print(result)


    def test_user_entities(self):
        entities = [
            apiai.Entity(
                'filter',
                [
                    apiai.Entry('filter','filter'),
                    apiai.Entry('air filter','air filter'),
                ]
            ),
            apiai.Entity(
                'brand',
                [
                    apiai.Entry('Honeywell',['honeywell','honeyw','honey','Honeywell Elite Allergen','Honeywell Alergen Plus','Honeywell Superior Allergen']),
                    apiai.Entry('Filtrete',['filtrete','3M Filtrete MPR2200','3M Filtrete MPR1000','3M Filtrete MPR600','3M Filtrete MPR300']),
                    apiai.Entry('3M',['3m','3M','filtrete','3M Filtrete MPR2200','3M Filtrete MPR1000','3M Filtrete MPR600','3M Filtrete MPR300']),
                    apiai.Entry('Nordic Pure',['nordic pure','nordic','nordicpure','nordic pure m14','nordic pure m12','nordic pure m8','m14','m12','m8']),

                ]
            ),
            apiai.Entity(
                'criteria',
                [
                    apiai.Entry('below','below'),
                    apiai.Entry('under','under'),
                    apiai.Entry('at most','at most'),
                    apiai.Entry('lower than','lower than'),
                    apiai.Entry('underneath','underneath'),
                    apiai.Entry('beneath','beneath'),
                    apiai.Entry('less than','less than'),
                    apiai.Entry('smaller than',['smaller than','no greater than']),
                    apiai.Entry('maximum','maximum'),
                    apiai.Entry('bigger than','bigger than'),
                    apiai.Entry('larger than',['larger than','no less than']),
                    apiai.Entry('at least','at least'),
                    apiai.Entry('above','above'),
                    apiai.Entry('over','over'),
                    apiai.Entry('more than','more than'),
                    apiai.Entry('higher than','higher than'),
                    apiai.Entry('beyond','beyond'),
                    apiai.Entry('greater than','greater than'),
                    apiai.Entry('minimum','minimum'),
                    apiai.Entry('in the middle of','in the middle of'),
                    apiai.Entry('between','between'),
                    apiai.Entry('equals','equals'),
                    apiai.Entry('match','match'),
                    apiai.Entry('be level with','be level with'),
                    apiai.Entry('matches','matches'),
                    apiai.Entry('equal to','equal to'),
                ]
            ),
            apiai.Entity(
                'filterAttributes',
                [
                    apiai.Entry('customer star rating',['reviews','customer rating','star rating','consumer rating','stars','feedback','customer reviews','opinion','appraisal','reputable','customer star rating']),
                    apiai.Entry('mold filtering ability',['mold','fungus','fungi','mold filtering ability']),
                    apiai.Entry('MERV rating',['merv','efficiency rating','rating of','rating','ratings','MERV rating']),
                    apiai.Entry('appearance',['looks','look','design','generic looking','looks generic','looks cheap','looks expensive','cheap look','expensive look','packaging','appearance']),
                    apiai.Entry('price',['Price','pricey','pricier','overpriced','money','expense','expensive','expenditure','inexpensive','cost','cheap','cheaper','cheapest','pay','paid','budget','dollars','dollar','price premium','premium price','economic','ecnomically','economical','financially']),
                    apiai.Entry('bacteria filtering ability',['bacteria','bacterial','germs','bacterias','pathogens','virus','viral','viruses','bacteria filtering ability']),
                    apiai.Entry('pollen filtering ability',['pollen','flower','air irritant','ragweed','pollen filtering ability']),
                    apiai.Entry('smoke odor filtering Ability',['smoke odor','smoke smell','smoke musk','smoke stench','smoke stink','smoke odor filtering ability']),
                    apiai.Entry('lint and fiber filtering Ability',['lint','fiber','clumps','lint and fiber filtering ability']),
                    apiai.Entry('allergen defense',['allergen defense','allergies','allergy','asthma','allergens','allergen','breathing','sinus','sinuses','allergic']),
                    apiai.Entry('dust filtering ability',['dust','dirt','particles','dusting','particulate','granular','mote','motes','speck','specks','dust filtering ability']),
                    apiai.Entry('smoke filtering Ability',['smog','smoke','smoke filtering Ability']),
                    apiai.Entry('overall air filtering effectiveness',['effectiveness','effective','quality','ability','capability','filterability','filters well','performance','does the job','performs','works']),
                    apiai.Entry('spore filtering Ability',['spores','spore','spore filtering','spore filtering Ability']),
                    apiai.Entry('pet dander filtering ability',['cat','dog','kitten','puppy','animal','hair','pet dander filtering ability','pet dander']),
                    apiai.Entry('overall evaluation',['evaluation','good air filter','bad air filter','good filter','bad filter','great air filter','great filter','excellent air filter','excellent filter','poor air filter','poor filter','fine air filter','fine filter','acceptable air filter','acceptable filter','perfect air filter','perfect filter','basic air filter','basic filter','reasonable air filter','reasonable filter','interior air filter','interior filter','suerior air filter','superior filter','best air filter','best filter','worst air filter','worst filter','overall evaluation']),
                    apiai.Entry('sturdiness or durability',['durability', 'sturdiness','sturdy','sturdier','durable','stability','strength','rigid','reinforcement','crumble','crumbling','instability','flimsy','unstable','stable','construction','sloppy','sturdiness or durability']),
                    apiai.Entry('tobacco smoke',['tobacco','cigarette','cigar','tobacco smoke']),
                    apiai.Entry('odor Filtering Ability',['odor','odors','smell','musk','stench','stink','odor Filtering Ability']),
                    apiai.Entry('air flow',['air flow','air pressure','hvac','pressure drop','pull air','air velocity','pulling air','pressure of air','restrict','restriction','flow of air','strain','blower','restrictive','straining','resistance','overheat','over freeze']),
                    apiai.Entry('filter material quality',['material','filter fiber','weave','mesh','netting','filter fibers','pleating','pleated','pleats','tread','treads','web']),
                    apiai.Entry('replacement time',['change','last','replace','duration','life','time','permanent']),
                ]
            ),
            apiai.Entity(
                'nonQuantitativeAttr',
                [
                    apiai.Entry('allergen defense',['allergen defense','allergies','allergy','asthma','allergens','allergen','breathing','sinus','sinuses','allergic']),
                    apiai.Entry('dust filtering ability',['dust','dirt','particles','dusting','particulate','granular','mote','motes','speck','specks','dust filtering ability']),
                    apiai.Entry('tobacco smoke',['tobacco','cigarette','cigar','tobacco smoke']),
                    apiai.Entry('spore filtering Ability',['spores','spore','spore filtering','spore filtering Ability']),
                    apiai.Entry('appearance',['looks','look','design','generic looking','looks generic','looks cheap','looks expensive','cheap look','expensive look','packaging','appearance']),
                    apiai.Entry('overall air filtering effectiveness',['effectiveness','effective','quality','ability','capability','filterability','filters well','performance','does the job','performs','works']),
                    apiai.Entry('odor Filtering Ability',['odor','odors','smell','musk','stench','stink','odor Filtering Ability']),
                    apiai.Entry('overall evaluation',['evaluation','good air filter','bad air filter','good filter','bad filter','great air filter','great filter','excellent air filter','excellent filter','poor air filter','poor filter','fine air filter','fine filter','acceptable air filter','acceptable filter','perfect air filter','perfect filter','basic air filter','basic filter','reasonable air filter','reasonable filter','interior air filter','interior filter','suerior air filter','superior filter','best air filter','best filter','worst air filter','worst filter','overall evaluation']),
                    apiai.Entry('mold filtering ability',['mold','fungus','fungi','mold filtering ability']),
                    apiai.Entry('bacteria filtering ability',['bacteria','bacterial','germs','bacterias','pathogens','virus','viral','viruses','bacteria filtering ability']),
                    apiai.Entry('sturdiness or durability',['durability', 'sturdiness','sturdy','sturdier','durable','stability','strength','rigid','reinforcement','crumble','crumbling','instability','flimsy','unstable','stable','construction','sloppy','sturdiness or durability']),
                    apiai.Entry('pet dander filtering ability',['cat','dog','kitten','puppy','animal','hair','pet dander filtering ability','pet dander']),
                    apiai.Entry('smoke filtering Ability',['smog','smoke','smoke filtering Ability']),
                    apiai.Entry('smoke odor filtering Ability',['smoke odor','smoke smell','smoke musk','smoke stench','smoke stink','smoke odor filtering ability']),
                    apiai.Entry('filter material quality',['material','filter fiber','weave','mesh','netting','filter fibers','pleating','pleated','pleats','tread','treads','web']),
                    apiai.Entry('air flow',['air flow','air pressure','hvac','pressure drop','pull air','air velocity','pulling air','pressure of air','restrict','restriction','flow of air','strain','blower','restrictive','straining','resistance','overheat','over freeze']),
                    apiai.Entry('pollen filtering ability',['pollen','flower','air irritant','ragweed','pollen filtering ability']),
                    apiai.Entry('lint and fiber filtering Ability',['lint','fiber','clumps','lint and fiber filtering ability']),
                ]
            ),
            apiai.Entity(
                'quantitativeAttr',
                [
                    apiai.Entry('price',['Price','pricey','pricier','overpriced','money','expense','expensive','expenditure','inexpensive','cost','cheap','cheaper','cheapest','pay','paid','budget','dollars','dollar','price premium','premium price','economic','ecnomically','economical','financially']),
                    apiai.Entry('MERV rating',['merv','efficiency rating','rating of','rating','ratings','MERV rating']),
                    apiai.Entry('replacement time',['change','last','replace','duration','life','time','permanent']),
                    apiai.Entry("customer star rating",["reviews","customer rating"])
                ]
            )
        ]

        path = os.path.dirname(os.getcwd()) + '/../cases/'
        correct = 0
        total = 0

        # Open output file
        outputFilename = os.path.dirname(os.getcwd()) + '/../default_Responses.txt'
        outputFilepath = open(outputFilename, 'r')
        outputFile = outputFilepath.readlines()
        outputFilepath.close()
        
        # Open json scripts
        jsonFolder = os.path.dirname(os.getcwd()) + '/../entities/'
        with open(jsonFolder+'brand_entries_en.json') as f:
            brandSynonym = json.load(f)
        with open(jsonFolder+'criteria_entries_en.json') as f:
            criteriaSynonym = json.load(f)
        with open(jsonFolder+'filter_entries_en.json') as f:
            filterSynonym = json.load(f)
        with open(jsonFolder+'filterAttributes_entries_en.json') as f:
            filterAttrSynonym = json.load(f)
        with open(jsonFolder+'nonQuantitativeAttr_entries_en.json') as f:
            nonQuantAttrSynonym = json.load(f)
        with open(jsonFolder+'quantitativeAttr_entries_en.json') as f:
            quantAttrSynonym = json.load(f)

        # find all the values & synonyms
        brandDict = {}
        for i in brandSynonym:
            brandDict[i['value']] = i['synonyms']
            brandDict[i['value']].append(i['value'])
        criteriaDict = {}
        for i in criteriaSynonym:
            criteriaDict[i['value']] = i['synonyms']
            criteriaDict[i['value']].append(i['value'])
        filterDict = {}
        for i in filterSynonym:
            filterDict[i['value']] = i['synonyms']
            filterDict[i['value']].append(i['value'])
        filterAttrDict = {}
        for i in filterAttrSynonym:
            filterAttrDict[i['value']] = i['synonyms']
            filterAttrDict[i['value']].append(i['value'])
        nonQuantAttrDict = {}
        for i in nonQuantAttrSynonym:
            nonQuantAttrDict[i['value']] = i['synonyms']
            nonQuantAttrDict[i['value']].append(i['value'])
        quantAttrDict = {}
        for i in quantAttrSynonym:
            quantAttrDict[i['value']] = i['synonyms']
            quantAttrDict[i['value']].append(i['value'])

        #print(brandDict)
        #print(criteriaDict)
        #print(filterDict)
        #print(filterAttrDict)
        #print(nonQuantAttrDict)
        #print(quantAttrDict)

        #for i in theRange:
        for i in range(9,11):

            incorrectQueries = []
            allQueries = []
            fileCorrect = 0
            fileTotal = 0
            print("Checking Case", i, ".txt")

            filename = path + 'case' + str(i) + '_testing_withBrackets.txt'
            filepath = open(filename, 'r')
            file = filepath.readlines()
            filepath.close()
        
            # get the expected output from output file
            expectedLine = outputFile[i-1].strip()
            splitList = expectedLine.split("[")
            splitList = [splitList[0]] + ["["+x for x in splitList[1:]]
            newSplitList = []

            # Breakdown string by whats in brackets
            for x in splitList:
                item = x.split("]")
                if (len(item) != 1):
                    newSplitList.append(item[0]+"]")
                    newSplitList.append(item[1])
                else:
                    newSplitList.append(item[0])

            for line in file:
                query = line
                queryInfo = []

                # Count the number of each attribute
                attributeCount = []
                if i == 7:
                    attributeCount.append(query.count("ATTRIBUTE"))
                if i == 8:
                    attributeCount.append(query.count("BRAND"))
                    attributeCount.append(query.count("ATTRIBUTE"))
                elif i == 9:
                    attributeCount.append(query.count("BRAND"))
                    attributeCount.append(query.count("ATTRIBUTE"))
                elif i == 10:
                    attributeCount.append(query.count("BRAND"))
                
                # if in the second file, skip parsing
                if i != 2:
            
                    while (query.find("[") != -1):
                        # Parse the query for the attribute block
                        attributeCont = query[query.find("["):query.find("]")+1]
                        attr = attributeCont.split("\"\"")[1]
                        query = query.replace(attributeCont, attr)

                if (query.find("3M") != -1):
                    query = query.replace("3M", "threeM")
                    
                # Add to output list
                queryInfo.append(query.strip())

                # Get the response from the dialogflow
                #print(query)
                response = self.load_text_request_with_quiery(query, resetContexts=True)
                #print(response['result']['parameters'])
                speech = response['result']['fulfillment']['speech']
            
                # Check if the responses are the same.
                sameText = True
                #print(speech)
                #print(newSplitList)

                tempSpeech = speech
                if (re.search("meet\W", tempSpeech) != None and i != 11):
                    tempSpeech = tempSpeech.replace("meet", "meets")
                if (tempSpeech.find("These models are") != -1):
                    tempSpeech = tempSpeech.replace("These models are", "This model is")
                if ( i == 5 and tempSpeech.find("This model is") != -1):
                    tempSpeech = tempSpeech.replace("This model is", "These models are")
                if (i != 11 and tempSpeech.find("meets your criteria") != -1):
                    tempSpeech = tempSpeech.replace("meets your criteria", "meet your criteria")
                if (i == 4 and tempSpeech.find("meet your criteria") != -1):
                    tempSpeech = tempSpeech.replace("meet your criteria", "meets your criteria")
                if (tempSpeech.find("model meets") != -1):
                    tempSpeech = tempSpeech.replace("model meets", "models meet")

                for section in newSplitList:
                    if (section == " or " or section == " and "):
                        continue
                    if (section[0] != "["):
                        if (tempSpeech.find(section) == -1):
                            if (speech.find(section) == -1):
                                print("Output: " + speech)
                                print("Changed to: " + tempSpeech)
                                print("Looking for: " + section)
                                #print(section)
                                sameText = False


                # if responses are not the same, print expected & actual
                if (not sameText):
                    #print("Query: " + query.strip())
                    #print("Actual: " + speech)
                    #print("Expected: " + expectedLine + "\n")
                    queryInfo.append(0)
                    incorrectQueries.append([query.strip(),response['result']['parameters'], speech, expectedLine])
                else:
                    queryInfo.append(1)
                    correct += 1
                    fileCorrect += 1

                parameters = response['result']['parameters']
                print(parameters)
                # Handle differently for each case

                def findAttribute(parameters, attribute, query, dictionary):
                    if (attribute in parameters):
                        attrVal = parameters[attribute]
                        if (attrVal == ''):
                            return 'NA', 0

                        if type(attrVal) == type([]):
                            vals = []
                            corrects = []
                            
                            for j in attrVal:
                                vals.append(j)
                                found = False
                                for x in dictionary[j]:
                                    if (query.find(x) != -1):
                                        found = True
                                        break
                                if (found):
                                    corrects.append(1)
                                else:
                                    corrects.append(0)

                            if len(vals) == 1:
                                return vals[0], corrects[0]
                            return vals, corrects

                            
                        # check if synonyms in the query
                        found = False
                        for x in dictionary[attrVal]:
                            if (query.find(x) != -1):
                                return attrVal, 1
                        return attrVal, 0

                    else:
                        return 'NA', 0

                if i == 1:
                    val, cor = findAttribute(parameters, 'filterAttributes', query, filterAttrDict)
                    queryInfo.append(val)
                    queryInfo.append(cor)
                    

                elif i == 3:
                    val, cor = findAttribute(parameters, 'brand', query, brandDict)
                    queryInfo.append(val)
                    queryInfo.append(cor)

                elif i == 4:
                    val, cor = findAttribute(parameters, 'brand', query, brandDict)
                    queryInfo.append(val)
                    queryInfo.append(cor)
                    
                    val, cor = findAttribute(parameters, 'criteria', query, criteriaDict)
                    queryInfo.append(val)
                    queryInfo.append(cor)

                    val, cor = findAttribute(parameters, 'quantitativeAttr', query, quantAttrDict)
                    if len(val) == 1:
                        queryInfo.append(val[0])
                        queryInfo.append(cor[0])
                    else:
                        queryInfo.append(val)
                        queryInfo.append(cor)

                elif i == 5:
                    val, cor = findAttribute(parameters, 'brand', query, brandDict)
                    queryInfo.append(val)
                    queryInfo.append(cor)

                    val, cor = findAttribute(parameters, 'nonQuantitativeAttr', query, nonQuantAttrDict)
                    queryInfo.append(val)
                    queryInfo.append(cor)


                elif i == 6:
                    val, cor = findAttribute(parameters, 'brand', query, brandDict)
                    queryInfo.append(val)
                    queryInfo.append(cor)

                    val, cor = findAttribute(parameters, 'quantitativeAttr', query, quantAttrDict)
                    queryInfo.append(val)
                    queryInfo.append(cor)

                elif i == 7:
                    val, cor = findAttribute(parameters, 'filterAttributes', query, filterAttrDict)
                    queryInfo.append(val)
                    queryInfo.append(cor)
                    # Make sure the correct number of attributes are returned
                    queryInfo.append(attributeCount[0])
                    if (isinstance(val, list) and attributeCount[0] == len(val)):
                        queryInfo.append(1)
                    elif (not isinstance(val, list) and val != "NA" and attributeCount[0] == 1):
                        queryInfo.append(1)
                    else:
                        queryInfo.append(0)

                elif i == 8:
                    val, cor = findAttribute(parameters, 'brand', query, brandDict)
                    queryInfo.append(val)
                    queryInfo.append(cor)
                    queryInfo.append(attributeCount[0])
                    if (isinstance(val, list) and len(val) == attributeCount[0]):
                        queryInfo.append(1)
                    elif (not isinstance(val, list) and val != "NA" and attributeCount[0] == 1):
                        queryInfo.append(1)
                    else:
                        queryInfo.append(0)

                    val, cor = findAttribute(parameters, 'filterAttributes', query, filterAttrDict)
                    queryInfo.append(val)
                    queryInfo.append(cor)
                    queryInfo.append(attributeCount[1])
                    if (isinstance(val, list) and len(val) == attributeCount[1]):
                        queryInfo.append(1)
                    elif (not isinstance(val, list) and val != "NA" and attributeCount[1] == 1):
                        queryInfo.append(1)
                    else:
                        queryInfo.append(0)

                elif i == 9:
                    val, cor = findAttribute(parameters, 'brand', query, brandDict)
                    queryInfo.append(val)
                    queryInfo.append(cor)
                    queryInfo.append(attributeCount[0])
                    if (isinstance(val, list) and len(val) == attributeCount[0]):
                        queryInfo.append(1)
                    elif (not isinstance(val, list) and val != "NA" and attributeCount[0] == 1):
                        queryInfo.append(1)
                    else:
                        queryInfo.append(0)

                    val, cor = findAttribute(parameters, 'filterAttributes', query, filterAttrDict)
                    queryInfo.append(val)
                    queryInfo.append(cor)
                    queryInfo.append(attributeCount[1])
                    if (isinstance(val, list) and len(val) == attributeCount[1]):
                        queryInfo.append(1)
                    elif (not isinstance(val, list) and val != "NA" and attributeCount[1] == 1):
                        queryInfo.append(1)
                    else:
                        queryInfo.append(0)

                elif i == 10:
                    val, cor = findAttribute(parameters, 'brand', query, brandDict)
                    queryInfo.append(val)
                    queryInfo.append(cor)
                    queryInfo.append(attributeCount[0])
                    if (isinstance(val, list) and len(val) == attributeCount[0]):
                        queryInfo.append(1)
                    elif (not isinstance(val, list) and val != "NA" and attributeCount[0] == 1):
                        queryInfo.append(1)
                    else:
                        queryInfo.append(0)

                elif i == 11:
                    val, cor = findAttribute(parameters, 'criteria', query, criteriaDict)
                    queryInfo.append(val)
                    queryInfo.append(cor)
                    
                    val, cor = findAttribute(parameters, 'filterAttributes', query, filterAttrDict)
                    queryInfo.append(val)
                    queryInfo.append(cor)

                allQueries.append(queryInfo)

                fileTotal += 1
                total += 1

            print("Total correct in this file: ", fileCorrect, " out of ", fileTotal)
            print("Writing to output"+ str(i)+".csv file...")
            with open("output files/output"+str(i)+"_testing.csv", "wb") as f:
                writer = csv.writer(f)
                writer.writerows(incorrectQueries)
            with open("output files/parameterOutput"+str(i)+"_testing.csv", "wb") as f:
                writer = csv.writer(f)
                writer.writerows(allQueries)

        print("Total Correct ", correct, " out of ", total)

        
        #with open('incorrectItems.txt', 'w') as f:
            #f.write('\n'.join(incorrectQueries))

if __name__ == '__main__':
    unittest.main()
