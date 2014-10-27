import requests
import xmltodict
from lxml import etree
from io import BytesIO
from random import randint


starboard_url = "http://chat.stackoverflow.com/feeds/rooms/starred/6"
tag_prefix = "{http://www.w3.org/2005/Atom}"


def get_entry(index=0, random=False):
    """ returns a starred entry """
    d = as_dict()
    if random:
        return d[randint(0, len(d))]
    return d[index]


def as_dict():
    """ returns all the starred messages as a list of OrderedDicts """
    xml_iterator = _tree_iter()
    entry_list = []
    for element in xml_iterator:
        entry_list.append(xmltodict.parse(etree.tostring(element, method="xml")))
    return entry_list


def _tree_iter():
    """ make an iterator for every starred message """
    xml = requests.get(starboard_url)
    parser = etree.XMLParser(ns_clean=True)
    tree = etree.parse(BytesIO(xml.content), parser)
    root_tag = "{0}{1}".format(tag_prefix, "entry")
    return tree.iter(root_tag)
