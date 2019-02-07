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
        return json.loads(response.read().decode())

    def test_hello(self):
        query = 'Hello'

        response = self.load_text_request_with_quiery(query)

        result = response['result']

        self.assertEqual(result['resolvedQuery'].lower(), query.lower())

        self.assertEqual(result['action'], 'input.welcome')
        self.assertEqual(result['fulfillment']['speech'], 'Welcome to our store. Are you looking for something particular today?')

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
        path ='/Users/kianamac/Documents/GitHub/MODAtesting/cases/'
        for i in range(1,12):
            filename = path + 'Case' + str(i) + '.txt'
            filepath = open(filename, 'r')
            file = filepath.readlines()
            filepath.close()

            for line in file:
                query = line

                # Parse the query for the attribute block
                attributeCont = query[query.find("["):query.find("]")+1]
                attr = attributeCont.split("\"")[1]
                query = query.replace(attributeCont, attr)

                #print(query)
                
            response = self.load_text_request_with_quiery(query, entities=entities)
            print(response)
                
                #print(response['result'])
            #f2 = open('/Users/kianamac/output.txt','a+')
            #if(response['result']['metadata']['intentName'] == query):
                #correct_cnt +=1 
            #self.assertTrue(response['result']['metadata']['intentName'] == 'BrandSearchWithoutAttr_SAT')

            #f2.write(response['result']['metadata']['intentName'])
            #f2.write(response['result']['fulfillment']['speech'])
            #f2.close()
        
if __name__ == '__main__':
    unittest.main()
