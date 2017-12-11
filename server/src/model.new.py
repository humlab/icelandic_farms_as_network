#  -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer, Float, Text, DateTime, Date, ForeignKey, Numeric, BigInteger, SmallInteger, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import UserDefinedType
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import column_property
from geoalchemy2 import Geometry
import config
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy import func

Base = declarative_base()

logger = config.get_default_logger(__name__)

# class Geometry(UserDefinedType):
#     def get_col_spec(self):
#         return "GEOMETRY"

#     def bind_expression(self, bindvalue):
#         return func.ST_GeomFromText(bindvalue, type_=self)

#     def column_expression(self, col):
#         return func.ST_AsText(col, type_=self)
class AdminCountiesSveitarfelog(Base):
    __tablename__ = 'admin_counties_sveitarfelog'

    gid = Column(Integer, primary_key=True) #, server_default=text("nextval('sveitarfelog_pgis_gid_seq'::regclass)"))
    nrsveitarf = Column(Integer)
    _1904_sveitarfel = Column('1904_sveitarfel', String(50))
    geom = Column(Geometry, index=True)
    jam_hreppur = Column(String(100))
    _1847_hreppur = Column('1847_hreppur', String(100))
    jam_temp_date = Column(Date)
    jam_temp = Column(Integer)
    storabola_survey_year = Column(Integer)
    storabola_casualties = Column(Integer)
    storabola_manntal_population = Column(Integer)
    storabola_casualty_proportion = Column(Float)
    storabola_source = Column(String(255))


class QueryFarm(Base): 
    
    #__tablename__ = "view_storiedlines_main_farms"
    
    #isleif_farms_id = Column(Integer, primary_key=True)     # isleif_farms."isleif_farms_id"
    #row_number = Column(Integer)                            # isleif_farms."Númer jarðar" (row_number() over)
    #shire_name = Column(String(30))                         # isleif_farms."Hreppur"
    #parish_name = Column(String(20))                        # isleif_farms."Sókn"
    #farm_name = Column(String(30))                          # isleif_farms."Heiti jarðar"  
    #farm_number = Column(String(15))                        # isleif_farms."Númer jarðar"
    #jardabok_text_vector = column_property(Column(TSVECTOR), deferred=True)
    #farm_geometry_geojson = Column(Text())                  # jam_farms_subunits."geom"
    #farm_property_value = Column(Integer)                   # jam_farms_logbyli."jam_census_property_dyrleiki"

    __tablename__ = "storiedlines_farms_web_export"

    isleif_farms_id = Column(Integer, primary_key=True)
    shire_name = Column(String(60))
    parish_name = Column(String(60))
    farm_name = Column(String(60))
    farm_number = Column(String(20))
    geom = Column(String(30))
    jam_census_property_dyrleiki = Column(Integer)
    historic_value = Column("1861_historic_value", Float())
    adjusted_value = Column("1861_adjusted_value", Float())
    jardabok_full_text = Column(Text())

#class FarmTextSearch(Base):
    #extend_existing=True
#    __tablename__ = "storiedlines_farms_web_export"

#    isleif_farms_id = Column(Integer, primary_key=True)
#    jardabok_full_text = Column(Text())

class QueryResourceNetwork(Base):
    __tablename__ = "storiedlines_resource_network_web_export"

    row_number = Column(Integer, primary_key=True)
    county = Column(String(30))
    commune = Column(String(30))
    parish = Column(String(20))
    farm_name = Column(String(30))
    farm_number = Column(String(15))
    lookup_resource_en = Column(String(255))
    lookup_resource_use_en = Column(String(255))
    target_isleif_name = Column(String(30))
    target_isleif_id = Column(String(15))
    st_makeline = Column(Text())
    lookup_resource_is = Column(String(255))
    jam_external_resource_notes = Column(String(255))
    temporal_phase_en = Column(String(255))

class QueryPropertyNetwork(Base):
    __tablename__ = "storiedlines_property_network_web_export"

    row_number = Column(Integer, primary_key=True)
    entity_name = Column(String(255))
    heimili = Column(String(30))
    heimili_code = Column(String(15))
    entity_type_alias = Column(String(255))
    property_name = Column(String(30))
    property_code = Column(String(15))
    st_makeline = Column(Text())
    link_jam_ownership_proportion = Column(Integer())

# auto_generated follows

# Below is generated classes for most tables

class AdminParishes1847(Base):
    __tablename__ = 'admin_parishes_1847'

    parish_id = Column(Integer, primary_key=True) #, server_default=text("nextval('parishes_1847_id_seq'::regclass)"))
    parish_name = Column(String(255))
    parish_church_id = Column(ForeignKey('isleif_farms.isleif_farms_id'))
    parish_sysla = Column(String(255))

    parish_church = relationship('IsleifFarm')


class Bibliography(Base):
    __tablename__ = 'bibliography'

    bibliography_id = Column(Integer, primary_key=True) #, server_default=text("nextval('bibliography_id_seq'::regclass)"))
    bibliography_title = Column(String)
    bibliography_lookup_author = Column(Integer)
    bibliography_pub_year = Column(String(255))
    bibliography_pub_place = Column(String(255))


class HvOwner(Base):
    __tablename__ = 'hv_owners'

    id = Column(Integer, primary_key=True) #, server_default=text("nextval('hv_owners_id_seq'::regclass)"))
    owner = Column(String(255))
    value = Column(Float(53))


class IsleifFarm(Base):
    __tablename__ = 'isleif_farms'

    Sýsla = Column(String(20))
    Hreppur = Column(String(30))
    Hreppsnúmer = Column(Integer)
    Sókn = Column(String(20))
    Heiti_jarðar = Column('Heiti jar\xf0ar', String(30))
    Númer_jarðar = Column('N\xfamer jar\xf0ar', String(15), nullable=False, unique=True)
    Skipting_jarðar = Column('Skipting jar\xf0ar', Text)
    Tún_og_sléttun = Column('T\xfan og sl\xe9ttun', Text)
    Skráningarsaga = Column(Text)
    Landamerki = Column(Text)
    Örnefni = Column(Text)
    isleif_farms_id = Column(Integer, primary_key=True) #, unique=True, server_default=text("nextval('isleif_farms_id_seq'::regclass)"))
    start_date = Column(SmallInteger)
    end_date = Column(SmallInteger)




class IsleifFarmsGeom(Base):
    __tablename__ = 'isleif_farms_geom'

    gid = Column(Integer, primary_key=True) #, server_default=text("nextval('farms_pgis_gid_seq'::regclass)"))
    objectid = Column(Numeric)
    svfn = Column(Integer)
    sysla = Column(Numeric)
    hreppur = Column(Integer)
    hreppsnafn = Column(String(60))
    heiti = Column(String(47))
    landnr = Column(Numeric)
    fjoleigna = Column(String(80))
    uppruni = Column(Numeric)
    adferd = Column(Integer)
    nytjad_af = Column(Numeric)
    ath = Column(Text)
    gerd = Column(Integer)
    flokkar = Column(Integer)
    geom = Column(Geometry) #, index=True)
    isleif_code = Column(String(15))
    _19C_hreppur = Column('19C_hreppur', String(30))
    jam_isleif_code = Column(String(15))
    isleif_site_type = Column(Integer)
    isleif_site_description = Column(Text)


class IsleifSite(Base):
    __tablename__ = 'isleif_sites'

    Teljari = Column(BigInteger)
    Númer_jarðar = Column('N\xfamer jar\xf0ar', String(10))
    Fornleif_númer = Column('Fornleif n\xfamer', String(10))
    Samtala = Column(String(11), primary_key=True)
    Sérheiti = Column(String(50))
    Sérheiti_2 = Column('S\xe9rheiti-2', String(50))
    Tegund = Column(String(50))
    Type = Column(String(20))
    Hlutverk = Column(String(50))
    Hlutverk_2 = Column('Hlutverk-2', String(50))
    Function = Column(String(20))
    Aldur = Column(String(20))
    X__A_ = Column('X (A)', BigInteger)
    Y__N_ = Column('Y (N)', BigInteger)
    Norður = Column(String(15))
    Vestur = Column(String(15))
    Skekkja = Column(BigInteger)
    Metrar_yfir_sjávarmáli = Column('Metrar yfir sj\xe1varm\xe1li', Integer)
    Leiðarvísir = Column(Text)
    Aðstæður = Column(Text)
    Lögun = Column(String(15))
    Lengd = Column(Float(53))
    Breidd = Column(Float(53))
    Þvermál = Column(Float(53))
    Hleðsluhæð = Column(Float(53))
    Utanmál_innanmál = Column('Utanm\xe1l/innanm\xe1l', String(15))
    Mælt_stikað = Column('M\xe6lt/stika\xf0', String(15))
    Ástand = Column(String(25))
    Ef_horfin__af_hverju = Column('Ef horfin, af hverju', String(25))
    Friðlýsing = Column(String(10))
    Hættumat = Column(String(20))
    Ástæða = Column(String(25))
    Fornleifakönnun = Column(Text)
    Heimildamaður = Column(String(50))
    Fæðingardagur_og_ár = Column('F\xe6\xf0ingardagur og \xe1r', DateTime)
    Heim_maður_kom = Column('Heim-ma\xf0ur kom', Integer)
    Heimildir = Column(String(255))
    Aðrar_athugasemdir = Column('A\xf0rar athugasemdir', Text)
    Uppdrættir = Column(String(50))
    Ljósmyndir = Column(String(50))
    Loftljósmyndir = Column(String(50))
    Skrásetjari_á_vettvangi = Column('Skr\xe1setjari \xe1 vettvangi', String(10))
    Dags = Column(DateTime)
    Skrásetjari_á_gagnagrunn = Column('Skr\xe1setjari \xe1 gagnagrunn', String(20))
    Dagsetning_innsláttar = Column('Dagsetning innsl\xe1ttar', DateTime)
    leiðrétting = Column(String(10))
    Netleif = Column(Text)
    Flokkur = Column(String(1))
    isleif_code = Column(String(15))


class JamEnvironmentalThreatFactor(Base):
    __tablename__ = 'jam_environmental_threat_factors'

    id = Column(Integer, primary_key=True) #, server_default=text("nextval('jam_environmental_threat_factors_id_seq'::regclass)"))
    isleif_farms_id = Column(ForeignKey('isleif_farms.isleif_farms_id'))
    lookup_environmental_change_agent_id = Column(ForeignKey('lookup_environmental_change_agents.lookup_environmental_change_agents_id'))
    lookup_resource_type_id = Column(ForeignKey('lookup_resource_type.lookup_resource_id'))
    lookup_resource_change_id = Column(ForeignKey('lookup_resource_change.lookup_resource_change_id'))
    lookup_timedepth_event = Column(ForeignKey('lookup_temporal_phase.temporal_phase_id'))
    environmental_threat_notes = Column(Text)

    isleif_farms = relationship('IsleifFarm')
    lookup_environmental_change_agent = relationship('LookupEnvironmentalChangeAgent')
    lookup_resource_change = relationship('LookupResourceChange')
    lookup_resource_type = relationship('LookupResourceType')
    lookup_temporal_phase = relationship('LookupTemporalPhase')


class JamFarmsLogbyli(Base):
    __tablename__ = 'jam_farms_logbyli'

    jam_logbyli_id = Column(Integer, primary_key=True) #, server_default=text("nextval('jardabok_full_text_id_seq'::regclass)"))
    isleif_farms_id = Column(ForeignKey('isleif_farms.isleif_farms_id'), index=True)
    logbyli_id = Column(Integer)
    hjaleiga_status = Column(String(255))
    hjaleiga_number = Column(Integer)
    jam_census_property_occupation = Column(Boolean)
    jam_census_property_abandon_year = Column(SmallInteger)
    jam_census_property_ecclesiastical_id = Column(Integer)
    jam_census_property_dyrleiki = Column(SmallInteger)
    lookup_jam_tithe_id = Column(ForeignKey('lookup_tithe.lookup_jam_tithe_id'))
    jam_tithe_notes = Column(String)
    jam_ecclesiastical_extancy = Column(Boolean)

    isleif_farms = relationship('IsleifFarm')
    lookup_jam_tithe = relationship('LookupTithe')

class JamFodderProductivity(Base):
    __tablename__ = 'jam_fodder_productivity'

    id = Column(Integer, primary_key=True) #, server_default=text("nextval('jam_fodder_productivity_id_seq'::regclass)"))
    jam_farms_subunits_id = Column(ForeignKey('jam_farms_subunits.gid'))
    cows = Column(Numeric(16, 1))
    sheep = Column(SmallInteger)
    lamb = Column(SmallInteger)
    horse = Column(SmallInteger)
    ungneyti = Column(SmallInteger)

    jam_farms_subunits = relationship('JamFarmsSubunit')

class JamFullText(Base):
    __tablename__ = 'jam_full_text'

    jardabok_full_text_id = Column(Integer, primary_key=True) #, server_default=text("nextval('jardabok_full_text_id_seq'::regclass)"))
    jardabok_full_text = Column(Text)
    isleif_farms_id = Column(ForeignKey('isleif_farms.isleif_farms_id'), index=True)

    isleif_farms = relationship(IsleifFarm, backref=backref('jardabok_texts', uselist=True), uselist=False)

class JamFarmsSubunit(Base):
    __tablename__ = 'jam_farms_subunits'

    gid = Column(Integer, primary_key=True) #, server_default=text("nextval('farmpoints_gid_seq'::regclass)"))
    jam_subunit_type = Column(SmallInteger)
    jam_subunit_geom_source = Column(String(10))
    jam_subunit_ornefni = Column(String(254))
    jam_subunit_numer_jord = Column(String(8))
    jam_subunit_samtala = Column(String(12))

    jam_farms_subunits_geom = Column("geom", Geometry('POINT'))

    geometry_geojson = column_property(func.ST_AsGeoJSON(jam_farms_subunits_geom))

    jam_subunit_isleif_id = Column(ForeignKey('isleif_farms.isleif_farms_id'))
    jam_subunit_occupation_status = Column(Boolean)
    jam_subunit_establish_date = Column(SmallInteger)
    jam_subunit_abandon_date = Column(SmallInteger)
    jam_subunit_fulltext = Column(Text)
    jam_subunit_proportion = Column(SmallInteger)
    jam_subunit_type_id = Column(Integer) #ForeignKey('lookup_site_type.jam_subunit_type_id'))
    jam_landskuld_value = Column(SmallInteger)
    jam_landskuld_paymethod_id = Column(Integer) #ForeignKey('lookup_economy_paymethod.lookup_economy_paymethod_id'))
    jam_leigukugildi_value = Column(Numeric(6, 1))
    jam_leigukugildi_paymethod_id = Column(Integer) #ForeignKey('lookup_economy_paymethod.lookup_economy_paymethod_id'))
    jam_leigukugildi_historic_value = Column(Numeric(6, 1))
    jam_leigukugildi_value_change_year = Column(SmallInteger)
    jam_leigukugildi_value_change_reason = Column(Integer) #ForeignKey('lookup_tax_change_reasons.id'))
    jam_leigukugildi_notes = Column(String)
    jam_leigukugildi_aggregation = Column(Boolean)
    jam_subunit_abandon_reason_id = Column(Integer) #ForeignKey('lookup_farm_abandonment_reasons.id'))
    jam_subunit_reoccupation_potential_id = Column(Integer) #ForeignKey('lookup_farm_reoccupation_potential.id'))
    jam_subunit_landskuld_paylocation = Column(ForeignKey('jam_farms_subunits.gid'))
    jam_subunit_landskuld_notes = Column(String(255))
    jam_subunit_trade_port = Column(ForeignKey('trade_ports.gid'))

    jam_subunit_isleif = relationship(IsleifFarm, backref=backref('subunits', uselist=True), uselist=False)

    # #jam_landskuld_paymethod = relationship('LookupEconomyPaymethod', primaryjoin='JamFarmsSubunit.jam_landskuld_paymethod_id == LookupEconomyPaymethod.lookup_economy_paymethod_id')
    # #jam_leigukugildi_paymethod = relationship('LookupEconomyPaymethod', primaryjoin='JamFarmsSubunit.jam_leigukugildi_paymethod_id == LookupEconomyPaymethod.lookup_economy_paymethod_id')
    # #lookup_tax_change_reason = relationship('LookupTaxChangeReason')
    # #jam_subunit_abandon_reason = relationship('LookupFarmAbandonmentReason')
    # #jam_subunit_isleif = relationship('IsleifFarm')
    # parent = relationship('JamFarmsSubunit', remote_side=[gid])
    # #jam_subunit_reoccupation_potential = relationship('LookupFarmReoccupationPotential')
    # #jam_subunit_type1 = relationship('LookupSiteType')

    trade_port = relationship('TradePort')
    
class JamKvadir(Base):
    __tablename__ = 'jam_kvadir'

    jam_kvadir_type = Column(String(255))
    jam_kvadir_notes = Column(Text)
    jam_kvadir_subunit_id = Column(ForeignKey('jam_farms_subunits.gid'))
    jam_kvadir_obligation_subunit_id = Column(ForeignKey('jam_farms_subunits.gid'))
    id = Column(Integer, primary_key=True) #, server_default=text("nextval('jam_kvadir_id_seq1'::regclass)"))
    jam_kvadir_value = Column(String(255))
    jam_kvadir_use = Column(Boolean)
    jam_kvadir_temporal_notes = Column(Text)
    lookup_kvadir_type = Column(ForeignKey('lookup_kvadir.lookup_kvadir_id'))
    jam_kvadir_use_phase = Column(ForeignKey('lookup_temporal_phase.temporal_phase_id'))

    jam_kvadir_obligation_subunit = relationship('JamFarmsSubunit', primaryjoin='JamKvadir.jam_kvadir_obligation_subunit_id == JamFarmsSubunit.gid')
    jam_kvadir_subunit = relationship('JamFarmsSubunit', primaryjoin='JamKvadir.jam_kvadir_subunit_id == JamFarmsSubunit.gid')
    lookup_temporal_phase = relationship('LookupTemporalPhase')
    lookup_kvadir = relationship('LookupKvadir')


class JamLandEnvchange(Base):
    __tablename__ = 'jam_land_envchange'

    jam_land_envchange_id = Column(Integer, primary_key=True) #, server_default=text("nextval('event_record_land_quality_event_record_land_quality_id_seq'::regclass)"))
    jam_isleif_id = Column(ForeignKey('isleif_farms.isleif_farms_id'))
    jam_land_type_id = Column(ForeignKey('lookup_land_type.lookup_land_type_id'))
    jam_environmental_change_class_id = Column(ForeignKey('lookup_environmental_change_classes.lookup_environmental_change_classes_id'))
    jam_environmental_change_agent_id = Column(ForeignKey('lookup_environmental_change_agents.lookup_environmental_change_agents_id'))
    jam_land_envchange_notes = Column(String)

    jam_environmental_change_agent = relationship('LookupEnvironmentalChangeAgent')
    jam_environmental_change_class = relationship('LookupEnvironmentalChangeClass')
    jam_isleif = relationship('IsleifFarm')
    jam_land_type = relationship('LookupLandType')


class JamLandQuality(Base):
    __tablename__ = 'jam_land_quality'

    id = Column(Integer, primary_key=True) #, server_default=text("nextval('jam_pasture_quality_id_seq'::regclass)"))
    lookup_isleif_id = Column(ForeignKey('isleif_farms.isleif_farms_id'))
    lookup_land_type_id = Column(ForeignKey('lookup_land_type.lookup_land_type_id'))
    lookup_land_quality_id = Column(ForeignKey('lookup_land_quality.lookup_land_quality_id'))
    jam_land_quality_notes = Column(Text)

    lookup_isleif = relationship('IsleifFarm')
    lookup_land_quality = relationship('LookupLandQuality')
    lookup_land_type = relationship('LookupLandType')


class JamLandskuldChange(Base):
    __tablename__ = 'jam_landskuld_changes'

    jam_farm_subunit_id = Column(Integer, nullable=False) #, server_default=text("nextval('farmpoints_gid_seq'::regclass)"))
    jam_landskuld_value = Column(SmallInteger)
    jam_landskuld_paymethod_id = Column(ForeignKey('lookup_economy_paymethod.lookup_economy_paymethod_id'))
    jam_landskuld_historic_value = Column(SmallInteger)
    jam_landskuld_value_change_year = Column(SmallInteger)
    jam_landskuld_value_change_reason = Column(ForeignKey('lookup_tax_change_reasons.id'))
    jam_landskuld_changes_id = Column(Integer, primary_key=True) #, server_default=text("nextval('jam_landskuld_changes2_id_seq'::regclass)"))

    jam_landskuld_paymethod = relationship('LookupEconomyPaymethod')
    lookup_tax_change_reason = relationship('LookupTaxChangeReason')


class JamLivestock(Base):
    __tablename__ = 'jam_livestock'

    jam_livestock_id = Column(Integer, primary_key=True) #, server_default=text("nextval('jam_livestock_id_seq'::regclass)"))
    jam_livestock_category_id = Column(ForeignKey('lookup_livestock.lookup_livestock_id'))
    jam_livestock_number = Column(Integer)
    jam_livestock_notes = Column(String(255))
    jam_farm_subunit_id = Column(ForeignKey('jam_farms_subunits.gid'))

    jam_farm_subunit = relationship('JamFarmsSubunit')
    jam_livestock_category = relationship('LookupLivestock')


class JamRecordEvent(Base):
    __tablename__ = 'jam_record_events'

    jam_record_events_id = Column(Integer, primary_key=True) #, server_default=text("nextval('jam_record_events_id_seq'::regclass)"))
    jam_record_events_date = Column(Date)
    jam_record_events_farm_id = Column(ForeignKey('isleif_farms.isleif_farms_id'))
    jam_record_events_witness_1 = Column(String(255))
    jam_record_events_witness_2 = Column(String(255))
    jam_record_events_hreppur_id = Column(ForeignKey('admin_counties_sveitarfelog.gid'))
    jam_record_events_fulltext = Column(Text)

    jam_record_events_farm = relationship('IsleifFarm')
    jam_record_events_hreppur = relationship('AdminCountiesSveitarfelog')


class JamResourceAccessExternal(Base):
    __tablename__ = 'jam_resource_access_external'

    id = Column(Integer, primary_key=True) #, server_default=text("nextval('jam_resource_access_external_id_seq'::regclass)"))
    isleif_farms_id = Column(ForeignKey('isleif_farms.isleif_farms_id'))
    lookup_resource_id = Column(ForeignKey('lookup_resource_type.lookup_resource_id'))
    source_farm_id = Column(ForeignKey('isleif_farms.isleif_farms_id'))
    jam_resource_access_external_type_id = Column(ForeignKey('lookup_resource_access_external_type.id'))
    jam_resource_access_ownership_proportion = Column(SmallInteger)
    jam_resource_access_use_id = Column(ForeignKey('lookup_resource_use.lookup_resource_use_id'))
    jam_external_resource_notes = Column(Text)
    jam_external_resource_source = Column(ForeignKey('records_full_text.records_full_text_id'))
    jam_external_resource_temporal_phase = Column(ForeignKey('lookup_temporal_phase.temporal_phase_id'))

    isleif_farms = relationship('IsleifFarm', primaryjoin='JamResourceAccessExternal.isleif_farms_id == IsleifFarm.isleif_farms_id')
    records_full_text = relationship('RecordsFullText')
    lookup_temporal_phase = relationship('LookupTemporalPhase')
    jam_resource_access_external_type = relationship('LookupResourceAccessExternalType')
    jam_resource_access_use = relationship('LookupResourceUse')
    lookup_resource = relationship('LookupResourceType')
    source_farm = relationship('IsleifFarm', primaryjoin='JamResourceAccessExternal.source_farm_id == IsleifFarm.isleif_farms_id')


class JamResourceAccessInternal(Base):
    __tablename__ = 'jam_resource_access_internal'

    id = Column(Integer, primary_key=True) #, server_default=text("nextval('jam_resource_access_internal_id_seq'::regclass)"))
    isleif_farms_id = Column(ForeignKey('isleif_farms.isleif_farms_id'))
    resource_id = Column(ForeignKey('lookup_resource_type.lookup_resource_id'))
    resource_quality_id = Column(ForeignKey('lookup_resource_quality.lookup_resource_quality_id'))
    resource_change_id = Column(ForeignKey('lookup_resource_change.lookup_resource_change_id'))
    resource_use_id = Column(ForeignKey('lookup_resource_use.lookup_resource_use_id'))
    resource_fuel_use = Column(Boolean)
    resource_historic_quality_id = Column(ForeignKey('lookup_resource_quality.lookup_resource_quality_id'))
    resource_notes = Column(String)

    isleif_farms = relationship('IsleifFarm')
    resource_change = relationship('LookupResourceChange')
    resource_historic_quality = relationship('LookupResourceQuality', primaryjoin='JamResourceAccessInternal.resource_historic_quality_id == LookupResourceQuality.lookup_resource_quality_id')
    resource = relationship('LookupResourceType')
    resource_quality = relationship('LookupResourceQuality', primaryjoin='JamResourceAccessInternal.resource_quality_id == LookupResourceQuality.lookup_resource_quality_id')
    resource_use = relationship('LookupResourceUse')


class JamShip(Base):
    __tablename__ = 'jam_ships'

    jam_ships_id = Column(Integer, primary_key=True) #, server_default=text("nextval('jam_ships_id_seq'::regclass)"))
    jam_farm_subunit_id = Column(ForeignKey('jam_farms_subunits.gid'))
    jam_ships_count = Column(SmallInteger)
    jam_ships_seasonality = Column(String(255))
    jam_ships_ownership = Column(ForeignKey('lookup_ships_ownership.lookup_ships_ownership_id'))

    jam_farm_subunit = relationship('JamFarmsSubunit')
    lookup_ships_ownership = relationship('LookupShipsOwnership')


class Jardabok1861ValueAdjustment(Base):
    __tablename__ = 'jardabok_1861_value_adjustments'

    jardabok_1861_pk = Column(Integer, primary_key=True) #, server_default=text("nextval('jardabok_1861_value_adjustments_id_seq'::regclass)"))
    isleif_farm_id = Column(ForeignKey('isleif_farms.isleif_farms_id'))
    historic_value = Column(Float)
    adjusted_value = Column(Float)

    isleif_farm = relationship('IsleifFarm', primaryjoin='Jardabok1861ValueAdjustment.isleif_farm_id == IsleifFarm.isleif_farms_id')


class LandskuldPayment(Base):
    __tablename__ = 'landskuld_payments'

    landskuld_payments_id = Column(Integer, primary_key=True) #, server_default=text("nextval('landskuld_payments_id_seq'::regclass)"))
    landskuld_payments_proprietor_farm = Column(ForeignKey('isleif_farms.isleif_farms_id'))
    landskuld_payments_tenant_farm = Column(ForeignKey('isleif_farms.isleif_farms_id'))
    landskuld_payments_alnir = Column(Float)
    landskuld_payments_year = Column(Integer)
    landskuld_payments_source = Column(ForeignKey('records_full_text.records_full_text_id'))
    landskuld_text = Column(Text)
    landskuld_proprietor_name = Column(String(255))
    landskuld_tenant_name = Column(String(255))
    landskuld_ombudsman_name = Column(String(255))
    landskuld_payment_type = Column(ForeignKey('lookup_payment_type.payment_type_id'))

    lookup_payment_type = relationship('LookupPaymentType')
    proprietor_farm = relationship('IsleifFarm', primaryjoin='LandskuldPayment.landskuld_payments_proprietor_farm == IsleifFarm.isleif_farms_id')
    records_full_text = relationship('RecordsFullText')
    tenant_farm = relationship('IsleifFarm', primaryjoin='LandskuldPayment.landskuld_payments_tenant_farm == IsleifFarm.isleif_farms_id')


class LinkJamOwnership(Base):
    __tablename__ = 'link_jam_ownership'

    link_jam_ownership_id = Column(Integer, primary_key=True) #, server_default=text("nextval('link_jam_ownership_id_seq'::regclass)"))
    link_jam_ownership_isleif_id = Column(ForeignKey('isleif_farms.isleif_farms_id'))
    link_jam_people_historical_id = Column(ForeignKey('lookup_people_historical.entity_historical_id'))
    link_jam_ownership_proportion = Column(SmallInteger)

    link_jam_ownership_isleif = relationship('IsleifFarm')
    link_jam_people_historical = relationship('LookupPeopleHistorical')


class LinkLandskuldPaylocation(Base):
    __tablename__ = 'link_landskuld_paylocation'

    landskuld_paylocation_id = Column(Integer, primary_key=True) #, server_default=text("nextval('landskuld_paylocation_id_seq'::regclass)"))
    landskuld_paylocation_tenant_id = Column(ForeignKey('jam_farms_subunits.gid'))
    landskuld_paylocation_paymentplace_id = Column(ForeignKey('jam_farms_subunits.gid'))
    landskuld_paylocation_notes = Column(String(255))

    landskuld_paylocation_paymentplace = relationship('JamFarmsSubunit', primaryjoin='LinkLandskuldPaylocation.landskuld_paylocation_paymentplace_id == JamFarmsSubunit.gid')
    landskuld_paylocation_tenant = relationship('JamFarmsSubunit', primaryjoin='LinkLandskuldPaylocation.landskuld_paylocation_tenant_id == JamFarmsSubunit.gid')


class LookupPeopleHistorical(Base):
    __tablename__ = 'lookup_people_historical'

    entity_name = Column(String(255))
    entity_historical_id = Column(Integer, primary_key=True) #, server_default=text("nextval('people_historical_id_seq'::regclass)"))
    description = Column(Text)
    entity_type_id = Column(Integer, ForeignKey('lookup_people_historical_type.entity_type_id'))
    isleif_farms_id = Column(ForeignKey('isleif_farms.isleif_farms_id'))
    title = Column(String(255))

    entity_type = relationship('LookupPeopleHistoricalType', primaryjoin='LookupPeopleHistorical.entity_type_id == LookupPeopleHistoricalType.entity_type_id')
    isleif_farms = relationship(IsleifFarm, backref=backref('people', uselist=True), uselist=False)

class Logbyli1847Censu(Base):
    __tablename__ = 'logbyli_1847_census'

    Heiti_jarðar = Column('Heiti jar\xf0ar', String(30))
    Númer_jarðar = Column('N\xfamer jar\xf0ar', String(15))
    isleif_farms_id = Column(ForeignKey('isleif_farms.isleif_farms_id') ) #, server_default=text("nextval('isleif_farms_id_seq'::regclass)"))
    id = Column(Integer, primary_key=True) #, server_default=text("nextval('logbyli_1847_census_id_seq'::regclass)"))
    _1847_dyrleiki = Column('1847_dyrleiki', Float)
    _1847_landskuld = Column('1847_landskuld', Float)
    _1847_kugildi = Column('1847_kugildi', Float)
    _1847_eigendur = Column('1847_eigendur', Integer)
    _1847_prestar = Column('1847_prestar', Integer)
    _1847_notes = Column('1847_notes', Text)
    _1847_leigulidar = Column('1847_leigulidar', Integer)
    lookup_ownership_type = Column(ForeignKey('lookup_ownership_type.id'))
    lookup_owner = Column(ForeignKey('lookup_people_historical.entity_historical_id'))

    isleif_farms = relationship('IsleifFarm')
    lookup_people_historical = relationship('LookupPeopleHistorical')
    lookup_ownership_type1 = relationship('LookupOwnershipType')


class LogbyliValuation(Base):
    __tablename__ = 'logbyli_valuations'

    jam_logbyli_id = Column(Integer, primary_key=True) #, server_default=text("nextval('jardabok_full_text_id_seq'::regclass)"))
    isleif_farms_id = Column(ForeignKey('isleif_farms.isleif_farms_id')) #, index=True)
    jam_census_property_dyrleiki = Column(SmallInteger)
    _1861_historic_value = Column('1861_historic_value', Float)
    _1861_adjusted_value = Column('1861_adjusted_value', Float)
    _169x_cow_eqv = Column('169x_cow_eqv', Float)
    _169x_value_hundreds = Column('169x_value_hundreds', Float)
    _169x_taxation_hundreds = Column('169x_taxation_hundreds', Float)

    isleif_farms = relationship('IsleifFarm', primaryjoin='LogbyliValuation.isleif_farms_id == IsleifFarm.isleif_farms_id')

class LookupEconomyPaymethod(Base):
    __tablename__ = 'lookup_economy_paymethod'

    lookup_economy_paymethod_id = Column(Integer, primary_key=True) #, server_default=text("nextval('lookup_dyrleiki_id_seq'::regclass)"))
    lookup_economy_paymethod_is = Column(String(255))
    lookup_economy_paymethod_en = Column(String(255))
    lookup_economy_paymethod_notes = Column(String)


class LookupEnvironmentalChangeAgent(Base):
    __tablename__ = 'lookup_environmental_change_agents'

    lookup_environmental_change_agents_id = Column(Integer, primary_key=True) #, server_default=text("nextval('"lookup_environmental_change agents_id_seq"'::regclass)"))
    lookup_environmental_agents_is = Column(String(255))
    lookup_environmental_agents_en = Column(String(255))


class LookupEnvironmentalChangeClass(Base):
    __tablename__ = 'lookup_environmental_change_classes'

    lookup_environmental_change_classes_id = Column(Integer, primary_key=True) #, server_default=text("nextval('lookup_environmental_change_classes_id_seq'::regclass)"))
    lookup_environmental_change_is = Column(String(255))
    lookup_environmental_change_en = Column(String(255))


class LookupFarmAbandonmentReason(Base):
    __tablename__ = 'lookup_farm_abandonment_reasons'

    id = Column(Integer, primary_key=True) #, server_default=text("nextval('lookup_farm_abandonment_reasons_id_seq'::regclass)"))
    lookup_farm_abandonment_reason_is = Column(String(255))
    lookup_farm_abandonment_reason_en = Column(String(255))
    lookup_farm_abandonment_reason_notes = Column(Text)


class LookupFarmReoccupationPotential(Base):
    __tablename__ = 'lookup_farm_reoccupation_potential'

    id = Column(Integer, primary_key=True) #, server_default=text("nextval('lookup_reoccupation_potential_id_seq'::regclass)"))
    lookup_reoccupation_potential_is = Column(String(255))
    lookup_reoccupation_potential_en = Column(String(255))
    lookup_reoccupation_potential_notes = Column(Text)


class LookupKvadir(Base):
    __tablename__ = 'lookup_kvadir'

    lookup_kvadir_id = Column(Integer, primary_key=True) #, server_default=text("nextval('lookup_kvadir_id_seq'::regclass)"))
    lookup_kvadir_type_is = Column(String(255))
    lookup_kvadir_type_en = Column(String(255))
    lookup_kvadir_notes = Column(String)
    lookup_kvadir_id_varchar = Column(String(255))


class LookupLandQuality(Base):
    __tablename__ = 'lookup_land_quality'

    lookup_land_quality_id = Column(Integer, primary_key=True) #, server_default=text("nextval('lookup_tun_quality_id_seq'::regclass)"))
    lookup_land_quality_description = Column(String(255))
    lookup_land_quality_alias = Column(String(255))
    lookup_land_quality_value = Column(String(255))


class LookupLandType(Base):
    __tablename__ = 'lookup_land_type'

    lookup_land_type_id = Column(Integer, primary_key=True) #, server_default=text("nextval('lookup_land_type_id_seq'::regclass)"))
    lookup_land_type_is = Column(String(255))
    lookup_land_type_en = Column(String(255))


class LookupLivestock(Base):
    __tablename__ = 'lookup_livestock'

    lookup_livestock_id = Column(Integer, primary_key=True) #, server_default=text("nextval('lookup_livestock_id_seq'::regclass)"))
    lookup_livestock_is = Column(String(255))
    lookup_livestock_en = Column(Text)
    lookup_livestock_species = Column(Integer)
    lookup_livestock_age = Column(SmallInteger)
    lookup_livestock_sex = Column(ForeignKey('lookup_sex.id'))
    lookup_livestock_notes = Column(String)

    lookup_sex = relationship('LookupSex', primaryjoin='LookupLivestock.lookup_livestock_sex == LookupSex.id')


class LookupOccupationEvent(Base):
    __tablename__ = 'lookup_occupation_event'

    id = Column(Integer, primary_key=True) #, server_default=text("nextval('lookup_settlement_event_id_seq'::regclass)"))
    occupation_event_type = Column(String(255))


class LookupOwnershipType(Base):
    __tablename__ = 'lookup_ownership_type'

    id = Column(Integer, primary_key=True) #, server_default=text("nextval('lookup_ownership_type_id_seq'::regclass)"))
    ownership_type = Column(String(255))
    primary_farm_association = Column(ForeignKey('isleif_farms.isleif_farms_id'))

    isleif_farm = relationship('IsleifFarm')


class LookupPaymentType(Base):
    __tablename__ = 'lookup_payment_type'

    payment_type_id = Column(Integer, primary_key=True) #, server_default=text("nextval('lookup_payment_type_id_seq'::regclass)"))
    payment_type_is = Column(String(255))
    payment_type_en = Column(String(255))
    notes = Column(Text)

class LookupPeopleHistoricalType(Base):
    __tablename__ = 'lookup_people_historical_type'

    entity_type_alias = Column(String(255))
    entity_type_id = Column(Integer, primary_key=True) #, server_default=text("nextval('lookup_entity_type_id_seq'::regclass)"))


class LookupRecordType(Base):
    __tablename__ = 'lookup_record_type'

    record_type_id = Column(Integer, primary_key=True) #, server_default=text("nextval('records_type_lookup_id_seq'::regclass)"))
    record_type_is = Column(String(255))
    record_type_en = Column(String(255))
    record_type_notes = Column(String)


class LookupResourceAccessExternalType(Base):
    __tablename__ = 'lookup_resource_access_external_type'

    id = Column(Integer, primary_key=True) #, server_default=text("nextval('lookup_resource_access_external_type_id_seq'::regclass)"))
    lookup_resource_access_type_is = Column(String(255))
    lookup_resource_access_type_en = Column(String(255))


class LookupResourceChange(Base):
    __tablename__ = 'lookup_resource_change'

    lookup_resource_change_id = Column(Integer, primary_key=True) #, server_default=text("nextval('lookup_resource_change_id_seq'::regclass)"))
    lookup_resource_change_is = Column(String(255))
    lookup_resource_change_en = Column(String(255))


class LookupResourceQuality(Base):
    __tablename__ = 'lookup_resource_quality'

    lookup_resource_quality_id = Column(Integer, primary_key=True) #, server_default=text("nextval('lookup_resource_quality_id_seq'::regclass)"))
    lookup_resource_quality_is = Column(String(255))
    lookup_resource_quality_en = Column(String(255))


class LookupResourceType(Base):
    __tablename__ = 'lookup_resource_type'

    lookup_resource_id = Column(Integer, primary_key=True) #, server_default=text("nextval('lookup_resource_id_seq'::regclass)"))
    lookup_resource_is = Column(String(255))
    lookup_resource_en = Column(String(255))
    lookup_resource_notes = Column(String(255))


class LookupResourceUse(Base):
    __tablename__ = 'lookup_resource_use'

    lookup_resource_use_id = Column(Integer, primary_key=True) #, server_default=text("nextval('lookup_resource_use_id_seq'::regclass)"))
    lookup_resource_use_is = Column(String(255))
    lookup_resource_use_en = Column(String(255))


class LookupSex(Base):
    __tablename__ = 'lookup_sex'

    id = Column(Integer, primary_key=True) #, server_default=text("nextval('lookup_sex_id_seq'::regclass)"))
    lookup_sex_cat = Column(String(255))


class LookupShipsOwnership(Base):
    __tablename__ = 'lookup_ships_ownership'

    lookup_ships_ownership_id = Column(Integer, primary_key=True) #, server_default=text("nextval('lookup_ships_ownership_id_seq'::regclass)"))
    lookup_ships_ownership_category = Column(String(255))


class LookupShipsSeasonality(Base):
    __tablename__ = 'lookup_ships_seasonality'

    lookup_ships_seasonality_id = Column(Integer, primary_key=True) #, server_default=text("nextval('lookup_ships_seasonality_id_seq'::regclass)"))
    lookup_ships_seasonality_is = Column(String(255))
    lookup_ships_seasonality_en = Column(String(255))


class LookupSiteType(Base):
    __tablename__ = 'lookup_site_type'

    jam_subunit_type_id = Column(Integer, primary_key=True) #, server_default=text("nextval('lookup_sitestatus_id_seq'::regclass)"))
    jam_subunit_type_desc_is = Column(String(255))
    jam_subunit_type_id_desc_en = Column(String(255))
    jam_subunit_type_code = Column(SmallInteger)


class LookupSocialRole(Base):
    __tablename__ = 'lookup_social_roles'

    place_type = Column(String(255))
    description = Column(Text)
    place_id = Column(Integer, primary_key=True) #, server_default=text("nextval('place_type_id_seq'::regclass)"))


class LookupTaxChangeReason(Base):
    __tablename__ = 'lookup_tax_change_reasons'

    id = Column(Integer, primary_key=True) #, server_default=text("nextval('lookup_tax_change_reasons_id_seq'::regclass)"))
    tax_change_reasons_is = Column(String(255))
    tax_change_reasons_en = Column(String(255))
    tax_change_reasons_notes = Column(String)


class LookupTemporalPhase(Base):
    __tablename__ = 'lookup_temporal_phase'

    temporal_phase_id = Column(Integer, primary_key=True) #, server_default=text("nextval('lookup_temporal_phase_id_seq'::regclass)"))
    temporal_phase_is = Column(String(255))
    temporal_phase_en = Column(String(255))
    temporal_phase_notes = Column(Text)


class LookupTithe(Base):
    __tablename__ = 'lookup_tithe'

    lookup_jam_tithe_id = Column(Integer, primary_key=True) #, server_default=text("nextval('lookup_economy_tithe_id_seq'::regclass)"))
    lookup_jam_tithe_type = Column(String(255))


class LookupYear(Base):
    __tablename__ = 'lookup_year'

    lookup_year_id = Column(Integer, primary_key=True) #, server_default=text("nextval('lookup_year_lookup_year_id_seq'::regclass)"))
    year = Column(Integer)


class RecordsFullText(Base):
    __tablename__ = 'records_full_text'

    records_full_text_id = Column(Integer, primary_key=True) #, server_default=text("nextval('records_full_text_id_seq'::regclass)"))
    records_full_text = Column(Text)
    records_primary_farm = Column(ForeignKey('isleif_farms.isleif_farms_id'))
    records_lookup_source = Column(ForeignKey('bibliography.bibliography_id'))
    records_page_source = Column(String(255))
    records_tentative_date = Column(String(255))
    records_notes = Column(String)
    records_lookup_type = Column(ForeignKey('lookup_record_type.record_type_id'))
    records_name = Column(String)

    bibliography = relationship('Bibliography', primaryjoin='RecordsFullText.records_lookup_source == Bibliography.bibliography_id')
    lookup_record_type = relationship('LookupRecordType', primaryjoin='RecordsFullText.records_lookup_type == LookupRecordType.record_type_id')
    isleif_farm = relationship('IsleifFarm', primaryjoin='RecordsFullText.records_primary_farm == IsleifFarm.isleif_farms_id')


class SpatialRefSy(Base):
    __tablename__ = 'spatial_ref_sys'

    srid = Column(Integer, primary_key=True)
    auth_name = Column(String(256))
    auth_srid = Column(Integer)
    srtext = Column(String(2048))
    proj4text = Column(String(2048))

class TimeOccupationEvent(Base):
    __tablename__ = 'time_occupation_events'

    id = Column(Integer, primary_key=True) #, server_default=text("nextval('time_occupation_events_id_seq'::regclass)"))
    jam_farms_subunit_id = Column(ForeignKey('jam_farms_subunits.gid'))
    lookup_occupation_events_id = Column(ForeignKey('lookup_occupation_event.id'))
    lookup_year_id = Column(ForeignKey('lookup_year.lookup_year_id'))
    lookup_farm_abandonment_reasons_id = Column(ForeignKey('lookup_farm_abandonment_reasons.id'))
    lookup_record_source = Column(ForeignKey('records_full_text.records_full_text_id'))
    lookup_testimony_temporality = Column(ForeignKey('lookup_temporal_phase.temporal_phase_id'))

    jam_farms_subunit = relationship('JamFarmsSubunit')
    lookup_farm_abandonment_reasons = relationship('LookupFarmAbandonmentReason')
    lookup_occupation_events = relationship('LookupOccupationEvent')
    records_full_text = relationship('RecordsFullText')
    lookup_temporal_phase = relationship('LookupTemporalPhase')
    lookup_year = relationship('LookupYear')


class TradePort(Base):
    __tablename__ = 'trade_ports'

    gid = Column(Integer, primary_key=True) #, server_default=text("nextval('trade_ports_gid_seq'::regclass)"))
    id = Column(Numeric(10, 0))
    name = Column(String(80))
    gg_id = Column(String(80))
    time_start = Column(Numeric(10, 0))
    time_end = Column(Numeric(10, 0))
    notes = Column(String(254))
    port_main = Column(SmallInteger)
    geom = Column(Geometry) #, index=True)


class VerferdirLandleidir(Base):
    __tablename__ = 'verferdir_landleidir'

    gid = Column(Integer, primary_key=True) #, server_default=text("nextval('verferdir_landleidir_gid_seq'::regclass)"))
    objectid = Column(Numeric(10, 0))
    heiti = Column(String(50))
    uppruni = Column(String(50))
    shape_leng = Column(Numeric)
    flokkur = Column(String(50))
    geom = Column(Geometry) #, index=True)


class VerferdirSjoleidir(Base):
    __tablename__ = 'verferdir_sjoleidir'

    gid = Column(Integer, primary_key=True) #, server_default=text("nextval('verferdir_sjoleidir_gid_seq'::regclass)"))
    objectid = Column(Numeric(10, 0))
    heiti = Column(String(50))
    uppruni = Column(String(50))
    flokkur = Column(String(50))
    shape_leng = Column(Numeric)
    geom = Column(Geometry) #, index=True)


class VerferdirStadir(Base):
    __tablename__ = 'verferdir_stadir'

    gid = Column(Integer, primary_key=True) #, server_default=text("nextval('verferdir_stadir_gid_seq'::regclass)"))
    objectid = Column(Numeric(10, 0))
    nafn = Column(String(50))
    flokkur = Column(String(50))
    landshluti = Column(String(50))
    geom = Column(Geometry) #, index=True)


class XlegacySveitarfelogPgi(Base):
    __tablename__ = 'xlegacy_sveitarfelog_pgis'

    gid = Column(Integer, primary_key=True) #, server_default=text("nextval('sveitarfelog_pgis_gid_seq'::regclass)"))
    nrsveitar = Column(Integer)
    _1904_sveitarfel = Column('1904_sveitarfel', String(50))
    geom = Column(Geometry) #, index=True)
    jam_hreppur = Column(String(100))
    _1847_hreppur = Column('1847_hreppur', String(100))
