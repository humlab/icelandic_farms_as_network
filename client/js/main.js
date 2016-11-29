
var layoutManager = null;
var layerManager = null;
var map = null;

$(document).ready(function() {

	//Create a Map controller
	map = new Map("frontPageMap");

	//Create a ResponsiveLayoutManager
	layoutManager = new ResponsiveLayoutManager();

	//Create a LayerManager
	layerManager = new LayerManager();

	//jQuery-UI magic
	$("#tabs").tabs({
	  active: 0
	});

});
