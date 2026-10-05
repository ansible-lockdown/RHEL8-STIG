"""Unit tests for the in-memory firewalld zone transformation."""

import sys
import unittest
from pathlib import Path
from xml.etree import ElementTree

from ansible.errors import AnsibleFilterError

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "filter_plugins"))
from firewalld_zone import rhel8stig_firewalld_zone  # noqa: E402


class FirewalldZoneTests(unittest.TestCase):
    def test_preserves_rules_and_updates_identity(self):
        source = """<?xml version="1.0" encoding="utf-8"?>
<!-- preserve this comment -->
<zone version="1.0" target="ACCEPT">
  <short>Public</short>
  <description>Keep all configured rules</description>
  <!-- preserve the rule comment too -->
  <interface name="eth0"/>
  <source address="192.0.2.0/24"/>
  <service name="ssh"/>
  <port port="8443" protocol="tcp"/>
  <protocol value="icmp"/>
  <masquerade/>
  <forward-port port="8080" protocol="tcp" to-port="80"/>
  <rule family="ipv4"><source address="198.51.100.0/24"/><accept/></rule>
</zone>
"""
        result = rhel8stig_firewalld_zone(source, "new_fw_zone")
        expected = ElementTree.fromstring(source)
        expected.set("target", "DROP")
        expected.find("short").text = "new_fw_zone"
        actual = ElementTree.fromstring(result)
        self.assertEqual(ElementTree.tostring(actual), ElementTree.tostring(expected))
        self.assertIn("<!-- preserve this comment -->", result)
        self.assertIn("<!-- preserve the rule comment too -->", result)

    def test_bare_zone(self):
        result = ElementTree.fromstring(rhel8stig_firewalld_zone(
            "<zone><short>Public</short><service name='ssh'/></zone>", "custom"))
        self.assertEqual(result.get("target"), "DROP")
        self.assertEqual(result.findtext("short"), "custom")
        self.assertEqual(result.find("service").get("name"), "ssh")

    def test_adds_missing_short_name(self):
        result = ElementTree.fromstring(rhel8stig_firewalld_zone("<zone/>", "custom"))
        self.assertEqual(result.findtext("short"), "custom")
        self.assertEqual(result.get("target"), "DROP")

    def test_render_is_stable_including_when_source_is_destination(self):
        source = "<zone><short>Public</short><service name='ssh'/></zone>"
        first = rhel8stig_firewalld_zone(source, "custom")
        self.assertEqual(first, rhel8stig_firewalld_zone(source, "custom"))
        self.assertEqual(first, rhel8stig_firewalld_zone(first, "custom"))

    def test_source_changes_propagate(self):
        first = rhel8stig_firewalld_zone("<zone><service name='ssh'/></zone>", "custom")
        second = rhel8stig_firewalld_zone("<zone><service name='https'/></zone>", "custom")
        self.assertNotEqual(first, second)
        self.assertEqual(ElementTree.fromstring(second).find("service").get("name"), "https")

    def test_escapes_short_name_and_preserves_unicode(self):
        result = rhel8stig_firewalld_zone(
            "<zone><description>Caf\u00e9 &amp; SSH</description></zone>", "A & B")
        parsed = ElementTree.fromstring(result)
        self.assertEqual(parsed.findtext("description"), "Caf\u00e9 & SSH")
        self.assertEqual(parsed.findtext("short"), "A & B")

    def test_rejects_malformed_xml(self):
        with self.assertRaises(AnsibleFilterError):
            rhel8stig_firewalld_zone("<zone>", "custom")

    def test_rejects_wrong_root(self):
        with self.assertRaises(AnsibleFilterError):
            rhel8stig_firewalld_zone("<service/>", "custom")

    def test_rejects_document_types(self):
        with self.assertRaises(AnsibleFilterError):
            rhel8stig_firewalld_zone("<!DOCTYPE zone><zone/>", "custom")


if __name__ == "__main__":
    unittest.main()
