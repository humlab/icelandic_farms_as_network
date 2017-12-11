/*
-- CRASHES SERVER: select ST_GeomFromGeoJSON('{"type":"Point","coordinates":[-2188568.37409769,9235370.51506867]}')
*/

/***********************************************************************************************************************
**  View    storiedlines_environmental_threats_web_exports_geojson
************************************************************************************************************************/

Create Or Replace view storiedlines_environmental_threats_web_exports_geojson as 
    With  environmental_threats As (
        SELECT row_number() OVER (ORDER BY isleif_farms."Númer jarðar")             AS row_number,
            isleif_farms."Hreppur"                                                  AS shire_name,
            isleif_farms."Hreppsnúmer"                                              AS shire_number,
            isleif_farms."Heiti jarðar"                                             AS farm_name,
            isleif_farms."Númer jarðar"                                             AS farm_number,
            leca.lookup_environmental_agents_is                                     AS lookup_environmental_agents_is,
            leca.lookup_environmental_agents_en                                     AS lookup_environmental_agents_en,
            lookup_resource_type.lookup_resource_is                                 AS lookup_resource_is,
            lookup_resource_type.lookup_resource_en                                 AS lookup_resource_en,
            lookup_resource_change.lookup_resource_change_is                        AS lookup_resource_change_is,
            lookup_resource_change.lookup_resource_change_en                        AS lookup_resource_change_en,
            lookup_temporal_phase.temporal_phase_is                                 AS temporal_phase_is,
            lookup_temporal_phase.temporal_phase_en                                 AS temporal_phase_en,
            jam_environmental_threat_factors.environmental_threat_notes             AS environmental_threat_notes,
            st_transform(st_setsrid(jam_farms_subunits.geom, 3057), 4326)           AS geom
        FROM jam_environmental_threat_factors
        JOIN lookup_environmental_change_agents leca
          ON jam_environmental_threat_factors.lookup_environmental_change_agent_id = leca.lookup_environmental_change_agents_id
        JOIN lookup_resource_type
          ON jam_environmental_threat_factors.lookup_resource_type_id = lookup_resource_type.lookup_resource_id
        JOIN lookup_resource_change
          ON jam_environmental_threat_factors.lookup_resource_change_id = lookup_resource_change.lookup_resource_change_id
        JOIN lookup_temporal_phase
          ON jam_environmental_threat_factors.lookup_timedepth_event = lookup_temporal_phase.temporal_phase_id
        JOIN isleif_farms
          ON jam_environmental_threat_factors.isleif_farms_id = isleif_farms.isleif_farms_id
        JOIN jam_farms_subunits
          ON jam_farms_subunits.jam_subunit_isleif_id = isleif_farms.isleif_farms_id
    )
        select 
            json_build_object('type', 'FeatureCollection', 'features',
                json_agg(
                    json_build_object(
                        'type', 'Feature',
                        'id', row_number,
                        'geometry', json_build_object(
                            'type', 'Point',
                            'coordinates', json_build_array(st_x(geom), st_y(geom))
                         ),
                        'properties', json_build_object(
                            'id', row_number,
                            'shire_name', shire_name,
                            'shire_number', shire_number,
                            'farm_name', farm_name,
                            'farm_number', farm_number,
                            'is', json_build_object(
                                'lookup_environmental_agents', lookup_environmental_agents_is,
                                'lookup_resource', lookup_resource_is,
                                'lookup_resource_change', lookup_resource_change_is,
                                'temporal_phase', temporal_phase_is
                            ),
                            'en', json_build_object(
                                'lookup_environmental_agents', lookup_environmental_agents_en,
                                'lookup_resource', lookup_resource_en,
                                'lookup_resource_change', lookup_resource_change_en,
                                'temporal_phase', temporal_phase_en
                            ),                               
                            'environmental_threat_notes', environmental_threat_notes
                        )
                    )
                )
            )
        from environmental_threats;

/***********************************************************************************************************************
**  View    storiedlines_farms_web_export_geojson
************************************************************************************************************************/

CREATE OR REPLACE view storiedlines_farms_web_export_geojson AS 

    WITH farms AS (
        SELECT
            row_number() OVER (ORDER BY isleif_farms."Númer jarðar")        AS row_number,
            isleif_farms."Hreppur"                                          AS shire_name,
            isleif_farms."Sókn"                                             AS parish_name,
            isleif_farms."Heiti jarðar"                                     AS farm_name,
            isleif_farms."Númer jarðar"                                     AS farm_number,
            jam_full_text.jardabok_full_text                                AS jardabok_full_text,
            st_transform(st_setsrid(jam_farms_subunits.geom, 3057), 4326)   AS geom,
            jam_farms_logbyli.jam_census_property_dyrleiki                  AS jam_census_property_dyrleiki,
            isleif_farms.isleif_farms_id                                    AS isleif_farms_id,
            logbyli_valuations."1861_historic_value"                        AS historic_value_1861,
            logbyli_valuations."1861_adjusted_value"                        AS adjusted_value_1861
        FROM jam_farms_subunits
        LEFT JOIN isleif_farms
          ON jam_farms_subunits.jam_subunit_isleif_id = isleif_farms.isleif_farms_id
        LEFT JOIN logbyli_valuations
          ON isleif_farms.isleif_farms_id = logbyli_valuations.isleif_farms_id
        LEFT JOIN jam_full_text
          ON jam_full_text.isleif_farms_id = isleif_farms.isleif_farms_id
        LEFT JOIN jam_farms_logbyli
          ON jam_farms_logbyli.isleif_farms_id = isleif_farms.isleif_farms_id
        WHERE jam_farms_subunits.jam_subunit_type = 10
    )
        SELECT --json_pretty(
            json_build_object('type', 'FeatureCollection', 'features',
                json_agg(
                    json_build_object(
                        'type', 'Feature',
                        'id', row_number,
                        'geometry', json_build_object(
                            'type', 'Point',
                            'coordinates', json_build_array(st_x(geom), st_y(geom))
                         ),
                        'properties', json_build_object(
                            'id', row_number,
                            'isleif_farms_id', isleif_farms_id,
                            'shire_name', shire_name,
                            'parish_name', parish_name,
                            'farm_name', farm_name,
                            'farm_number', farm_number,
                            'jam_census_property_dyrleiki', jam_census_property_dyrleiki,
                            'historic_value_1861', historic_value_1861,
                            'adjusted_value_1861', adjusted_value_1861,
                            -- 'jardabok_full_text_base64', ENCODE(convert_to(jardabok_full_text, 'UTF8'), 'base64')
                            'jardabok_full_text', jardabok_full_text
                        )
                    )
                )
            )--)
        FROM farms;

/***********************************************************************************************************************
**  View    storiedlines_property_network_web_export_geojson
************************************************************************************************************************/

CREATE OR REPLACE VIEW public.storiedlines_property_network_web_export_geojson AS

    WITH property_network AS (
        SELECT
            row_number() OVER (ORDER BY view_spider_ownerhome.entity_name)          AS row_number,
            view_spider_ownerhome.entity_name                                       AS entity_name,
            view_spider_ownerhome.heimili                                           AS heimili,
            view_spider_ownerhome.heimili_code                                      AS heimili_code,
            lookup_people_historical_type.entity_type_alias                         AS entity_type_alias,
            view_spider_ownership.farm_name                                         AS property_name,
            view_spider_ownership.isleif_number                                     AS property_code,
            st_transform(st_setsrid(view_spider_ownerhome.geom, 3057), 4326)        AS geom_ownerhome,
            st_transform(st_setsrid(view_spider_ownership.geom, 3057), 4326)        AS geom_ownership,
            view_spider_ownership.link_jam_ownership_proportion                     AS link_jam_ownership_proportion
        FROM view_spider_ownerhome
        RIGHT JOIN view_spider_ownership
          ON view_spider_ownerhome.entity_name::text = view_spider_ownership.entity_name::text
        LEFT JOIN lookup_people_historical_type
          ON lookup_people_historical_type.entity_type_id = view_spider_ownerhome.entity_type_id
    )
        SELECT --json_pretty(
            json_build_object('type', 'FeatureCollection', 'features',
                json_agg(
                    json_build_object(
                        'type', 'Feature',
                        'id', row_number,
                        'geometry', json_build_object(
                            'type', 'Line',
                            'coordinates', json_build_array(
                                st_x(geom_ownerhome),
                                st_y(geom_ownerhome),
                                st_x(geom_ownership),
                                st_y(geom_ownership)
                            )
                         ),
                        'properties', json_build_object(
                            'id', row_number,
                            'entity_name', entity_name,
                            'entity_type_alias', entity_type_alias,
                            'heimili', heimili,
                            'heimili_code', heimili_code,
                            'property_name', property_name,
                            'property_code', property_code,
                            'link_jam_ownership_proportion', link_jam_ownership_proportion
                        )
                    )
                )
            )--)
        FROM property_network;

/***********************************************************************************************************************
**  View    storiedlines_records_web_export_geojson
************************************************************************************************************************/

CREATE OR REPLACE VIEW public.storiedlines_records_web_export_geojson AS 

    WITH records AS (
        SELECT
            row_number() OVER (ORDER BY records_full_text.records_tentative_date)   AS row_number,
            records_full_text.records_full_text                                     AS records_full_text,
            records_full_text.records_page_source                                   AS records_page_source,
            records_full_text.records_tentative_date                                AS records_tentative_date,
            records_full_text.records_notes                                         AS records_notes,
            isleif_farms."Heiti jarðar"                                             AS farm_name,
            isleif_farms."Númer jarðar"                                             AS farm_number,
            st_transform(st_setsrid(logbyli_points.geom, 3057), 4326)               AS geom,
            lookup_record_type.record_type_is                                       AS record_type_is,
            lookup_record_type.record_type_en                                       AS record_type_en
        FROM records_full_text
        JOIN isleif_farms
          ON records_full_text.records_primary_farm = isleif_farms.isleif_farms_id
         AND records_full_text.records_primary_farm = isleif_farms.isleif_farms_id
        JOIN logbyli_points
          ON isleif_farms."Númer jarðar"::text = logbyli_points.numer_jord::text
        JOIN lookup_record_type
          ON records_full_text.records_lookup_type = lookup_record_type.record_type_id
         AND records_full_text.records_lookup_type = lookup_record_type.record_type_id
    )
        SELECT --json_pretty(
            json_build_object('type', 'FeatureCollection', 'features',
                json_agg(
                    json_build_object(
                        'type', 'Feature',
                        'id', row_number,
                        'geometry', json_build_object(
                            'type', 'Point',
                            'coordinates', json_build_array(st_x(geom), st_y(geom))
                         ),
                        'properties', json_build_object(
                            'id', row_number,
                            'records_page_source', records_page_source,
                            'records_tentative_date', records_tentative_date,
                            'records_notes', records_notes,
                            'records_notes_base64', ENCODE(convert_to(records_notes, 'UTF8'), 'base64'),
                            'farm_name', farm_name,
                            'farm_number', farm_number,
                            'record_type_is', record_type_is,
                            'record_type_en', record_type_en,
                            -- 'records_full_text_base64', ENCODE(convert_to(records_full_text, 'UTF8'), 'base64')
                            'records_full_text', records_full_text
                        )
                    )
                )
            )--)
        FROM records;

/***********************************************************************************************************************
**  View    storiedlines_resource_network_web_export_geojson
************************************************************************************************************************/

CREATE OR REPLACE VIEW public.storiedlines_resource_network_web_export_geojson  AS
    WITH resource_network As (
        SELECT
            row_number() OVER (ORDER BY view_external_resources."Heiti jarðar")     AS row_number,
            view_external_resources."Sýsla"                                         AS county,
            view_external_resources."Hreppur"                                       AS shire_name,
            view_external_resources."Sókn"                                          AS parish_name,
            view_external_resources."Heiti jarðar"                                  AS farm_name,
            view_external_resources."Númer jarðar"                                  AS farm_number,
            view_external_resources.lookup_resource_en                              AS lookup_resource_en,
            view_external_resources.lookup_resource_use_en                          AS lookup_resource_use_en,
            isleif_farms."Heiti jarðar"                                             AS target_isleif_name,
            isleif_farms."Númer jarðar"                                             AS target_isleif_id,
            st_transform(st_setsrid(view_external_resources.geom, 3057), 4326)      AS geom_resource,
            st_transform(st_setsrid(view_external_sourcefarm.geom, 3057), 4326)     AS geom_sourcefarm,
            view_external_resources.lookup_resource_is                              AS lookup_resource_is,
            view_external_resources.jam_external_resource_notes                     AS jam_external_resource_notes,
            view_external_resources.temporal_phase_en                               AS temporal_phase_en
        FROM view_external_resources
        JOIN view_external_sourcefarm
          ON view_external_resources.id = view_external_sourcefarm.id
        JOIN isleif_farms
          ON isleif_farms.isleif_farms_id = view_external_sourcefarm.source_farm_id
    )
        SELECT --json_pretty(
            json_build_object('type', 'FeatureCollection', 'features',
                json_agg(
                    json_build_object(
                        'type', 'Feature',
                        'id', row_number,
                        'geometry', json_build_object(
                            'type', 'Line',
                            'coordinates', json_build_array(st_x(geom_resource), st_y(geom_resource), st_x(geom_sourcefarm), st_y(geom_sourcefarm))
                         ),
                        'properties', json_build_object(
                            'id', row_number,
                            'county', county,
                            'shire_name', shire_name,
                            'parish_name', parish_name,
                            'farm_name', farm_name,
                            'farm_number', farm_number,
                            'lookup_resource_en', lookup_resource_en,
                            'lookup_resource_use_en', lookup_resource_use_en,
                            'target_isleif_name', target_isleif_name,
                            'target_isleif_id', target_isleif_id,
                            'lookup_resource_is', lookup_resource_is,
                            'jam_external_resource_notes', jam_external_resource_notes,
                            -- 'jam_external_resource_notes', ENCODE(convert_to(jam_external_resource_notes, 'UTF8'), 'base64'),
                            'temporal_phase_en', temporal_phase_en
                        )
                    )
                )
            )--)
        FROM resource_network;


-- psql --host=archviz.humlab.umu.se --username=humlab --tuples-only --no-align --quiet --command="\COPY (SELECT * FROM storiedlines_resource_network_web_export_geojson) TO STDOUT (FROMAT text, HEADER false, ENCODING 'utf-8')""

