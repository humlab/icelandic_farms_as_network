

class Map {

	constructor(containerDomId) {
		if(containerDomId.length > 0) {
			this.createMapInContainer(containerDomId);
		}
	}

	createMapInContainer(containerDomId) {

		var format = 'image/png';
		var bounds = [134491.28507963746, 256709.59349107544, 872885.1398414932, 747362.6529178418];

		var mousePositionControl = new ol.control.MousePosition({
			className: 'custom-mouse-position',
			target: document.getElementById('location'),
			coordinateFormat: ol.coordinate.createStringXY(5),
			undefinedHTML: '&nbsp;'
		});

		var projection = new ol.proj.Projection({
			code: 'EPSG:3057',
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
