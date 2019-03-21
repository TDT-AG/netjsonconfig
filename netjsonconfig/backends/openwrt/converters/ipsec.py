from ..schema import schema
from .base import OpenWrtConverter


class IPsec(OpenWrtConverter):
    netjson_key = 'ipsec'
    intermediate_key = 'ipsec'
    _uci_types = ['ipsec']
    _schema = schema['properties']['ipsec']['items']

    def to_intermediate_loop(self, block, result, index=None):
        block.update({
            '.type': 'conn',
            '.name': block.pop('id', None) or
                     self.__get_auto_name(block),
        })
        result.setdefault('ipsec', [])
        result['ipsec'].append(self.sorted_dict(block))
        return result

    def __get_auto_name(self, ipsec):
        return '{0}'.format(ipsec['name'].lower())

    def to_netjson_loop(self, block, result, index):
        result.setdefault('ipsec', [])
        result['ipsec'].append(self.__netjson_ipsec(block))
        return result

    def __netjson_ipsec(self, ipsec):
        del ipsec['.type']
        _name = ipsec.pop('.name')
        if _name != self.__get_auto_name(ipsec):
            ipsec['id'] = _name
        return self.type_cast(ipsec)
