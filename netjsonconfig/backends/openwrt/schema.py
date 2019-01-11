"""
OpenWrt specific JSON-Schema definition
"""
from ...schema import schema as default_schema
from ...utils import merge_config
from ..openvpn.schema import base_openvpn_schema
from .timezones import timezones

default_radio_driver = "mac80211"


schema = merge_config(default_schema, {
    "definitions": {
        "interface_settings": {
            "properties": {
                "network": {
                    "type": "string",
                    "description": "logical interface name in UCI (OpenWRT configuration format), "
                                   "will be automatically generated if left blank",
                    "maxLength": 15,
                    "pattern": "^[a-zA-z0-9_\\.\\-]*$",
                    "propertyOrder": 7
                }
            }
        },
        "wireless_interface": {
            "properties": {
                "wireless": {
                    "properties": {
                        "network": {
                            "type": "array",
                            "title": "Attached Networks",
                            "description": "override OpenWRT \"network\" config option of of wifi-iface "
                                           "directive; will be automatically determined if left blank",
                            "uniqueItems": True,
                            "additionalItems": True,
                            "items": {
                                "title": "network",
                                "type": "string",
                                "$ref": "#/definitions/interface_settings/properties/network"
                            },
                            "propertyOrder": 19
                        }
                    }
                }
            }
        },
        "ap_wireless_settings": {
            "allOf": [
                {
                    "properties": {
                        "wmm": {
                            "type": "boolean",
                            "title": "WMM (802.11e)",
                            "description": "enables WMM (802.11e) support; "
                                           "required for 802.11n support",
                            "default": True,
                            "format": "checkbox",
                            "propertyOrder": 8,
                        },
                        "isolate": {
                            "type": "boolean",
                            "title": "isolate clients",
                            "description": "isolate wireless clients from one another",
                            "default": False,
                            "format": "checkbox",
                            "propertyOrder": 9,
                        },
                        "macfilter": {
                            "type": "string",
                            "title": "MAC Filter",
                            "description": "specifies the mac filter policy, \"disable\" to disable "
                                           "the filter, \"allow\" to treat it as whitelist or "
                                           "\"deny\" to treat it as blacklist",
                            "enum": [
                                "disable",
                                "allow",
                                "deny",
                            ],
                            "default": "disable",
                            "propertyOrder": 15,
                        },
                        "maclist": {
                            "type": "array",
                            "title": "MAC List",
                            "description": "mac addresses that will be filtered according to the policy "
                                           "specified in the \"macfilter\" option",
                            "propertyOrder": 16,
                            "items": {
                                "type": "string",
                                "title": "MAC address",
                                "pattern": "^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$",
                                "minLength": 17,
                                "maxLength": 17,
                            }
                        }
                    }
                }
            ]
        },
        "bridge_interface": {
            "allOf": [
                {
                    "properties": {
                        "igmp_snooping": {
                            "type": "boolean",
                            "title": "IGMP snooping",
                            "description": "sets the \"multicast_snooping\" kernel setting for a bridge",
                            "default": True,
                            "format": "checkbox",
                            "propertyOrder": 4,
                        }
                    }
                }
            ]
        },
        "base_radio_settings": {
            "properties": {
                "driver": {
                    "type": "string",
                    "enum": [
                        "mac80211",
                        "madwifi",
                        "ath5k",
                        "ath9k",
                        "broadcom"
                    ],
                    "default": default_radio_driver,
                    "propertyOrder": 2,
                }
            }
        },
        "radio_hwmode_11g": {
            "properties": {
                "hwmode": {
                    "type": "string",
                    "title": "hardware mode",
                    "readOnly": True,
                    "propertyOrder": 8,
                    "default": "11g",
                    "enum": ["11g"],
                }
            }
        },
        "radio_hwmode_11a": {
            "properties": {
                "hwmode": {
                    "type": "string",
                    "title": "hardware mode",
                    "readOnly": True,
                    "propertyOrder": 8,
                    "default": "11a",
                    "enum": ["11a"],
                }
            }
        },
        "radio_80211gn_settings": {
            "allOf": [{"$ref": "#/definitions/radio_hwmode_11g"}]
        },
        "radio_80211an_settings": {
            "allOf": [{"$ref": "#/definitions/radio_hwmode_11a"}]
        },
        "radio_80211ac_2ghz_settings": {
            "allOf": [{"$ref": "#/definitions/radio_hwmode_11g"}]
        },
        "radio_80211ac_5ghz_settings": {
            "allOf": [{"$ref": "#/definitions/radio_hwmode_11a"}]
        },
        "firewall_policy": {
            "type": "string",
            "enum": ["ACCEPT", "REJECT", "DROP"],
            "options": {
                "enum_titles": [
                    "Accept", "Reject", "Drop"]
            },
            "default": "REJECT"
        },
        "zone_policy": {
            "type": "string",
            "enum": ["ACCEPT", "REJECT", "DROP"],
            "options": {
                "enum_titles": [
                    "Accept", "Reject", "Drop"]
            },
            "default": "DROP"
        },
        "rule_policy": {
            "type": "string",
            "enum": ["ACCEPT", "REJECT", "DROP", "MARK", "NOTRACK"],
            "options": {
                "enum_titles": [
                    "Accept", "Reject", "Drop", "Mark", "Notrack"]
            },
            "default": "DROP"
        },
    },
    "properties": {
        "general": {
            "properties": {
                "timezone": {
                    "enum": list(timezones.keys()),
                    "default": "UTC",
                }
            }
        },
        "routes": {
            "items": {
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": [
                            "unicast",
                            "local",
                            "broadcast",
                            "multicast",
                            "unreachable",
                            "prohibit",
                            "blackhole",
                            "anycast"
                        ],
                        "default": "unicast",
                        "propertyOrder": 0,
                    },
                    "mtu": {
                        "type": "string",
                        "title": "MTU",
                        "propertyOrder": 6,
                        "pattern": "^[0-9]*$",
                    },
                    "table": {
                        "type": "string",
                        "propertyOrder": 7,
                        "pattern": "^[0-9]*$",
                    },
                    "onlink": {
                        "type": "boolean",
                        "default": False,
                        "format": "checkbox",
                        "propertyOrder": 8,
                    }
                }
            }
        },
        "ip_rules": {
            "type": "array",
            "title": "Policy routing",
            "uniqueItems": True,
            "additionalItems": True,
            "propertyOrder": 7,
            "items": {
                "type": "object",
                "title": "IP rule",
                "additionalProperties": True,
                "properties": {
                    "in": {
                        "type": "string",
                        "title": "incoming interface",
                        "propertyOrder": 1,
                    },
                    "out": {
                        "type": "string",
                        "title": "outgoing interface",
                        "propertyOrder": 2,
                    },
                    "src": {
                        "type": "string",
                        "title": "source subnet",
                        "description": "(CIDR notation)",
                        "propertyOrder": 3,
                    },
                    "dest": {
                        "type": "string",
                        "title": "destination subnet",
                        "description": "(CIDR notation)",
                        "propertyOrder": 4,
                    },
                    "tos": {
                        "type": "integer",
                        "title": "TOS",
                        "description": "TOS value to match in IP headers",
                        "propertyOrder": 5,
                    },
                    "mark": {
                        "type": "string",
                        "description": "TOS value to match in IP headers",
                        "propertyOrder": 6,
                    },
                    "lookup": {
                        "type": "string",
                        "description": "routing table ID or symbolic link alias",
                        "propertyOrder": 7,
                    },
                    "action": {
                        "type": "string",
                        "enum": [
                            "prohibit",
                            "unreachable",
                            "blackhole",
                            "throw"
                        ],
                        "propertyOrder": 8,
                    },
                    "goto": {
                        "type": "integer",
                        "propertyOrder": 9,
                    },
                    "invert": {
                        "type": "boolean",
                        "default": False,
                        "format": "checkbox",
                        "propertyOrder": 10,
                    }
                }
            }
        },
        "ntp": {
            "type": "object",
            "title": "NTP Settings",
            "additionalProperties": True,
            "propertyOrder": 8,
            "properties": {
                "enabled": {
                    "type": "boolean",
                    "title": "enable NTP client",
                    "default": True,
                    "format": "checkbox",
                    "propertyOrder": 1,
                },
                "enable_server": {
                    "type": "boolean",
                    "title": "enable NTP server",
                    "default": False,
                    "format": "checkbox",
                    "propertyOrder": 2,
                },
                "server": {
                    "title": "NTP Servers",
                    "description": "NTP server candidates",
                    "type": "array",
                    "uniqueItems": True,
                    "additionalItems": True,
                    "propertyOrder": 3,
                    "items": {
                        "title": "NTP server",
                        "type": "string",
                        "format": "hostname"
                    },
                    "default": [
                        "0.openwrt.pool.ntp.org",
                        "1.openwrt.pool.ntp.org",
                        "2.openwrt.pool.ntp.org",
                        "3.openwrt.pool.ntp.org",
                    ]
                }
            }
        },
        "switch": {
            "type": "array",
            "uniqueItems": True,
            "additionalItems": True,
            "title": "Programmable Switch",
            "propertyOrder": 9,
            "items": {
                "title": "Switch",
                "type": "object",
                "additionalProperties": True,
                "required": [
                    "name",
                    "reset",
                    "enable_vlan",
                    "vlan"
                ],
                "properties": {
                    "name": {
                        "type": "string",
                        "propertyOrder": 1,
                    },
                    "reset": {
                        "type": "boolean",
                        "default": True,
                        "format": "checkbox",
                        "propertyOrder": 2,
                    },
                    "enable_vlan": {
                        "type": "boolean",
                        "title": "enable vlan",
                        "default": True,
                        "format": "checkbox",
                        "propertyOrder": 3,
                    },
                    "vlan": {
                        "type": "array",
                        "title": "VLANs",
                        "uniqueItems": True,
                        "additionalItems": True,
                        "propertyOrder": 4,
                        "items": {
                            "type": "object",
                            "title": "VLAN",
                            "additionalProperties": True,
                            "required": [
                                "device",
                                "vlan",
                                "ports"
                            ],
                            "properties": {
                                "device": {
                                    "type": "string",
                                    "propertyOrder": 1,
                                },
                                "vlan": {
                                    "type": "integer",
                                    "propertyOrder": 2,
                                },
                                "ports": {
                                    "type": "string",
                                    "propertyOrder": 3,
                                }
                            }
                        }
                    }
                }
            }
        },
        "led": {
            "type": "array",
            "title": "LEDs",
            "uniqueItems": True,
            "additionalItems": True,
            "propertyOrder": 10,
            "items": {
                "type": "object",
                "title": "LED",
                "additionalProperties": True,
                "required": [
                    "name",
                    "sysfs",
                    "trigger"
                ],
                "properties": {
                    "name": {
                        "type": "string",
                        "propertyOrder": 1,
                    },
                    "default": {
                        "type": "boolean",
                        "format": "checkbox",
                        "propertyOrder": 2,
                    },
                    "dev": {
                        "type": "string",
                        "propertyOrder": 3,
                    },
                    "sysfs": {
                        "type": "string",
                        "propertyOrder": 4,
                    },
                    "trigger": {
                        "type": "string",
                        "propertyOrder": 5,
                    },
                    "delayoff": {
                        "type": "integer",
                        "propertyOrder": 6,
                    },
                    "delayon": {
                        "type": "integer",
                        "propertyOrder": 7,
                    },
                    "interval": {
                        "type": "integer",
                        "propertyOrder": 8,
                    },
                    "message": {
                        "type": "string",
                        "propertyOrder": 9,
                    },
                    "mode": {
                        "type": "string",
                        "propertyOrder": 10,
                    }
                }
            }
        },
        "firewall": {
            "type": "object",
            "title": "Firewall",
            "additionalProperties": True,
            "propertyOrder": 11,
            "properties": {
                "syn_flood": {
                    "type": "boolean",
                    "title": "enable SYN flood protection",
                    "default": False,
                    "format": "checkbox",
                    "propertyOrder": 1,
                },
                "input": {
                    "allOf": [
                        {"$ref": "#/definitions/firewall_policy"},
                        {
                            "title": "input",
                            "description": "policy for the INPUT chain of the filter table",
                            "propertyOrder": 2,
                        }
                    ]
                },
                "output": {
                    "allOf": [
                        {"$ref": "#/definitions/firewall_policy"},
                        {
                            "title": "output",
                            "description": "policy for the OUTPUT chain of the filter table",
                            "propertyOrder": 3,
                        }
                    ]
                },
                "forward": {
                    "allOf": [
                        {"$ref": "#/definitions/firewall_policy"},
                        {
                            "title": "forward",
                            "description": "policy for the FORWARD chain of the filter table",
                            "propertyOrder": 4,
                        }
                    ]
                },
                "forwardings": {
                    "type": "array",
                    "title": "Forwardings",
                    "propertyOrder": 5,
                    "items": {
                        "type": "object",
                        "title": "Forwarding",
                        "additionalProperties": False,
                        "required": [
                            "src",
                            "dest",
                        ],
                        "properties": {
                            "src": {
                                "type": "string",
                                "title": "src",
                                "description": "specifies the traffic source zone and must "
                                               "refer to one of the defined zone names",
                                "propertyOrder": 1,
                            },
                            "dest": {
                                "type": "string",
                                "title": "dest",
                                "description": "specifies the traffic destination zone and must "
                                               "refer to one of the defined zone names",
                                "propertyOrder": 2,
                            },
                            "family": {
                                "type": "string",
                                "title": "family",
                                "description": "protocol family (ipv4, ipv6 or any) to generate "
                                               "iptables rules for",
                                "enum": ["ipv4", "ipv6", "any"],
                                "default": "any",
                                "propertyOrder": 3
                            }
                        }
                    }
                },
                "zones": {
                    "type": "array",
                    "title": "Zones",
                    "propertyOrder": 6,
                    "items": {
                        "type": "object",
                        "title": "Zones",
                        "additionalProperties": True,
                        "required": [
                            "name"
                        ],
                        "properties": {
                            "name": {
                                "type": "string",
                                "title": "name",
                                "description": "unique zone name",
                                "maxLength": 11,
                                "propertyOrder": 1
                            },
                            "network": {
                                "type": "array",
                                "title": "Network",
                                "description": "list of interfaces attached to this zone",
                                "uniqueItems": True,
                                "propertyOrder": 2,
                                "items": {
                                    "title": "Network",
                                    "type": "string",
                                    "maxLength": 15,
                                    "pattern": "^[a-zA-z0-9_\\.\\-]*$"
                                }
                            },
                            "masq": {
                                "type": "boolean",
                                "title": "masq",
                                "description": "specifies wether outgoing zone traffic should be "
                                               "masqueraded",
                                "default": False,
                                "format": "checkbox",
                                "propertyOrder": 3
                            },
                            "mtu_fix": {
                                "type": "boolean",
                                "title": "mtu_fix",
                                "description": "enable MSS clamping for outgoing zone traffic",
                                "default": False,
                                "format": "checkbox",
                                "propertyOrder": 4,
                            },
                            "input": {
                                "allOf": [
                                    {"$ref": "#/definitions/zone_policy"},
                                    {
                                        "title": "input",
                                        "description": "default policy for incoming zone traffic",
                                        "propertyOrder": 5,
                                    }
                                ]
                            },
                            "output": {
                                "allOf": [
                                    {"$ref": "#/definitions/zone_policy"},
                                    {
                                        "title": "output",
                                        "description": "default policy for outgoing zone traffic",
                                        "propertyOrder": 6,
                                    }
                                ]
                            },
                            "forward": {
                                "allOf": [
                                    {"$ref": "#/definitions/zone_policy"},
                                    {
                                        "title": "forward",
                                        "description": "default policy for forwarded zone traffic",
                                        "propertyOrder": 7,
                                    }
                                ]
                            }
                        }
                    }
                },
                "rules": {
                    "type": "array",
                    "title": "Rules",
                    "propertyOrder": 7,
                    "items": {
                        "type": "object",
                        "title": "Rules",
                        "additionalProperties": True,
                        "required": [
                            "src",
                            "target"
                        ],
                        "properties": {
                            "name": {
                                "type": "string",
                                "title": "name",
                                "description": "name of the rule",
                                "propertyOrder": 1
                            },
                            "src": {
                                "type": "string",
                                "title": "src",
                                "description": "specifies the traffic source zone and must "
                                               "refer to one of the defined zone names",
                                "propertyOrder": 2
                            },
                            "src_ip": {
                                "type": "string",
                                "title": "src_ip",
                                "description": "match incoming traffic from the specified "
                                               "source ip address",
                                "propertyOrder": 3
                            },
                            "src_mac": {
                                "type": "string",
                                "title": "src_mac",
                                "description": "match incoming traffic from the specified "
                                               "mac address",
                                "pattern": "^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$",
                                "minLength": 17,
                                "maxLength": 17,
                                "propertyOrder": 4
                            },
                            "src_port": {
                                "type": "string",
                                "title": "src_port",
                                "description": "match incoming traffic from the specified "
                                               "source port or port range, if relevant proto "
                                               "is specified. Multiple ports can be specified "
                                               "separated by blanks",
                                "propertyOrder": 5
                            },
                            "proto": {
                                "type": "string",
                                "title": "proto",
                                "description": "match incoming traffic using the given protocol. "
                                               "Can be one of tcp, udp, tcpudp, udplite, icmp, esp, "
                                               "ah, sctp, or all or it can be a numeric value, "
                                               "representing one of these protocols or a different one. "
                                               "A protocol name from /etc/protocols is also allowed. "
                                               "The number 0 is equivalent to all",
                                "default": "tcpudp",
                                "propertyOrder": 6
                            },
                            "icmp_type": {
                                "title": "icmp_type",
                                "description": "for protocol icmp select specific icmp types to match. "
                                               "Values can be either exact icmp type numbers or type names",
                                "type": "array",
                                "uniqueItems": True,
                                "additionalItems": True,
                                "propertyOrder": 7,
                                "items": {
                                    "title": "ICMP type",
                                    "type": "string"
                                }
                            },
                            "dest": {
                                "type": "string",
                                "title": "dest",
                                "description": "specifies the traffic destination zone and must "
                                               "refer to one of the defined zone names, or * for "
                                               "any zone. If specified, the rule applies to forwarded "
                                               "traffic; otherwise, it is treated as input rule",
                                "propertyOrder": 8
                            },
                            "dest_ip": {
                                "type": "string",
                                "title": "dest_ip",
                                "description": "match incoming traffic directed to the specified "
                                               "destination ip address. With no dest zone, this "
                                               "is treated as an input rule",
                                "propertyOrder": 9
                            },
                            "dest_port": {
                                "type": "string",
                                "title": "dest_port",
                                "description": "match incoming traffic directed at the given "
                                               "destination port or port range, if relevant "
                                               "proto is specified. Multiple ports can be specified "
                                               "separated by blanks",
                                "propertyOrder": 10
                            },
                            "target": {
                                "allOf": [
                                    {"$ref": "#/definitions/rule_policy"},
                                    {
                                        "title": "target",
                                        "description": "firewall action for matched traffic",
                                        "propertyOrder": 11
                                    }
                                ]
                            },
                            "family": {
                                "type": "string",
                                "title": "family",
                                "description": "protocol family to generate iptables rules for",
                                "enum": ["ipv4", "ipv6", "any"],
                                "default": "any",
                                "propertyOrder": 12
                            },
                            "limit": {
                                "type": "string",
                                "title": "limit",
                                "description": "maximum average matching rate; specified as a number, "
                                               "with an optional /second, /minute, /hour or /day suffix",
                                "propertyOrder": 13
                            },
                            "enabled": {
                                "type": "boolean",
                                "title": "enable rule",
                                "default": True,
                                "format": "checkbox",
                                "propertyOrder": 14
                            }
                        }
                    }
                }
            }
        },
        "ddns": {
            "type": "object",
            "title": "DDNS Settings",
            "additionalProperties": True,
            "propertyOrder": 11,
            "properties": {
                "upd_privateip": {
                    "type": "boolean",
                    "title": "upd_privateip",
                    "description": "disallow/allow sending of private/special IP's to the DDNS provider; "
                                   "blocked IPv4: 0/8, 10/8, 100.64/10, 127/8, 169.254/16, 172.16/12, "
                                   "192.168/16; blocked IPv6: ::/32, f000::/4",
                    "default": False,
                    "format": "checkbox",
                    "propertyOrder": 1,
                },
                "ddns_dateformat": {
                    "type": "string",
                    "title": "ddns_dateformat",
                    "description": "date format to use for displaying dates in logfiles and LuCI",
                    "default": "%F %R",
                    "propertyOrder": 2,
                },
                "ddns_rundir": {
                    "type": "string",
                    "title": "ddns_rundir",
                    "description": "directory to use for *.pid and *.update files",
                    "default": "/var/run/ddns",
                    "propertyOrder": 3,
                },
                "ddns_logdir": {
                    "type": "string",
                    "title": "ddns_logdir",
                    "description": "directory to use for *.log files",
                    "default": "/var/log/ddns",
                    "propertyOrder": 4,
                },
                "ddns_loglines": {
                    "type": "integer",
                    "title": "ddns_loglines",
                    "description": "number of lines stored in *.log files before automatically truncated",
                    "default": 250,
                    "propertyOrder": 5,
                },
                "use_curl": {
                    "type": "boolean",
                    "title": "use_curl",
                    "description": "if both wget and curl are installed, wget is used for communication "
                                   "by default",
                    "default": False,
                    "format": "checkbox",
                    "propertyOrder": 6,
                },
                "providers": {
                    "type": "array",
                    "title": "Service Providers",
                    "uniqueItems": True,
                    "additionalItems": True,
                    "propertyOrder": 7,
                    "items": {
                        "type": "object",
                        "title": "DDNS provider",
                        "additionalProperties": True,
                        "required": [
                            "enabled",
                            "interface",
                            "ip_source",
                            "lookup_host",
                            "domain",
                            "username",
                            "password",
                        ],
                        "properties": {
                            "enabled": {
                                "type": "boolean",
                                "title": "enabled",
                                "default": False,
                                "format": "checkbox",
                                "propertyOrder": 1,
                            },
                            "interface": {
                                "type": "string",
                                "title": "interface",
                                "description": "network from /etc/config/network to monitor for up/down "
                                               "events to start the ddns update script via hotplug",
                                "propertyOrder": 2,
                            },
                            "ip_source": {
                                "type": "string",
                                "title": "ip_source",
                                "description": "specifies the source to detect the local IP: 'network' uses "
                                               "'ip_network', 'web' uses 'ip_url', 'interface' uses "
                                               "'ip_interface', 'script' uses 'ip_script'",
                                "enum": [
                                    "network",
                                    "web",
                                    "interface",
                                    "script"
                                ],
                                "default": "network",
                                "propertyOrder": 3,
                            },
                            "lookup_host": {
                                "type": "string",
                                "title": "lookup_host",
                                "description": "FQDN of the host registered at the DDNS provider",
                                "propertyOrder": 4,
                            },
                            "domain": {
                                "type": "string",
                                "title": "domain",
                                "description": "the DNS name to update; this property can also be used for "
                                               "special multihost update configurations supported by"
                                               " some providers",
                                "propertyOrder": 5,
                            },
                            "username": {
                                "type": "string",
                                "title": "username",
                                "description": "username of the DDNS service account",
                                "propertyOrder": 6,
                            },
                            "password": {
                                "type": "string",
                                "title": "password",
                                "description": "password of the DDNS service account",
                                "propertyOrder": 7,
                            },
                            "service_name": {
                                "type": "string",
                                "title": "service_name",
                                "description": "name of the DDNS service to use",
                                "propertyOrder": 8,
                            },
                            "update_url": {
                                "type": "string",
                                "title": "update_url",
                                "description": "url to the DDNS service to use if 'service_name' is not set",
                                "propertyOrder": 9,
                            },
                            "update_script": {
                                "type": "string",
                                "title": "update_script",
                                "description": "script to use if 'service_name' is not set",
                                "propertyOrder": 10,
                            },
                            "ip_network": {
                                "type": "string",
                                "title": "ip_network",
                                "description": "network from /etc/config/network to use for detecting the IP "
                                               "if 'ip_source' is set to 'network'",
                                "default": "wan",
                                "propertyOrder": 11,
                            },
                            "ip_url": {
                                "type": "string",
                                "title": "ip_url",
                                "description": "url to use for detecting the IP if 'ip_source' is set to "
                                               "'web'",
                                "propertyOrder": 12,
                            },
                            "ip_interface": {
                                "type": "string",
                                "title": "ip_interface",
                                "description": "local interface to use for detecting the IP if 'ip_source' is"
                                               " set to 'interface'",
                                "propertyOrder": 13,
                            },
                            "ip_script": {
                                "type": "string",
                                "title": "ip_script",
                                "description": "script to use for detecting the IP if 'ip_source' is set to "
                                               "'script'",
                                "propertyOrder": 14,
                            },
                            "use_syslog": {
                                "type": "integer",
                                "title": "use_syslog",
                                "description": "level of events logged to syslog",
                                "enum": [0, 1, 2, 3, 4],
                                "options": {
                                    "enum_titles": [
                                        "0 - disable",
                                        "1 - info, notice, warning, errors",
                                        "2 - notice, warning, errors",
                                        "3 - warning, errors",
                                        "4 - errors"
                                    ]
                                },
                                "default": 0,
                                "propertyOrder": 15,
                            },
                            "use_logfile": {
                                "type": "boolean",
                                "title": "use_logfile",
                                "description": "disable/enable logging to logfile",
                                "default": True,
                                "propertyOrder": 16,
                            }
                        }
                    }
                }
            }
        },
        "multisim": {
            "type": "array",
            "title": "Multisim Settings",
            "uniqueItems": True,
            "additionalItems": True,
            "propertyOrder": 11,
            "items": {
                "type": "object",
                "title": "Sim",
                "additionalProperties": True,
                "required": [
                    "name",
                    "plmn",
                    "apn"
                ],
                "properties": {
                    "name": {
                        "type": "string",
                        "title": "Name",
                        "propertyOrder": 1,
                    },
                    "plmn": {
                        "type": "integer",
                        "title": "PLMN",
                        "description": "Public Land Mobile Network (PLMN) identifier",
                        "default": 0,
                        "propertyOrder": 2,
                    },
                    "apn": {
                        "type": "string",
                        "title": "APN",
                        "description": "Access Point Name (APN)",
                        "propertyOrder": 3,
                    },
                    "pincode": {
                        "type": "integer",
                        "title": "Pincode",
                        "description": "pincode of the SIM card",
                        "propertyOrder": 4,
                    },
                    "auth": {
                        "type": "string",
                        "title": "Authentication",
                        "enum": [
                            "none",
                            "chap",
                            "pap",
                            "both"
                        ],
                        "default": "none",
                        "propertyOrder": 5,
                    },
                    "username": {
                        "type": "string",
                        "title": "Username",
                        "description": "username for authentication",
                        "propertyOrder": 6,
                    },
                    "password": {
                        "type": "string",
                        "title": "Password",
                        "description": "password for authentication",
                        "propertyOrder": 7,
                    },
                    "modes": {
                        "type": "string",
                        "title": "Modes",
                        "description": "Allowed network modes",
                        "enum": [
                            "all",
                            "lte",
                            "umts",
                            "gsm",
                            "lte,umts",
                            "lte,gsm",
                            "umts,gsm"
                        ],
                        "options": {
                            "enum_titles": [
                                "All",
                                "LTE",
                                "UMTS",
                                "GPRS",
                                "LTE/UMTS",
                                "LTE/GPRS",
                                "UMTS/GPRS"
                            ]
                        },
                        "default": "all",
                        "propertyOrder": 8,
                    }
                }
            }
        }
    }
})

# add OpenVPN schema
schema = merge_config(schema, base_openvpn_schema)
# OpenVPN customizations for OpenWRT
schema = merge_config(schema, {
    "definitions": {
        "tunnel": {
            "properties": {
                "disabled": {
                    "title": "disabled",
                    "description": "disable this VPN without deleting its configuration",
                    "type": "boolean",
                    "default": False,
                    "format": "checkbox",
                    "propertyOrder": 1
                }
            }
        }
    }
})
