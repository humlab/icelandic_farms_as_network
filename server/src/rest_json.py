#  -*- coding: utf-8 -*-
from datetime import date
from marshmallow import Schema, fields, pprint
import json

class JsonString(fields.Field):
    def _serialize(self, value, attr, obj):
        return json.loads(value)

# class NestedDict(fields.Nested):
#     def __init__(self, nested, key, *args, **kwargs):
#         super(NestedDict, self).__init__(nested, many=True, *args, **kwargs)
#         self.key = key

#     def _serialize(self, nested_obj, attr, obj):
#         nested_list = super(NestedDict, self)._serialize(nested_obj, attr, obj)
#         nested_dict = {item[self.key]: item for item in nested_list}
#         return nested_dict

#     def _deserialize(self, value, attr, data):
#         raw_list = [item for key, item in value.items()]
#         nested_list = super(NestedDict, self)._deserialize(raw_list, attr, data)
#         return nested_list

class QueryFarmSchema(Schema):
    isleif_farms_id = fields.Integer()
    row_number = fields.Integer()
    shire_name = fields.String()
    parish_name = fields.String()
    farm_name = fields.String()  
    farm_number = fields.String()
    farm_geometry_geojson = fields.String()
    farm_geometry = JsonString(attribute="farm_geometry_geojson")
    farm_property_value = fields.Integer()

class JamFarmsSubunitSchema(Schema):
    gid = fields.Integer()
    jam_subunit_type = fields.Integer()
    jam_subunit_geom_source = fields.String()
    jam_subunit_ornefni = fields.String()
    jam_subunit_numer_jord = fields.String()
    jam_subunit_samtala = fields.String()
    jam_farms_subunits_geom = fields.String()
    geometry_geojson = JsonString(attribute="geometry_geojson")

    jam_subunit_isleif_id = fields.Integer()
    jam_subunit_occupation_status = fields.Boolean()
    jam_subunit_establish_date = fields.Integer()
    jam_subunit_abandon_date = fields.Integer()
    jam_subunit_fulltext = fields.String()
    jam_subunit_proportion = fields.Integer()
    jam_subunit_type_id = fields.Integer()
    jam_landskuld_value = fields.Integer()
    jam_landskuld_paymethod_id = fields.Integer()
    jam_leigukugildi_value = fields.Decimal(6, 1)
    jam_leigukugildi_paymethod_id = fields.Integer()
    jam_leigukugildi_historic_value = fields.Decimal(6, 1)
    jam_leigukugildi_value_change_year = fields.Integer()
    jam_leigukugildi_value_change_reason = fields.Integer()
    jam_leigukugildi_notes = fields.String()
    jam_leigukugildi_aggregation = fields.Boolean()
    jam_subunit_abandon_reason_id = fields.Integer()
    jam_subunit_reoccupation_potential_id = fields.Integer()
    #jam_subunit_landskuld_paylocation = Column(ForeignKey('jam_farms_subunits.gid'))
    jam_subunit_landskuld_notes = fields.String()

class IsleifFarmSchema(Schema):

    isleif_farms_id = fields.Integer()
    county_name = fields.String()
    shire_name = fields.String(attribute="Hreppur")
    shire_number = fields.Integer(attribute="Hreppsnúmer")
    parish_name = fields.String(attribute="Sókn")
    farm_name = fields.String(attribute="Heiti_jarðar")
    farm_number = fields.String(attribute="Númer_jarðar")
    farm_division = fields.String(attribute="Skipting_jarðar")
    fields_and_smoothing = fields.String(attribute="Tún_og_sléttun")
    registration_history = fields.String(attribute="Skráningarsaga")
    boundary = fields.String(attribute="Landamerki")
    place_names = fields.String(attribute="Örnefni")
    subunits = fields.Nested("JamFarmsSubunitSchema", many=True) #, exclude=("playlist", ))
    jardabok_texts = fields.Nested("JamFullTextSchema", many=True)

class JamFullTextSchema(Schema):
    jardabok_full_text_id = fields.Integer()
    jardabok_full_text =  fields.String()
    isleif_farms_id = fields.Integer()
    logbyli_id = fields.Integer()
    hjaleiga_status =  fields.String()
    hjaleiga_number = fields.Integer()
    jam_census_property_occupation = fields.Boolean()
    jam_census_property_abandon_year = fields.Integer()
    jam_census_property_ecclesiastical_id = fields.Integer()
    jam_census_property_dyrleiki = fields.Integer()

