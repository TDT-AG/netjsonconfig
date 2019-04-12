from ..schema import schema
from .base import OpenWrtConverter


class IPsec(OpenWrtConverter):
    netjson_key = 'ipsec'
    intermediate_key = 'ipsec'
    _uci_types = ['conn', 'secret']
    _schema = schema['properties']['ipsec']

    def to_intermediate_loop(self, block, result, index=None):
        secrets = self._get_type_intermediate(block, 'secret')
        connections = self._get_type_intermediate(block, 'conn')

        result.setdefault(self.netjson_key, [])
        result[self.netjson_key] = secrets + connections
        return result

    def to_netjson_loop(self, block, result, index):
        result.setdefault(self.netjson_key, {})
        uci_type = block.pop(".type", None)

        if uci_type in self._uci_types:
            block_updated = self._get_type_netjson(block, uci_type)
            result[self.netjson_key].setdefault(uci_type, [])
            result[self.netjson_key][uci_type].append(block_updated)
        return result

    def _get_type_intermediate(self, block, uci_type):
        result = []
        for section in block.pop(uci_type, {}):
            section.update({
                '.type': uci_type,
                '.name': self.__get_auto_name(section, uci_type),
            })
            result.append(self.sorted_dict(section))
        return result

    def _get_type_netjson(self, block, uci_type):
        # next line could cause trouble
        _name = "_".join(block.pop('.name').split('_')[1:])
        if _name != self.__get_auto_name(block, uci_type):
            block['name'] = _name
        schema_uci_type = self._schema['properties'][uci_type]['items']
        result = self.type_cast(block, schema=schema_uci_type)
        return result

    def __get_auto_name(self, section, uci_type):
        return '{0}_{1}'.format(uci_type, section.pop('name', None))
