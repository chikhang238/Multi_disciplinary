

$("button").click(function(){
	  $("#table2excel").table2excel({
	    // exclude CSS class
	    exclude: ".abc",
	    name: "Worksheet Name",
	    filename: "SomeFile", //do not include extension
	    fileext: ".xls" // file extension
	  });
	});

