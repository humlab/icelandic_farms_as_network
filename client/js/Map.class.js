
class Map {

	constructor(containerDomId) {
		if(containerDomId.length > 0) {
			this.createMapInContainer(containerDomId);
		}
	}

	createMapInContainer(containerDomId) {

		var view = new ol.View({
		    center: ol.proj.transform([12.4852, 41.8922], 'EPSG:4326', 'EPSG:3857'),
		    zoom: 5,
		    minZoom: 3,
			maxZoom: 12
		});

		//Tile layers
		var layers = [
		new ol.layer.Tile({
				source: new ol.source.XYZ({
					logo: "http://dare.ht.lu.se/pics/logo-lu-en.png",
					url: "http://pelagios.dme.ait.ac.at/tilesets/imperium/{z}/{x}/{y}.png",
					attributions: [
				    new ol.Attribution({
				      html: 'Map graciously provided by ' +
				          '<a href="http://dare.ht.lu.se/">Digital Atlas of the Roman Empire</a> under a <a href="http://creativecommons.org/licenses/by-sa/3.0/">CC BY-SA</a> license.'
				    })
				  ]
					})
			}),
			new ol.layer.Tile({
		      source: new ol.source.OSM()
		    })
		];

		//Create map with tile layers and view
		this.map = new ol.Map({
			layers: layers,
			target: containerDomId,
			view: view
		});

		return this.map;
	}
}
