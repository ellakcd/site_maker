  // $( function() {
		//     $( "#sortable_headshots" ).sortable();
		//     $( "#sortable_headshots" ).disableSelection();
		//   } );

// function teatArea(results) {
// 	let photos = results["photos"];
// 	for (let i=0; i<photos.length; i++) {
// 		let photo = photos[i];
// 		$("#test_area").append("<img src={}".format(photo));
// 	}

// }


//ORDERING

function saveMiscPhotoOrder(evt) {
	evt.preventDefault();
	
	var newOrder = $( "#sortable_misc_photos" ).sortable( "toArray", {
		attribute: "id"
	});

	$.ajax({
		url: "/save_misc_photo_order",
		type: "POST",
		data: {"order": JSON.stringify(newOrder)}, 
	});
	console.log("end of function");
}


$("#save_misc_photo_order").on("click", saveMiscPhotoOrder);


function saveHeadshotOrder(evt) {
	evt.preventDefault();
	console.log("in js");
	var newOrder = $( "#sortable_headshots" ).sortable( "toArray", {
		attribute: "id"
	});
	console.log(newOrder);

	$.ajax({
		url: "/save_headshot_order",
		type: "POST",
		data: {"order": JSON.stringify(newOrder)}, 
	});
	console.log("end of function");
}


$("#save_headshot_order").on("click", saveHeadshotOrder);


function saveShowPhotoOrder(evt) {
	evt.preventDefault();
	console.log("saving show")
	var newOrder = $( "#sortable_show_photos" ).sortable( "toArray", {
		attribute: "id"
	});

	$.ajax({
	url: "/save_show_photo_order",
	type:"POST",
	data: {"order": JSON.stringify(newOrder)}, 
});
	console.log("end of function");
}


$("#save_show_photo_order").on("click", saveShowPhotoOrder);


function savePlayOrder(evt) {
	evt.preventDefault();
	console.log("saving play")
	var newOrder = $( "tbody" ).sortable( "toArray", {
		attribute: "id"
	});
	console.log(newOrder);

	$.ajax({
	url: "/save_play_order",
	type:"POST",
	data: {"order": JSON.stringify(newOrder)}, 
});
	console.log("end of function");
}


$("#save_play_order").on("click", savePlayOrder);


function saveFilmOrder(evt) {
	evt.preventDefault();
	console.log("saving film")
	var newOrder = $( "tbody" ).sortable( "toArray", {
		attribute: "id"
	});
	console.log(newOrder);

	$.ajax({
	url: "/save_film_order",
	type:"POST",
	data: {"order": JSON.stringify(newOrder)}, 
});
	console.log("end of function");
}


$("#save_film_order").on("click", saveFilmOrder);



function saveReviewOrder(evt) {
	evt.preventDefault();
	console.log("saving review")
	var newOrder = $( "#sortable_review_projects" ).sortable( "toArray", {
		attribute: "id"
	});

	$.ajax({
	url: "/save_review_order",
	type:"POST",
	data: {"order": JSON.stringify(newOrder)}, 
});
	console.log(newOrder);
	console.log("end of function");
}


$("#save_review_order").on("click", saveReviewOrder);


// function deletePhoto(evt) {
// 	evt.preventDefault();
// 	var photoId = $(this).data("photoId");
// 	var photoType = $(this).data("photoType");
// 	console.log("test");
// 	console.log(photoId);
// 	console.log(photoType);
// 	var result = confirm("Are you sure you want to hide this photo?");
// 	if(result) {
// 		$.ajax({
// 			url: "/delete_photo", 
// 			type: "POST", 
// 			data: {
// 				"photo_id": photoId, 
// 				"photo_type": photoType
// 			}
// 		});
// 	}
// }

$(".delete_photo").on("click", function (evt) {
	evt.preventDefault();

	var photoEl = this;
	var photoId = $(this).data("photoId");
	var photoType = $(this).data("photoType");

	var result = confirm("Are you sure you want to hide this photo?");
	if(result) {
		$.ajax({
			url: "/delete_photo",
			type: "POST",
			data: {
				"photo_id": photoId, 
				"photo_type": photoType
			},
		}).done(function() {
			$(photoEl).closest(".photo_container").addClass("hidden_element");
		});
	}
});



//HIDING

function includePhoto(evt) {
	evt.preventDefault();

	var photoEl = this;
	var photoId = $(this).data("photoId");
	var photoType = $(this).data("photoType");

		$.ajax({
			url: "/include_photo",
			type: "POST",
			data: {
				"photo_id": photoId, 
				"photo_type": photoType
			}
		}).done(function() {
			$(photoEl).closest(".photo_container").removeClass("hidden_element");
		});
	// }
}

$(".include_photo").on("click", includePhoto);


function deleteProject(evt) {
	evt.preventDefault();

	var projectEl = this;
	var projectId = $(this).data("projectId");
	var projectType = $(this).data("projectType");

    var result = confirm("Are you sure you want to hide?");

	if(result) {
		$.ajax({
			url: "/delete_project", 
			type: "POST", 
			data: {
				"project_id": projectId, 
				"project_type": projectType
			}
		}).done(function() {
			$(projectEl).closest("tr").addClass("hidden_element");
		});
	}
}

$(".delete_project").on("click", deleteProject);


function includeProject(evt) {
	evt.preventDefault();

	var projectEl = this;
	var projectId = $(this).data("projectId");
	var projectType = $(this).data("projectType");
	
		$.ajax({
			url: "/include_project", 
			type: "POST", 
			data: {
				"project_id": projectId, 
				"project_type": projectType
			}
		}).done(function() {
			$(projectEl).closest("tr").removeClass("hidden_element");
		});
}

$(".include_project").on("click", includeProject);


// function makeMainPhoto(evt) {

// 	var photoId = $(this).data("photoId");
// 		$.ajax({
// 			url: "/make_main_photo", 
// 			type: "POST", 
// 			data: {
// 				"photo_id": photoId
// 			}
// 		});
// }

// $(".make_main_photo").on("click", makeMainPhoto);


// function displayReadings(results) {
// 	var readings = results["readings"]
// }

// function addReading(evt) {
// 	evt.preventDefault();
// 	var reading = results["reading"];

// 	var formInputs = {
// 		"reading": reading
// 	}
// 	$.post("/add_reading", formInputs, displayReadings);

// }



// $("#add_reading").on("submit", addReading);




//EDITING


function showHomepage(results) {
 		console.log(results);
 		elementId = results["element_id"];
 		elementValue = results["element_value"]
 		document.getElementById(elementId).textContent=elementValue;
 		// $(".{elementId}").each(function(el, elementValue){
 		// 	el.textContent = elementValue;
 		// });
 	}


 	$(document).ready(function() {
 	$('.editable_homepage').editable(function(value, id) {
     console.log(this);
     console.log(value);
     console.log(this.id);
     var formInputs = {
     	"id": this.id, 
     	"value": value
     }
     $.post("/edit_homepage", formInputs, showHomepage);
     // return(value);
  }, {
     // type    : 'textarea',
     submit  : 'save',
     style : 'inherit', 
     style: "display: inline",
     height: 30, 
     width: 100
 });
 	 		});





function showResume(results) {
 		console.log(results);
 		elementId = results["element_id"];
 		elementValue = results["element_value"]
 		document.getElementById(elementId).textContent=elementValue;
 	}


 	$(document).ready(function() {
 	$('.editable_project').editable(function(value, id) {
     console.log(this);
     console.log(value);
     console.log(this.id);
     var formInputs = {
     	"id": this.id, 
     	"value": value
     }

     $.post("/edit_resume", formInputs, showResume);
     // return(value);
  }, {
     // type    : 'textarea',
     submit  : 'save',
     style : 'inherit', 
     style: "display: inline",
     height: 30, 
     width: 100, 
     placeholder: "add", 
     // submitcssclass: "btn btn-default", 
     // type: "autogrow"
 });
 	 		});



// function showMainPhoto(results) {
	
// }

// function changeMainPhoto(evt) {
// 	evt.preventDefault();
	
// }


// $(".change_main_photo").on("submit", changeMainPhoto);






