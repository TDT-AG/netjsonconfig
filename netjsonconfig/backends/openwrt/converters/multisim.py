from ..schema import schema
from .base import OpenWrtConverter


class Multisim(OpenWrtConverter):
    netjson_key = 'multisim'
    intermediate_key = 'multisim'
    _uci_types = ['sim']
    _schema = schema['properties']['multisim']['items']

    def to_intermediate_loop(self, block, result, index=None):
        block.update({
            '.type': 'multisim',
            '.name': block.pop('name', None),
        })
        result.setdefault('multisim', [])
        result['multisim'].append(self.sorted_dict(block))
        return result

    def to_netjson_loop(self, block, result, index):
        result.setdefault('multisim', [])
        result['multisim'].append(self.__netjson_multisim(block))
        return result

    def __netjson_multisim(self, sim):
        del sim['.type']
        sim['id'] = sim.pop('.name')
        return self.type_cast(sim)
