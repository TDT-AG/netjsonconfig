import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.utils import _TabsMixin


class TestIpsec(unittest.TestCase, _TabsMixin):
    maxDiff = None
    _conn_netjson = {
        "ipsec": {
            "conn": [
                {
                    "esp": [
                        "aes128-sha256-modp3072"
                    ],
                    "lefthostaccess": "yes",
                    "dpddelay": 30,
                    "ike": [
                        "aes128-sha256-modp3072"
                    ],
                    "closeaction": "restart",
                    "dpdaction": "restart",
                    "dpdtimeout": 150,
                    "authby": "psk",
                    "right": "10.0.0.51",
                    "auto": "start",
                    "rightsubnet": "192.168.1.0/24",
                    "keyexchange": "ike",
                    "type": "tunnel",
                    "name": "test-connection",
                    "keyingtries": "3",
                    "leftsubnet": "192.168.0.0/24",
                    "leftfirewall": "yes"
                },
                {
                    "esp": [
                        "aes128-sha256-modp3072"
                    ],
                    "lefthostaccess": "yes",
                    "dpddelay": 30,
                    "ike": [
                        "aes128-sha256-modp3072"
                    ],
                    "closeaction": "restart",
                    "dpdaction": "restart",
                    "dpdtimeout": 150,
                    "authby": "psk",
                    "right": "10.0.0.51",
                    "auto": "start",
                    "rightsubnet": "192.168.1.0/24",
                    "keyexchange": "ike",
                    "type": "tunnel",
                    "name": "test_connection",
                    "keyingtries": "3",
                    "leftsubnet": "192.168.0.0/24",
                    "leftfirewall": "yes"
                }
            ]
        }
    }
    _conn_uci = """package ipsec

config conn 'conn_test-connection'
    option authby 'psk'
    option auto 'start'
    option closeaction 'restart'
    option dpdaction 'restart'
    option dpddelay '30'
    option dpdtimeout '150'
    list esp 'aes128-sha256-modp3072'
    list ike 'aes128-sha256-modp3072'
    option keyexchange 'ike'
    option keyingtries '3'
    option leftfirewall 'yes'
    option lefthostaccess 'yes'
    option leftsubnet '192.168.0.0/24'
    option right '10.0.0.51'
    option rightsubnet '192.168.1.0/24'
    option type 'tunnel'

config conn 'conn_test_connection'
    option authby 'psk'
    option auto 'start'
    option closeaction 'restart'
    option dpdaction 'restart'
    option dpddelay '30'
    option dpdtimeout '150'
    list esp 'aes128-sha256-modp3072'
    list ike 'aes128-sha256-modp3072'
    option keyexchange 'ike'
    option keyingtries '3'
    option leftfirewall 'yes'
    option lefthostaccess 'yes'
    option leftsubnet '192.168.0.0/24'
    option right '10.0.0.51'
    option rightsubnet '192.168.1.0/24'
    option type 'tunnel'
"""

    def test_render_conn(self):
        o = OpenWrt(self._conn_netjson)
        expected = self._tabs(self._conn_uci)
        result = o.render()
        self.assertEqual(result, expected)

    def test_parse_conn(self):
        o = OpenWrt(native=self._conn_uci)
        expected = self._conn_netjson
        result = o.config
        self.assertDictEqual(result, expected)

    _secret_netjson = {
        "ipsec": {
            "secret": [
                {
                    "type": "PSK",
                    "name": "release_test",
                    "pass_secret": "testtest",
                    "id_selector": "*"
                },
                {
                    "type": "PSK",
                    "name": "release-test",
                    "pass_secret": "testtest",
                    "id_selector": "*"
                }
            ]
        }
    }
    _secret_uci = """package ipsec

config secret 'secret_release_test'
    option id_selector '*'
    option pass_secret 'testtest'
    option type 'PSK'

config secret 'secret_release-test'
    option id_selector '*'
    option pass_secret 'testtest'
    option type 'PSK'
"""

    def test_render_secret(self):
        o = OpenWrt(self._secret_netjson)
        expected = self._tabs(self._secret_uci)
        result = o.render()
        self.assertEqual(result, expected)

    def test_parse_secret(self):
        o = OpenWrt(native=self._secret_uci)
        expected = self._secret_netjson
        result = o.config
        self.assertDictEqual(result, expected)

    _both_netjson = {
        "ipsec": {}
    }
    _both_netjson['ipsec']['conn'] = _conn_netjson.get('ipsec').get('conn')
    _both_netjson['ipsec']['secret'] = _secret_netjson\
        .get('ipsec').get('secret')

    _both_uci = """package ipsec

config secret 'secret_release_test'
    option id_selector '*'
    option pass_secret 'testtest'
    option type 'PSK'

config secret 'secret_release-test'
    option id_selector '*'
    option pass_secret 'testtest'
    option type 'PSK'

config conn 'conn_test-connection'
    option authby 'psk'
    option auto 'start'
    option closeaction 'restart'
    option dpdaction 'restart'
    option dpddelay '30'
    option dpdtimeout '150'
    list esp 'aes128-sha256-modp3072'
    list ike 'aes128-sha256-modp3072'
    option keyexchange 'ike'
    option keyingtries '3'
    option leftfirewall 'yes'
    option lefthostaccess 'yes'
    option leftsubnet '192.168.0.0/24'
    option right '10.0.0.51'
    option rightsubnet '192.168.1.0/24'
    option type 'tunnel'

config conn 'conn_test_connection'
    option authby 'psk'
    option auto 'start'
    option closeaction 'restart'
    option dpdaction 'restart'
    option dpddelay '30'
    option dpdtimeout '150'
    list esp 'aes128-sha256-modp3072'
    list ike 'aes128-sha256-modp3072'
    option keyexchange 'ike'
    option keyingtries '3'
    option leftfirewall 'yes'
    option lefthostaccess 'yes'
    option leftsubnet '192.168.0.0/24'
    option right '10.0.0.51'
    option rightsubnet '192.168.1.0/24'
    option type 'tunnel'
"""

    def test_render_both(self):
        o = OpenWrt(self._both_netjson)
        expected = self._tabs(self._both_uci)
        result = o.render()
        self.assertEqual(result, expected)

    def test_parse_both(self):
        o = OpenWrt(native=self._both_uci)
        expected = self._both_netjson
        result = o.config
        self.assertDictEqual(result, expected)
