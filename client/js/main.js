
var layoutManager = null;
var map = null;

$(document).ready(function() {

	//Create map
	map = new Map("frontPageMap");

	//Instatiate layoutManager
	layoutManager = new ResponsiveLayoutManager();

	//jQuery-UI magic
	$("#tabs").tabs({
	  active: 1
	});
});
