from ..schema import schema
from .base import OpenWrtConverter


class Mwan3(OpenWrtConverter):
    netjson_key = 'mwan3'
    intermediate_key = 'mwan3'
    _uci_types = ['interface']
    _schema = schema['properties']['mwan3']

    def to_intermediate_loop(self, block, result, index=None):
        interfaces = self.__intermediate_interfaces(block, 'interfaces')

        result.setdefault(self.intermediate_key, [])
        result[self.intermediate_key] = interfaces
        return result

    def __intermediate_interfaces(self, block, uci_type):
        result = []

        for interface in block.get(uci_type, {}):
            interface.update(
                {
                    '.type': 'interface',
                    '.name': self.__get_auto_name(interface)
                }
            )
            result.append(self.sorted_dict(interface))

        return result

    def __get_auto_name(self, interface):
        return 'interface_{0}'.format(interface.get('name', None))

    def to_netjson_loop(self, block, result, index):
        result.setdefault(self.netjson_key, {})
        result[self.netjson_key].setdefault('interfaces', [])
        result[self.netjson_key]['interfaces'].append(
            self.__netjson_mwan3(block)
        )
        return result

    def __netjson_mwan3(self, mwan3):
        del mwan3['.type']
        _name = mwan3.pop('.name')

        if _name != self.__get_auto_name(mwan3):
            mwan3['id'] = _name

        schema = self._schema.get('properties').get('interfaces').get('items')
        return self.type_cast(mwan3, schema=schema)
