import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.exceptions import ValidationError
from netjsonconfig.utils import _TabsMixin


class TestMultisim(unittest.TestCase, _TabsMixin):
    _multisim_netjson = {
        "multisim": [
            {
                "pincode": 25482,
                "apn": "test1.tdt.de",
                "plmn": 4711,
                "name": "Simcard1"
            },
            {
                "auth": "chap",
                "pincode": 86734,
                "apn": "test2.tdt.de",
                "username": "hans",
                "password": "geheim",
                "modes": "lte,umts",
                "plmn": 815,
                "name": "Simcard2"
            }
        ]
    }
    _multisim_uci = """package multisim

config multisim 'Simcard1'
    option apn 'test1.tdt.de'
    option pincode '25482'
    option plmn '4711'

config multisim 'Simcard2'
    option apn 'test2.tdt.de'
    option auth 'chap'
    option modes 'lte,umts'
    option password 'geheim'
    option pincode '86734'
    option plmn '815'
    option username 'hans'
"""

    def test_render_multisim(self):
        o = OpenWrt(self._multisim_netjson)
        expected = self._tabs(self._multisim_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_multisim(self):
        o = OpenWrt(native=(self._multisim_uci))
        self.assertEqual(o.config, self._multisim_netjson)

    def test_multisim_schema_validation(self):
        o = OpenWrt({"multisim": [{"invalid": True}]})
        with self.assertRaises(ValidationError):
            o.validate()
