import sys
import os
from rtree import index
from flask import Flask
from flask import request
from flask import jsonify
from json import loads
from flask_cors import CORS
import glob
import json
import math
from rtree import index
import random
import networkx as nx
import matplotlib.pyplot as plt


pathRoad ='assignments\\A04\\assets\\json\\ne_10m_populated_places\\populatedplacesgeo.geojson'
crossed = 'assignments\\A04\\assets\\json\\ne_10m_roads_north_america\\roadwork.geojson'

def isJson(data):
    """ Helper method to test if val can be json
        without throwing an actual error.
    """
    try:
        json.loads(data)
        return True
    except ValueError:
        return False

def load_data(path):
    """ Given a path, load the file and handle it based on its
        extension type. So far I have code for json and csv files.
    """
    _, ftype = os.path.splitext(path)   # get fname (_), and extenstion (ftype)

    if os.path.isfile(path):            # is it a real file?
        with open(path,'r', encoding='utf-8') as f:

            if ftype == ".json" or ftype == ".geojson":  # handle json
                data = f.read()
                if isJson(data):
                    return json.loads(data)

            elif ftype == ".csv":       # handle csv with csv reader
                with open(path, newline='') as csvfile:
                    data = csv.DictReader(csvfile)
def deletePath(path):
    featuretype =  ["SCALERANK","NATSCALE","LABELRANK","NAMEPAR","NAMEALT","name_nl"
 ,"DIFFASCII" ,"NAMEASCII" ,"ADM0CAP" ,"CAPIN" ,"WORLDCITY" ,"MEGACITY" ,"SOV0NAME" ,"SOV_A3" ,"ADM0NAME" ,"ADM0_A3" ,"ADM1NAME" ,"ISO_A2" ,"NOTE" ,"LATITUDE" ,"LONGITUDE" ,"CHANGED" ,"NAMEDIFF" ,"DIFFNOTE" ,"POP_MAX" ,"POP_MIN" ,"POP_OTHER" ,"RANK_MAX" ,"RANK_MIN" ,"GEONAMEID" ,"MEGANAME" ,"LS_NAME" ,"LS_MATCH" ,"CHECKME" ,"MAX_POP10" ,"MAX_POP20" ,"MAX_POP50" ,"MAX_POP300" ,"MAX_POP310" ,"MAX_NATSCA" ,"MIN_AREAKM" ,"MAX_AREAKM" ,"MIN_AREAMI" ,"MAX_AREAMI" ,"MIN_PERKM" ,"MAX_PERKM" ,"MIN_PERMI" ,"MAX_PERMI" ,"MIN_BBXMIN" ,"MAX_BBXMIN" ,"MIN_BBXMAX" ,"MAX_BBXMAX" ,"MIN_BBYMIN" ,"MAX_BBYMIN" ,"MIN_BBYMAX" ,"MAX_BBYMAX" ,"MEAN_BBXC" ,"MEAN_BBYC" ,"COMPARE" ,"GN_ASCII" ,"FEATURE_CL" ,"FEATURE_CO" ,"ADMIN1_COD" ,"GN_POP" ,"ELEVATION" ,"GTOPO30" ,"TIMEZONE" ,"GEONAMESNO" ,"UN_FID" ,"UN_ADM0" ,"UN_LAT" ,"UN_LONG" ,"POP1950" ,"POP1955" ,"POP1960" ,"POP1965" ,"POP1970" ,"POP1975" ,"POP1980" ,"POP1985" ,"POP1990" ,"POP1995" ,"POP2000" ,"POP2005" ,"POP2010" ,"POP2015" ,"POP2020" ,"POP2025" ,"POP2050" ,"CITYALT" ,"min_zoom" ,"wikidataid" ,"wof_id" ,"CAPALT" ,"name_en" ,"name_de" ,"name_es" ,"name_fr" ,"name_pt" ,"name_ru" ,"name_zh" ,"label" ,"name_ar" ,"name_bn" ,"name_el" ,"name_hi" ,"name_hu"  ,"name_id" ,"name_it" ,"name_ja"  ,"name_ko"  ,"name_pl" ,"name_sv"  ,"name_tr" ,"name_vi" ,"wdid_score"]  

    data = load_data(path)
    feature = data['features']
   
    for row in feature:
        rowprop = row["properties"]
        res = deletefrondic(featuretype, rowprop)
        rowprop = res
    
        
       
    with open('poulatedcitiesgeo.geojson', 'w') as outfile:
        outfile.write(json.dumps(data,indent = 1))

def truncate(number, decimals=0):
    """
    Returns a value truncated to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor
        
def deletefrondic(entries, the_dict):
    for key in entries:
        if key  in the_dict:
            del the_dict[key]
    return the_dict
def decmalplace(path):
    data = load_data(path)
    feature = data['features']
    for row in feature:
        resultlist= row["geometry"]["coordinates"]
        needed = resultlist[0]
        for subrow in needed:
            for i in range(0,2):
                subrow[i] = truncate(subrow[i], 6)
        listed = needed
        """ resultlist.clear()
        resultlist.append(listed)
        listed.clear() """
    with open('newroad7.geojson', 'w') as outfile:
        outfile.write(json.dumps(data,indent = 1))


    


if __name__ == '__main__':
    decmalplace(crossed)
    