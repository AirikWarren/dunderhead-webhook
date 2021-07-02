from dataclasses import dataclass
from typing import List, Tuple, Union
from datetime import datetime
import os
import xml.etree.ElementTree as ET


@dataclass
class RssItem:
    title : str
    description : str

@dataclass
class RssChannel:
    title : str
    description : str
    items : List[RssItem]


def extract_rss_channel_from_xml(xml_filepath : str, properties_of_interest : Tuple[str]) -> RssChannel:
    '''accepts a path to a .xml file conforming to some version of the rss standard and a Tuple of strings defining
    rss properties to be stored inside of the RssChannel object and the RssItem(s) objects it contains. 
    reference rss standard here : https://www.w3schools.com/xml/xml_rss.asp'''
    tree = ET.parse(xml_filepath)
    root = tree.getroot()

    channel = root.find('rss/channel')
    title, description = map(lambda x: channel.find(x).text.strip(), properties_of_interest)
    rss_items = list() # gets populated in the loop below

    for child in root.findall('rss/channel/item'):
        t,d = map(lambda x: child.find(x).text.strip(), properties_of_interest)
        rss_items.append(RssItem(title=t, description=d))
    
    return RssChannel(title=title, description=description, items=rss_items)

def extract_dates_from_channel(rss_channel:RssChannel, use_datetimes=True) -> Union[List[datetime], List[str]]:
    date_list = list()
    for item in rss_channel.items:
        full_desc = item.description
        full_desc = full_desc[full_desc.find('Thursday,'):]
        full_desc = full_desc[:full_desc.find('PM')+2].strip()
        date_list.append(full_desc)
    return [
    dt.replace(year=2021) for dt in 
        [datetime.strptime(x,"%A, %B %d at %H:%M %p") for x in date_list]
    ] if use_datetimes else date_list

if __name__ == '__main__':
    # config variables
    xml_directory_path = 'rss-xml-files'
    xml_filepaths = list()
    required_rss_properties = ('title', 'description')

    # setting up the directory if it's not alreaady
    try:
        os.mkdir(xml_directory_path)
    except FileExistsError:
        xml_filepaths = os.listdir(xml_directory_path)
        for i,filepath in enumerate(xml_filepaths):
            xml_filepaths[i] = f"{xml_directory_path}/{filepath}"

    # list of RssChannel objects
    rss_channels = [extract_rss_channel_from_xml(x, required_rss_properties) for x in xml_filepaths]
    print(f"\n\nif you type 'interact' from the pdb you can enter an interactive shell with all of the variables in this program in scope\n\n")
