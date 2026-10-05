"""Prepare a copied firewalld zone before comparing it with the destination."""

from xml.dom import Node, minidom
from xml.parsers.expat import ExpatError

from ansible.errors import AnsibleFilterError


def rhel8stig_firewalld_zone(content, name):
    try:
        document = minidom.parseString(content)
    except (ExpatError, TypeError, ValueError) as error:
        raise AnsibleFilterError("Invalid firewalld zone XML: %s" % error)

    zone = document.documentElement
    if zone.tagName != "zone" or document.doctype is not None:
        raise AnsibleFilterError("Expected a firewalld zone without a document type")

    zone.setAttribute("target", "DROP")
    short = next(
        (child for child in zone.childNodes
         if child.nodeType == Node.ELEMENT_NODE and child.tagName == "short"),
        None,
    )
    if short is None:
        short = document.createElement("short")
        zone.appendChild(short)
    for child in list(short.childNodes):
        short.removeChild(child)
    short.appendChild(document.createTextNode(name))

    return '<?xml version="1.0" encoding="utf-8"?>\n' + "".join(
        child.toxml() for child in document.childNodes
    ) + "\n"


class FilterModule:
    def filters(self):
        return {"rhel8stig_firewalld_zone": rhel8stig_firewalld_zone}
