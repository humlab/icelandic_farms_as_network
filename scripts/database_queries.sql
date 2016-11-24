
-- The user enters a farm code, a farm name or a keyword in the search (or filter) field, and the system responds with a point distribution of all farms matching the entered text on the map.
-- System performs a free text search among (specifies entities), and returns all (geo-located) entities that matches the search, and displays a feature (marker) on the map for each entity.

/*************************************************************************************
**  View  View that simplifies full text search
**  NOTE! It is a materialized view and must be refreshed whenever data are updated  
**************************************************************************************/

DROP MATERIALIZED VIEW view_jam_text_vector;

ALTER DATABASE isleif_development
  SET default_text_search_config = 'pg_catalog.Simple';

CREATE MATERIALIZED VIEW view_jam_text_vector AS
  SELECT f.isleif_farms_id, to_tsvector(Coalesce(replace(f."Númer jarðar",'-',''),'') || ' ' || Coalesce(f."Heiti jarðar",'') || ' ' || string_agg(Coalesce(t.jardabok_full_text,''), ' ')) AS jardabok_text_vector
  FROM isleif_farms f
  LEFT JOIN jam_full_text t
    ON t.isleif_farms_id = f.isleif_farms_id
  GROUP BY f.isleif_farms_id;

CREATE INDEX idx_view_jam_text_vector_farms_id
    ON public.view_jam_text_vector USING btree (isleif_farms_id);
  
CREATE INDEX idx_gin_view_jam_text_vector
    ON public.view_jam_text_vector USING gin(jardabok_text_vector);
     
ALTER TABLE public.view_jam_text_vector
    OWNER TO gisli;
    
/*************************************************************************************
**  View  View that exposes main form data to the storiedline web application
**  NOTE! It is a materialized view for perfonace reasons, and hence needs to be
**        refreshed whenever data in dependent tables are updated  
**************************************************************************************/
-- DROP MATERIALIZED VIEW view_storiedlines_main_farms  
CREATE MATERIALIZED VIEW view_storiedlines_main_farms as
    SELECT row_number() OVER (ORDER BY f."Númer jarðar") AS row_number,
        f.isleif_farms_id			        as isleif_farms_id,
        f."Hreppur"				            as shire_name,
        f."Sókn"					        as parish_name,
        f."Heiti jarðar"				    as farm_name,
        f."Númer jarðar"				    as farm_number,
        x.jardabok_text_vector				as jardabok_text_vector,
        ST_AsGeoJSON(g.geom)			    as farm_geometry_geojson,
        v.jam_census_property_dyrleiki		as farm_property_value
    FROM isleif_farms f
    JOIN view_jam_text_vector x
      ON x.isleif_farms_id = f.isleif_farms_id
    JOIN jam_farms_subunits g
     ON g.jam_subunit_isleif_id = f.isleif_farms_id
    JOIN jam_farms_logbyli v
     ON v.isleif_farms_id = f.isleif_farms_id
    WHERE g.jam_subunit_type = 10;
 
SELECT * FROM isleif_farms WHERE isleif_farms_id = 2;

SELECT isleif_farms_id, count(*)
FROM view_jam_text_vector
GROUP by isleif_farms_id
having count(*) > 1
WHERE jardabok_text_vector @@ 'afdeilt'
    
 SELECT alias, description, token FROM ts_debug('AB-12');
 
 SELECT alias, description, token FROM ts_debug('foo-bar-beta1');
    