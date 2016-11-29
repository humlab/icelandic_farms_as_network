/**
* :: LayerManager ::
* This class handles everything relating to layers on the map. 
* It is responsible for responding to user actions that should affect the rendering of layers, such as a user clicking on a layer checkbox.
* It is also responsible for fetching the data associated with layers and properly drawing them on the map.
**/
class LayerManager {
	constructor() {
		//Listen to events from all the HTML-controls relating to layers

		//If a layer checkbox is selected or deselected, modify the data displayed on the map in an appropriate way
		$(".layerCheckbox").bind("change", function() {
			//If a box was selected we need to do some sort of XHR-fetching here but what and where? And then load that data into OL3
			//If a box was deselected we just need to clear the data corresponding to this layer from the OL3 map
			console.log(this.id); //This is the id of the checkbox which this event relates to
		});
	}
}