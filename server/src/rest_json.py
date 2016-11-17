from datetime import date
from marshmallow import Schema, fields, pprint

class QueryFarmSchema(Schema):
    isleif_farms_id = fields.Integer()
    row_number = fields.Integer()
    shire_name = fields.String()
    parish_name = fields.String()
    farm_name = fields.String()  
    farm_number = fields.String()
    jardabok_full_text = fields.String()
    farm_geometry_geojson = fields.String()
    farm_property_value = fields.String()

class IsleifFarmSchema(Schema):

    Sýsla =  fields.String()
    Hreppur =  fields.String()
    Hreppsnúmer = fields.Integer()
    Sókn =  fields.String()
    Heiti_jarðar =  fields.String()
    Númer_jarðar =  fields.String()
    Skipting_jarðar =  fields.String()
    Tún_og_sléttun =  fields.String()
    Skráningarsaga =  fields.String()
    Landamerki =  fields.String()
    Örnefni =  fields.String()
    isleif_farms_id = fields.Integer()
