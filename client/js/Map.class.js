/**
* :: Map ::
* This class is basically just a wrapper around the OL3 map object and is supposed to provide some abstraction, convenience and encapsulation regarding map-related things.
**/
class Map {

	constructor(containerDomId) {
		if(containerDomId.length > 0) {
			this.createMapInContainer(containerDomId);
		}
	}

	createMapInContainer(containerDomId) {

		var format = 'image/png';
		var bounds = [-3218214.0777506866, 8840353.902547171, -1019292.003273349, 10381889.89850889];

		var mousePositionControl = new ol.control.MousePosition({
			className: 'custom-mouse-position',
			target: document.getElementById('location'),
			coordinateFormat: ol.coordinate.createStringXY(5),
			undefinedHTML: '&nbsp;'
		});

		var projection = new ol.proj.Projection({
			code: 'EPSG:3857', //EPSG:3057 would be better but it's not supported
			units: 'm',
			axisOrientation: 'neu',
			global: false,
			extent: bounds
		});

		var view = new ol.View({
			projection: projection,
		    minZoom: 1, 
			maxZoom: 5
		});

		//Tile layers
		var icelandSource = new ol.source.TileWMS({
			url: 'http://archviz.humlab.umu.se:80/geoserver/Maps/wms',
			params: {
				'FORMAT': format,
				'VERSION': '1.1.1',
				tiled: true,
				LAYERS: 'Maps:1843_fornfraedafelagid',
				STYLES: ''
			}
		});

		var layers = [
			/*
			new ol.layer.Tile({
	            source: new ol.source.OSM()
			}),
			*/
			new ol.layer.Tile({
				source: icelandSource
			})
		];

		this.map = new ol.Map({
			controls: ol.control.defaults({
				attribution: false
			}).extend([mousePositionControl]),
				layers: layers,
				target: 'frontPageMap',
				view: view
		});

		this.map.getView().fit(bounds, this.map.getSize());

		return this.map;
	}
}
