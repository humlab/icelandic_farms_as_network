/*
* :: ResponsiveLayoutManager ::
* This class is responsibe for adapting the user interface to various devices and their capabilities, primarly in terms of screen space.
* It relies on the Enquire js lib which in turn relies on CSS3 media queries.
* There should only be one instance of this class.
*/

class ResponsiveLayoutManager {

	constructor() {
		this.setupResizableSections();

		//Transition to small-screen mode at this width (in pixels)
		this.screenWidthBreakPoint = 720;

		enquire.register("screen and (max-width:"+this.screenWidthBreakPoint+"px)", {
			// OPTIONAL
			// If supplied, triggered when a media query matches.
			match : this.breakPointMatch,
			                            
			// OPTIONAL
			// If supplied, triggered when the media query transitions 
			// *from a matched state to an unmatched state*.
			unmatch : this.breakPointUnmatch,

			// OPTIONAL
			// If supplied, triggered once, when the handler is registered.
			setup : function() {
			},    

			// OPTIONAL, defaults to false
			// If set to true, defers execution of the setup function 
			// until the first time the media query is matched
			deferSetup : false,
			                            
			// OPTIONAL
			// If supplied, triggered when handler is unregistered. 
			// Place cleanup code here
			destroy : function() {
			}
		    
		});

		//Bind actions for clicking on the panel toggle button
		$(".sectionToggleButton").bind("click", function() {

			//Just toggles which section is shown based on which one is currently shown/hidden
			if($(".sectionRight").css("display") == "none") {
				ResponsiveLayoutManager.switchSection("right");
			}
			else {
				ResponsiveLayoutManager.switchSection("left");
			}
		});
	}


	/**
	* breakPointMatch
	* The things which happen when the layout transitions from big-screen to small-screen mode
	**/
	breakPointMatch() {
		ResponsiveLayoutManager.switchSection("left");
		ResponsiveLayoutManager.toggleToggleButton(true);
	}

	/**
	* breakPointUnmatch
	* The things which happen when the layout transitions from small-screen to big-screen mode
	**/
	breakPointUnmatch() {
		$(".sectionLeft").removeClass("fullSection");
		$(".sectionRight").removeClass("fullSection");
		$(".sectionLeft").removeClass("hiddenSection");
		$(".sectionRight").removeClass("hiddenSection");
		ResponsiveLayoutManager.toggleToggleButton(false);
	}

	/**
	* :: toggleToggleButton ::
	* Toggles the showing/hiding of the toggle-section button (in small screen mode)
	*/
	static toggleToggleButton(show) {
		if(show) {
			$(".sectionToggleButton").show();
		}
		else {
			$(".sectionToggleButton").hide();
		}
	}

	/**
	* :: switchSection ::
	* Takes care of everything needing to be done when switching between left/right sections in small-screen mode
	**/
	static switchSection(section) {

		$(".sectionLeft").removeClass("fullSection");
		$(".sectionRight").removeClass("fullSection");
		$(".sectionLeft").removeClass("hiddenSection");
		$(".sectionRight").removeClass("hiddenSection");

		var hideSection = null;
		var showSection = null;

		if(section == "left") {
			showSection = $(".sectionLeft");
			hideSection = $(".sectionRight");
		}
		else {
			hideSection = $(".sectionLeft");
			showSection = $(".sectionRight");
		}

		showSection.addClass("fullSection");
		showSection.css("width", "100vw");
		$("#frontPageMap").css("width", "100vw");
		hideSection.addClass("hiddenSection");
	}

	/**
	* :: setupResizableSections ::
	* Does what it says on the tin.
	**/
	setupResizableSections() {
		$(".sectionLeft").resizable({
			handles: "e",
			resize: function(event, ui) {
				//Slave right section to being the inverse size of the left section
				var totalWidth = $(document).width();
				var rightSectionWidth = totalWidth - ui.size.width;
				$(".sectionRight").css("width", rightSectionWidth+"px");

				//update map container according with left-section width and refresh map
				$("#frontPageMap").css("width", $(".sectionLeft").css("width"));
				map.map.updateSize();
			}
		}).on("resize", function(e) {
			//This was to prevent an issue with section-resize events being propagated as window-resize events
			e.stopPropagation();
		});
	}

}