/*************************************************************************************
**  View  View that exposes data to the storiedline web application
**  NOTE! It is a materialized view for perfonace reasons, and hence needs to be
**        refreshed whenever data in dependent tables are updated  
**************************************************************************************/

CREATE MATERIALIZED VIEW view_storiedlines_farms as
    SELECT row_number() OVER (ORDER BY f."Númer jarðar") AS row_number,
        f.isleif_farms_id			        as isleif_farms_id,
        f."Hreppur"				            as shire_name,
        f."Sókn"					        as parish_name,
        f."Heiti jarðar"				    as farm_name,
        f."Númer jarðar"				    as farm_number,
        to_tsvector(t.jardabok_full_text)	as ts_jardabok_full_text,
        t.jardabok_full_text			    as jardabok_full_text,
        g.geom					            as farm_geometry,
        ST_AsGeoJSON(g.geom)			    as farm_geometry_geojson,
        v.jam_census_property_dyrleiki		as farm_property_value
    FROM isleif_farms f
    JOIN jam_farms_subunits g
     ON g.jam_subunit_isleif_id = f.isleif_farms_id
    JOIN jam_full_text t
     ON t.isleif_farms_id = f.isleif_farms_id
    JOIN jam_farms_logbyli v
     ON v.isleif_farms_id = f.isleif_farms_id
    WHERE g.jam_subunit_type = 10
