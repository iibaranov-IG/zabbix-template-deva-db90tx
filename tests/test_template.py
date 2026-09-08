import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = ROOT / "zabbix_template_devabroadcast_db90tx.json"


class TemplateIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
        cls.template = cls.document["zabbix_export"]["templates"][0]
        cls.discovery = cls.template["discovery_rules"][0]
        cls.prototypes = {
            prototype["key"]: prototype
            for prototype in cls.discovery["item_prototypes"]
        }

    def test_stream_down_recovers_on_an_active_sample(self):
        trigger = self.prototypes["stream.active[{#SNMPINDEX}]"][
            "trigger_prototypes"
        ][0]
        self.assertEqual(
            trigger["expression"],
            "max(/DEVABroadcast DB90TX by SNMP/stream.active[{#SNMPINDEX}],3m)=0",
        )
        self.assertEqual(
            trigger["recovery_expression"],
            "last(/DEVABroadcast DB90TX by SNMP/stream.active[{#SNMPINDEX}])=1",
        )

    def test_reconnect_event_recovers_after_the_counter_advances(self):
        trigger = self.prototypes["stream.clientTIME[{#SNMPINDEX}]"][
            "trigger_prototypes"
        ][0]
        self.assertEqual(
            trigger["expression"],
            "change(/DEVABroadcast DB90TX by SNMP/stream.clientTIME[{#SNMPINDEX}]) < 0",
        )
        self.assertEqual(
            trigger["recovery_expression"],
            "last(/DEVABroadcast DB90TX by SNMP/stream.clientTIME[{#SNMPINDEX}]) > 0",
        )

    def test_trigger_names_do_not_reference_a_second_expression_item(self):
        names = []
        for prototype in self.discovery["item_prototypes"]:
            names.extend(
                trigger["name"]
                for trigger in prototype.get("trigger_prototypes", [])
            )
        self.assertNotIn("{ITEM.LASTVALUE2}", "\n".join(names))

    def test_template_does_not_ship_a_default_snmp_community(self):
        macros = {macro["macro"] for macro in self.template.get("macros", [])}
        self.assertNotIn("{$SNMP_COMMUNITY}", macros)

    def test_all_export_uuids_are_unique(self):
        uuids = []

        def collect(value):
            if isinstance(value, dict):
                if "uuid" in value:
                    uuids.append(value["uuid"])
                for child in value.values():
                    collect(child)
            elif isinstance(value, list):
                for child in value:
                    collect(child)

        collect(self.document)
        self.assertEqual(len(uuids), len(set(uuids)))


if __name__ == "__main__":
    unittest.main()
