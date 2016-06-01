// Load Location depending onf the location level
function loadLocation(level,value) {
	console.log(level)
	var url = 'https://ebird.org/ws1.1/ref/location/list?rtype=' + level;
	if (level == 'country'){
		url = url + '&fmt=xml';
		radio_value = 'country';	
	} else if (level == 'subnational1') {
		url = url + '&countryCode=' + value + '&fmt=xml';
		radio_value = 'country';
	} else if (level == 'subnational2') {
		url = url + '&subnational1Code=' + value + '&fmt=xml';
		var radio_value = 'subnational1'
	} else {
		throw 'not defined level'
	}

	xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (xhttp.readyState == 4 && xhttp.status == 200) {
			var elmts = xhttp.responseXML.getElementsByTagName(level);
			list = document.getElementById('sel-loc-'+level);
			list.innerHTML='';
			document.getElementById('sel-loc-subnational2').innerHTML=''; // always erase this one
			for (var i = 0; i <elmts.length; i++) {
				var opt = document.createElement('option');
				opt.appendChild( document.createTextNode(elmts[i].getElementsByTagName("name")[0].childNodes[0].nodeValue) );
				opt.value = elmts[i].getElementsByTagName(level+"-code")[0].childNodes[0].nodeValue;
				list.appendChild(opt);
			}
			list.style.display = "block";
			updateLocRadio(radio_value)
		}
	};
	xhttp.open("GET", url, true);
	xhttp.send();
}


function updateLocRadio(value){
console.log(value)
	jQuery("input[value='" + value + "']").prop('checked',true)
}


function RunPython() {
	jQuery.ajax({
		type: "POST",
		url: "http://zoziologie.raphaelnussbaumer.com/wp-content/plugins/eBirdToLaTeX-Checklist-Generator/Script_Python.py",
		data: { param: 'hello'}
	}).done(function( o ) {
		console.log('Python runned')
	});
}



jQuery(document).ready(function(){
	// Populate Country 
	loadLocation('country',1);

	//var selLocCountry = document.getElementById('sel-loc-country');
	//selLocCountry.onchange = UpdateSelLocCountry();

	//var selLocSubnat1 = document.getElementById('sel-loc-subnat1');
	//selLocSubnat1.onchange = UpdateSelLocSubnat1;

	// Able to move the stuff in checklist-
	dragula([document.querySelector('#panel-body-col-library'), document.querySelector('#panel-body-col-checklist')]);
});
