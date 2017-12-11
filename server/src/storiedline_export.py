import sys
import os
import time
import io
import json
sys.path = [ "." ] + sys.path
import config
import repository


class GeoJSONStoriedlineGenerator():

    def __init__(self, directory='/tmp'):
        self.store = repository.RepositoryRegistry().get(repository.QueryFarmRepository)
        self.directory = directory

    def ts_data_path(self, filename):
        return os.path.join(self.directory, '{}_{}'.format(time.strftime("%Y%m%d%H%M"), filename))

    def generate_json(self, table):
        data = self.store.get_table(table)
        for x in data:
            return x[0]
        return None

    def store_json(self, table, data):
        if data is None: return
        filename = self.ts_data_path(table + '.json')
        if data is not None:
            with io.open(filename, 'w', encoding='utf8') as f:
                json.dump(data, f)

    def generate_and_store(self, table):
        data = self.generate_json(table)
        self.store_json(table, data)


def main():
    tables = [
        'storiedlines_environmental_threats_web_exports_geojson',
        'storiedlines_farms_web_export_geojson',
        'storiedlines_property_network_web_export_geojson',
        'storiedlines_records_web_export_geojson',
        'storiedlines_resource_network_web_export_geojson'
    ]
    generator = GeoJSONStoriedlineGenerator()
    for table in tables:
        generator.generate_and_store(table)

if __name__ == '__main__':
    main()