import requests
import xmltodict
from lxml import etree
from io import BytesIO
from random import randint
from flask import Markup


starboard_url = "http://chat.stackoverflow.com/feeds/rooms/starred/6"
tag_prefix = "{http://www.w3.org/2005/Atom}"


def all_starred():
    """ returns all the starred messages as a list of OrderedDicts """
    xml_iterator = _tree_iter()
    starred = []
    for element in xml_iterator:
        starred.append( xmltodict.parse(etree.tostring(element, method="xml"))['entry'] )
    return starred


def _tree_iter():
    """ make an iterator for every starred message """
    xml = requests.get(starboard_url)
    parser = etree.XMLParser(ns_clean=True)
    tree = etree.parse(BytesIO(xml.content), parser)
    root_tag = "{0}{1}".format(tag_prefix, "entry")
    return tree.iter(root_tag)


def get_random_starred():
    """ returns a random message from the starboard """
    starred = all_starred()
    rand = starred[randint(0, len(starred) - 1)]

    # message for future implementation:
    # you may want to add a link to the user's profile
    # this can be accessed in the random item at:
    # rand['author']['uri']
    html = Markup("""
        <blockquote>
            <p>{0}</p>
            <footer><a href="{1}"><cite title="">{2}</cite></a></footer>
        </blockquote>
    """.format(rand['summary']['#text'], rand['author']['uri'], rand['author']['name']))
    return html


def init_app(app):
    """ equip the jinja2 context processor """
    @app.context_processor
    def random_starred():
        return dict(random_starred=get_random_starred)
