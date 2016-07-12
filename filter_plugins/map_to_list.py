def map_to_list(map, key='key', value='value'):
    return [{key : k, value: v} for k, v in map.items()]

class FilterModule(object):
    def filters(self):
        return {'map_to_list': map_to_list}
