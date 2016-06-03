// Load Location depending onf the location level
function loadLocation(level,value) {
	var startelmt = 0;
	var url = 'https://ebird.org/ws1.1/ref/location/list?rtype=' + level;
	if (level == 'country'){
		url = url + '&fmt=xml';
		radio_value = 'country';	
	} else if (level == 'subnational1') {
		url = url + '&countryCode=' + value + '&fmt=xml';
		radio_value = 'country';
		startelmt = 1;
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
			for (var i = startelmt; i <elmts.length; i++) {
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
	jQuery("input[value='" + value + "']").prop('checked',true)
}


function RunPython() {
	// check if all is ok for sumbitting to python
	// TO BE DONE
	code_loc = jQuery('#sel-loc-'+jQuery("input[name='radio-loc']:checked").val()).val();
	if (code_loc == null) {
		alert('Location not selected. Please choose one');
		return
	} else if (code_loc.length>1){
		confirm('Warning: Several location selected, only the first one is taken! Continue ? ')
			code_loc = code_loc[0];
	} else {
		code_loc = code_loc[0];
	}

	var params = {
		code_loc: code_loc,
		project_name: jQuery('#sel-loc-'+jQuery("input[name='radio-loc']:checked").val()+' option:selected')[0].text,
		cat: jQuery('#sel-cat').val(),
		byear: jQuery('#div-date-begin .form-control')[0].value.split('-')[0],
		eyear: jQuery('#div-date-begin .form-control')[1].value.split('-')[0],
		bmonth: jQuery('#div-date-begin .form-control')[0].value.split('-')[1],
		emonth: jQuery('#div-date-begin .form-control')[1].value.split('-')[1],

	};

	params['col']=[];

	for (col of jQuery('#panel-body-col-checklist .btn')) {
		var col_list = [];
		col_list.push(col.type);

		forms=col.getElementsByClassName('form-control')
			col_list.push(forms[0].value);
		if (forms.length==2 && forms[1].value) {
			col_list.push(forms[1].value);
		} else{
			col_list.push(0);
		}
		params['col'].push(col_list);
	}	

	window.open("http://zoziologie.raphaelnussbaumer.com/wp-content/plugins/e2L/e2L.php?" + encodeURIComponent(jQuery.param(params)))

}




function FreqIndex(target) {
	var freqIndex = target.parentNode.getElementsByClassName('freq-index')[0];
	var value = target.value;
	if (value == 'year'){
		freqIndex.style.display='none';
		return
	} else if (value == 'season') {
		name = ['Spring','Summer','Autumn','Winter'];
	} else if (value == 'month') {
		name=['January','February','March','April','June','July','August','September','October','November','December'];
	} else if (value == 'week') {
		var name = [];
		for (var i = 0; i <= 54; i++) {
			name.push(i);
		};
	} else {
		alert('value of frequence not define')
		return
	}

	freqIndex.style.display='inline';
	freqIndex.innerHTML='';
	for (var i=0; i<name.length; i++){
		var option = document.createElement("option");
		option.value=i;
		option.text = name[i];
		freqIndex.add(option);
	}
}










jQuery(document).ready(function(){
	// Populate Country 
	loadLocation('country',1);

	// Able to move the stuff in checklist-
	dragula([document.getElementById('panel-body-col-library'), document.getElementById('panel-body-col-checklist')],{
		copy: function (el, source) {
			return source === document.getElementById('panel-body-col-library')
		},
		accepts: function (el, target) {
			return target !== document.getElementById('panel-body-col-library')
		},
		removeOnSpill: true
	});


});
