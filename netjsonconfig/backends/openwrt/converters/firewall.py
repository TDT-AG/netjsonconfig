from collections import OrderedDict

from ..schema import schema
from .base import OpenWrtConverter


class Firewall(OpenWrtConverter):
    netjson_key = 'firewall'
    intermediate_key = 'firewall'
    _uci_types = ['defaults', 'forwarding', 'zone']
    _schema = schema['properties']['firewall']

    def to_intermediate_loop(self, block, result, index=None):
        if block:
            provider_list = self.__intermediate_providers(block.pop('providers', {}))
            block.update({
                '.type': 'defaults',
                '.name': block.pop('id', None),
            })
            result.setdefault('firewall', [])
            result['firewall'] = [self.sorted_dict(block)] + provider_list
        return result

    def __intermediate_providers(self, providers):
        """
        converts NetJSON provider to
        UCI intermediate data structure
        """
        result = []
        for provider in providers:
            uci_name = self._get_uci_name(provider['lookup_host'])
            resultdict = OrderedDict((('.name', uci_name),
                                      ('.type', 'service')))
            for key, value in provider.items():
                resultdict[key] = value
            result.append(resultdict)
        return result

    def to_netjson_loop(self, block, result, index):
        result['firewall'] = self.__netjson_firewall(block)
        return result

    def __netjson_firewall(self, firewall):
        del firewall['.type']
        _name = firewall.pop('.name')
        if _name != 'firewall':
            firewall['id'] = _name
        return self.type_cast(firewall)
