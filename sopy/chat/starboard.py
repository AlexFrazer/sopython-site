import requests
from xml.etree import ElementTree
import xmltodict

starboard_url = "http://chat.stackoverflow.com/feeds/rooms/starred/6"
tag_prefix = "{http://www.w3.org/2005/Atom}"

def get_all():
    """ returns all the starred messages as a list of OrderedDicts """
    xml_iterator = _tree_iter()
    board = [convert_xml_to_dict(e) for e in xml_iterator]
    return board


def _tree_iter():
    """ make an iterator for every starred message """
    starboard_xml = requests.get(starboard_url).text
    et = ElementTree.fromstring(starboard_xml)
    root_tag = "{0}{1}".format(tag_prefix, "entry")
    return et.iter(root_tag)


def convert_xml_to_dict(element):
    """ takes an element in the etree from the starboard and converts it to list
    :param element: a star element in the xml tree
    """
    xml_string = ElementTree.tostring(element, encoding='utf-8', method='xml')
    todict = xmltodict.parse(xml_string)
    return todict
