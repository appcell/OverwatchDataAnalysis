import os
import sys
import zipfile
import json

sys.path.append('../utils')
from utils import stats

class SingleMatchStats:
    """Class of a SingleMatchStats object.

    Retrieves and stores all stats listed in 
    competitive_stats_rating_list.xlsx.

    Attributes:
        data_metainfo: Raw data in metainfo.json in dict format
        data_frames: Raw data in frames.json in dict format
        data_sheet1: Raw data in data_sheet1.json in dict format
        data_sheet1: Raw data in data_sheet2.json in dict format
        data_sheet1: Raw data in data_sheet3.json in dict format
        elims: List of all eliminations in the game, with 'time' expressed in
               seconds, not in hh:mm:ss
        teamfight_separations: List of teamfight separation points
    """

    def __init__(self, zip_path):
        """Parse JSON zip pack and return corresponding dicts

        Author:
            Appcell

        Args:
            zip_path: path of the .zip file needs to be analyzed

        Returns:
            None

        """
        archive = zipfile.ZipFile(zip_path, 'r')
        self.data_metainfo = json.loads(archive.read('metainfo.json'))
        self.data_frames = json.loads(archive.read('frames.json'))
        self.data_sheet1 = json.loads(archive.read('data_sheet1.json'))
        self.data_sheet2 = json.loads(archive.read('data_sheet1.json'))
        self.data_sheet3 = json.loads(archive.read('data_sheet1.json'))
        self.elims = self.get_eliminations()
        self.teamfight_separations = self.get_teamfight_separations()

    def get_eliminations(self, start_time=0, end_time=0):
        """Get all eliminatins in a given time range.

        If start_time == 0 and end_time == 0, return full elim list.

        Author:
            Appcell

        Args:
            start_time: start of the time range given in seconds
            end_time: end of the time range given in seconds

        Returns:
            A list of all eliminatins in a given time range.
        """
        res = []
        if end_time == 0 and start_time == 0:
            for event in self.data_sheet1:
                if event['action'] == 'Eliminate':
                    time_arr = event['time'].split(':')
                    curr_time = stats.hms_to_seconds(time_arr[0],
                        time_arr[1], time_arr[2])
                    event['time'] = curr_time
                    res.append(event)
        else:
            for event in self.data_sheet1:
                time_arr = event['time'].split(':')
                curr_time = stats.hms_to_seconds(time_arr[0],
                    time_arr[1], time_arr[2])
                if curr_time >= start_time and curr_time >= end_time \
                and self.event['action'] == 'Eliminate':
                    event['time'] = curr_time
                    res.append(event)
        return res

    def get_eliminations_incremented(self, data, start_time, end_time):
        """Append eliminations in given time range onto existed array
        
        Author:
            Appcell

        Args:
            data: list of given elimination data
            start_time: start of the time range given in seconds
            end_time: end of the time range given in seconds

        Returns:
            A list of all eliminatins in a given time range appended to original list.
        """
        return data.append(self.get_eliminations(start_time, end_time))


    def get_teamfight_index(self, time):
        """Get index of team-fight happening at given timestamp.
        
        A temporary standard for separating team-fights:

        Author:
            ForYou

        Args:
            time: current time in seconds

        Returns:
            Index of team-fight happening at 'time'.
        """
        if len(self.teamfight_separations) <= 1:
            return 1
        else:
            for ind_timestamp in range(1, len(self.teamfight_separations)):
                if time < self.teamfight_separations[ind_timestamp] \
                and time > self.teamfight_separations[ind_timestamp - 1]:
                    return ind_timestamp
            if time > self.teamfight_separations[-1]:
                return len(self.teamfight_separations) + 1
        

    def get_teamfight_separations(self):
        """Get a list of all separation timestamps between each teamfight.
        
        Author:
            Appcell

        Args:
            None

        Returns:
            A list of all timestamps marking separations between each teamfight.
        """
        res = [0]
        if len(self.elims) > 1:
            for ind_elim in range(1, len(self.elims)):
                if self.elims[ind_elim]['time'] \
                - self.elims[ind_elim - 1]['time'] > 14:
                    res.append((self.elims[ind_elim]['time'] \
                        + self.elims[ind_elim - 1]['time']) / 2)
        return res


