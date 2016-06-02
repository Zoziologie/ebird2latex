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
	// check if all is ok for sumbitting to python
	// TO BE DONE
	
	var params = {
		code_loc: jQuery('#sel-loc-'+jQuery("input[name='radio-loc']:checked").val()).val()[0],
		lang: 'EN',
		cat: jQuery('#sel-cat').val().join('-'),
		byear: jQuery('#div-date-begin .form-control')[0].value.split('-')[0],
		eyear: jQuery('#div-date-begin .form-control')[1].value.split('-')[0],
		bmonth: jQuery('#div-date-begin .form-control')[0].value.split('-')[1],
		emonth: jQuery('#div-date-begin .form-control')[1].value.split('-')[1],

	};


	window.open("http://zoziologie.raphaelnussbaumer.com/wp-content/plugins/eBirdToLaTeX-Checklist-Generator/ChecklistGenerator.php?" + encodeURIComponent(jQuery.param(params)))


//	var esc = encodeURIComponent;
//	var query = Object.keys(params)
//		.map(k => esc(k) + '=' + esc(params[k]))
//		.join('&');
//	console.log(query)
//	window.open("http://zoziologie.raphaelnussbaumer.com/wp-content/plugins/eBirdToLaTeX-Checklist-Generator/ChecklistGenerator.php?"+query);
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
