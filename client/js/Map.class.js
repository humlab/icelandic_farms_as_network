
class Map {

	constructor() {

	}

	createMapInContainer(container_dom_id) {
		var dare_tile_layer = L.tileLayer('http://pelagios.dme.ait.ac.at/tilesets/imperium/{z}/{x}/{y}.png', {
		    attribution: '&copy; <a href="http://dare.ht.lu.se/">Digital Atlas of the Roman Empire</a>.',
			minZoom: 5,
			maxZoom: 11
		});
		

		var awmc_tile_layer = L.tileLayer('http://{s}.tiles.mapbox.com/v3/isawnyu.map-knmctlkh/{z}/{x}/{y}.png', {
		    attribution: '&copy; <a href="http://awmc.unc.edu/">Ancient World Mapping Center</a>'
		});


		var map = L.map(container_dom_id, {
			layers: [dare_tile_layer, awmc_tile_layer]
		}).setView([51.505, -0.09], 3);
		

		var baseMaps = {
		    "DARE Map": dare_tile_layer,
		    "AWMC Map": awmc_tile_layer
		};

		L.control.layers(baseMaps).addTo(map);

		map.on('baselayerchange', function(e) {
			console.log("hello");
		});

		self.map = map;
		return map;
	}

	populateMapWithVisualizations() {
		$.get("/service/visualizations", "", function(data) {
			//console.log(data);

			var layer = new L.geoJson(data, {
				onEachFeature: function(feature, layer) {
					var popupContent = ucfirst(feature.properties.siteType)+" site<br >";
					var gazetteerUrl = getGazetteerInterfaceByName(feature.properties.gazetteer).getPlaceURL(feature.properties.gazetteerId);
					popupContent += "<a target=\"_blank\" href=\""+gazetteerUrl+"\">"+feature.properties.gazetteer+" "+feature.properties.gazetteerId+"</a>";
					layer.bindPopup(popupContent);
					//layer.addTo(self.map);
				}
			});
			var myIcon = L.icon({
			    iconUrl: 'my-icon.png',
			    iconSize: [38, 95],
			    iconAnchor: [22, 94],
			    popupAnchor: [-3, -76],
			    shadowUrl: 'my-icon-shadow.png',
			    shadowSize: [68, 95],
			    shadowAnchor: [22, 94]
			});
			//layer.setIcon(myIcon);
			layer.addTo(self.map);

	    }, "json");
		
	}
};
