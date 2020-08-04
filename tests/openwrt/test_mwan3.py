import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.utils import _TabsMixin


class TestMwan3(unittest.TestCase, _TabsMixin):
    maxDiff = None

    _interface_netjson = {
        "mwan3": {
            "interfaces": [
                {
                    "name": "wan",
                    "enabled": False,
                    "track_method": "ping",
                    "track_ip": [
                        "192.0.0.1",
                        "192.0.0.2"
                    ],
                    "reliability": 1,
                    "count": 1,
                    "timeout": 4,
                    "interval": 10,
                    "failure_interval": 3,
                    "recovery_interval": 3,
                    "keep_failure_interval": False,
                    "up": 5,
                    "down": 5,
                    "family": "ipv4",
                    "max_ttl": 60,
                    "initial_state": "online",
                    "size": 56,
                    "flush_conntrack": "never"
                },
                {
                    "name": "wan_1",
                    "enabled": False,
                    "track_method": "ping",
                    "track_ip": [
                        "192.0.0.3",
                        "192.0.0.4"
                    ],
                    "reliability": 1,
                    "count": 1,
                    "timeout": 4,
                    "interval": 10,
                    "failure_interval": 3,
                    "recovery_interval": 3,
                    "keep_failure_interval": False,
                    "up": 5,
                    "down": 5,
                    "family": "ipv4",
                    "max_ttl": 60,
                    "initial_state": "online",
                    "size": 56,
                    "flush_conntrack": "never"
                }
            ]
        }
    }

    _interface_uci = """package mwan3

config interface 'interface_wan'
    option count '1'
    option down '5'
    option enabled '0'
    option failure_interval '3'
    option family 'ipv4'
    option flush_conntrack 'never'
    option initial_state 'online'
    option interval '10'
    option keep_failure_interval '0'
    option max_ttl '60'
    option name 'wan'
    option recovery_interval '3'
    option reliability '1'
    option size '56'
    option timeout '4'
    list track_ip '192.0.0.1'
    list track_ip '192.0.0.2'
    option track_method 'ping'
    option up '5'

config interface 'interface_wan_1'
    option count '1'
    option down '5'
    option enabled '0'
    option failure_interval '3'
    option family 'ipv4'
    option flush_conntrack 'never'
    option initial_state 'online'
    option interval '10'
    option keep_failure_interval '0'
    option max_ttl '60'
    option name 'wan_1'
    option recovery_interval '3'
    option reliability '1'
    option size '56'
    option timeout '4'
    list track_ip '192.0.0.3'
    list track_ip '192.0.0.4'
    option track_method 'ping'
    option up '5'
"""

    def test_render_interface(self):
        o = OpenWrt(self._interface_netjson)
        expected = self._tabs(self._interface_uci)
        result = o.render()
        self.assertEqual(result, expected)

    def test_parse_interface(self):
        o = OpenWrt(native=self._interface_uci)
        expected = self._interface_netjson
        result = o.config
        self.assertDictEqual(result, expected)
