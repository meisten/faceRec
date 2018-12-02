import json
import sys
import numpy as np


def findPeople(features_arr, positions, thres=0.6, percent_thres=70):
    """
    :param percent_thres: a
    :param features_arr: a list of 128d Features of all faces on screen
    :param positions: a list of face position types of all faces on screen
    :param thres: distance threshold
    :return: person name and percentage
    """
    f = open('./services/storage.json', 'r')
    data_set = json.loads(f.read())
    returnRes = []
    for (i, features_128D) in enumerate(features_arr):
        result = ""
        smallest = sys.maxsize
        for person in data_set.keys():
            person_data = data_set[person][positions[i]]
            for data in person_data:
                distance = np.sqrt(np.sum(np.square(data - features_128D)))
                if distance < smallest:
                    smallest = distance
                    result = person
        percentage = min(100, 100 * thres / smallest)
        if percentage <= percent_thres:
            result = ""
        returnRes.append((result, percentage))
    return returnRes