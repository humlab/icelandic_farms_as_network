
 $(document).ready(function() {

 	$(".section-toggle-button").bind("click", function() {

 		var hideSection = null;
 		var showSection = null;

 		if($(".section-right").css("display") == "none") {
 			switchSection("right");
 		}
 		else {
 			switchSection("left");
 		}

 		/*
 		showSection.animate({
 			width: "100vw"
 		}, 1000);
 		hideSection.animate({
 			width: "0vw"
 		}, 1000);
 		*/
 		
 	});


 	$(".section-left").resizable({
 		handles: "e",
 		resize: function(event, ui) {
 			//Slave right section to being the inverse size of the left section
 			var totalWidth = $(document).width();
 			var rightSectionWidth = totalWidth - ui.size.width;
 			$(".section-right").css("width", rightSectionWidth+"px");

 			//update map container according with left-section width and refresh map
 			$("#frontPageMap").css("width", $(".section-left").css("width"));
 			map.updateSize();
 		}
 	}).on("resize", function(e) {
 		e.stopPropagation();
 	});



 	enquire.register("screen and (max-width:640px)", {

	    // OPTIONAL
	    // If supplied, triggered when a media query matches.
	    match : function() {
	    	console.log("Match");
	    	switchSection("left");
	    	toggleToggleButton(true);
	    },      
	                                
	    // OPTIONAL
	    // If supplied, triggered when the media query transitions 
	    // *from a matched state to an unmatched state*.
	    unmatch : function() {
	    	console.log("Unmatch");
	    	$(".section-left").removeClass("full-section");
	    	$(".section-right").removeClass("full-section");
	    	$(".section-left").removeClass("hidden-section");
	    	$(".section-right").removeClass("hidden-section");
	    	toggleToggleButton(false);
	    },    
	    
	    // OPTIONAL
	    // If supplied, triggered once, when the handler is registered.
	    setup : function() {
	    	console.log("Setup");
	    },    
	                                
	    // OPTIONAL, defaults to false
	    // If set to true, defers execution of the setup function 
	    // until the first time the media query is matched
	    deferSetup : true,
	                                
	    // OPTIONAL
	    // If supplied, triggered when handler is unregistered. 
	    // Place cleanup code here
	    destroy : function() {
	    	console.log("Destroy");
	    }
	    
	});

 	$("#tabs").tabs({
	  active: 1
	});

 	var map = createFrontPageMap();

 });

function toggleToggleButton(show) {
	if(show) {
		$(".section-toggle-button").show();
	}
	else {
		$(".section-toggle-button").hide();
	}
}

function switchSection(section) {

	$(".section-left").removeClass("full-section");
	$(".section-right").removeClass("full-section");
	$(".section-left").removeClass("hidden-section");
	$(".section-right").removeClass("hidden-section");

	if(section == "left") {
		showSection = $(".section-left");
		hideSection = $(".section-right");
	}
	else {
		hideSection = $(".section-left");
		showSection = $(".section-right");
	}

	showSection.addClass("full-section");
	showSection.css("width", "100vw");
	$("#frontPageMap").css("width", "100vw");
	hideSection.addClass("hidden-section");
}

function createFrontPageMap() {

	$("#frontPageMap").html("");

	var iconStyleProduction = new ol.style.Style({
		image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
		anchor: [0.5, 32],
		anchorXUnits: 'fraction',
		anchorYUnits: 'pixels',
		src: '/images/marker-blue.png'
		}))
	});

	var iconStyleAncient = new ol.style.Style({
		image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
		anchor: [0.5, 32],
		anchorXUnits: 'fraction',
		anchorYUnits: 'pixels',
		src: '/images/marker-orange.png'
		}))
	});
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
          axisOrientation: 'neu'
    });

	var view = new ol.View({
		projection: projection,
	    //center: ol.proj.transform([12.4852, 41.8922], 'EPSG:4326', 'EPSG:3857'),
	    //zoom: 5,
	    //minZoom: 3,
		//maxZoom: 12
    });


	//Tile layers
	var iceland_source = new ol.source.TileWMS({
          url: 'http://archviz.humlab.umu.se:80/geoserver/Maps/wms',
          params: {
			'FORMAT': format,
			'VERSION': '1.1.1',
			tiled: true,
			LAYERS: 'Maps:1843_fornfraedafelagid',
			STYLES: '',
          }
        });

  var dare = new ol.source.XYZ({
  			logo: "http://dare.ht.lu.se/pics/logo-lu-en.png",
  			url: "http://pelagios.dme.ait.ac.at/tilesets/imperium/{z}/{x}/{y}.png",
  			attributions: [
			    new ol.Attribution({
			      html: 'Map graciously provided by ' +
			          '<a href="http://dare.ht.lu.se/">Digital Atlas of the Roman Empire</a> under a <a href="http://creativecommons.org/licenses/by-sa/3.0/">CC BY-SA</a> license.'
			    })
			  ]
  			});

	var layers = [
		new ol.layer.Tile({
	      source: new ol.source.OSM()
	    }),
		new ol.layer.Tile({
			source: iceland_source
		})
	];


	//Create map with tile layers and view
	var map = new ol.Map({
        controls: ol.control.defaults({
  			attribution: false
        }).extend([mousePositionControl]),
		layers: layers,
		target: 'frontPageMap',
		view: view
	});
	map.getView().fit(bounds, map.getSize());
	return map;
}