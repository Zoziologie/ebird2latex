function RunPython() {
	
	params = {
		code_loc: '',
		project_name: '',
		byear: jQuery('#div-date-begin .form-control')[0].value.split('-')[1],
		eyear: jQuery('#div-date-begin .form-control')[1].value.split('-')[1],
		bmonth: jQuery('#div-date-begin .form-control')[0].value.split('-')[0],
		emonth: jQuery('#div-date-begin .form-control')[1].value.split('-')[0],
		cat: [],
		col: [],
		condition: [jQuery('#threshold_rarity').val(),jQuery('#threshold_display').val()],
		format: jQuery('input[type=radio][name=format]:checked').val()+',margin='+jQuery('#margin').val()+'in',
		family: jQuery('input[value=family_name]').is(':checked')
	};

	// Location
	if (s_country.getValue()){
		if (s_sub1.getValue()){
			if (s_sub2.getValue()){
				params.code_loc = s_sub2.getValue();
				params.project_name =  s_sub2.getItem(s_sub2.getValue())[0].innerHTML;
			} else{
				params.code_loc = s_sub1.getValue();
				params.project_name =  s_sub1.getItem(s_sub1.getValue())[0].innerHTML;
			}
		} else {
			params.code_loc = s_country.getValue();
			params.project_name =  s_country.getItem(s_country.getValue())[0].innerHTML;
		}
	} else{
		alert('No Location choosen!')
		return;
	}

	// Categorie
	jQuery('#sel-cat :checkbox:checked').each(function(i){
		params.cat.push(jQuery(this).val());
	});
	if (params.cat.length==0){
		alert('No Categorie choosen!')
		return;
	}

	// Column
	if (jQuery('#panel-body-col-checklist .btn').length==0){
		alert('No colunm choosen!')
		return;
	}
	jQuery('#panel-body-col-checklist .btn').each(function(i,col){
		var col_list = [];
		col_list.push(col.type);

		forms=col.getElementsByClassName('form-control')
		col_list.push(forms[0].value);
		if (forms.length==2 && forms[1].value) {
			col_list.push(forms[1].value);
		} else{
			col_list.push(0);
		}
		params.col.push(col_list);
	});

	console.log(params)
	window.open("http://zoziologie.raphaelnussbaumer.com/ebirdtolatex/generate?" + jQuery.param(params,true))
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
		name=['January','February','March','April','May','June','July','August','September','October','November','December'];
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




var s_sub1, s_sub2, s_country, params;


jQuery(document).ready(function(){

	var $s_country = jQuery('#sel-loc-country').selectize({
		valueField: 'country-code',
		labelField: 'name',
		searchField: ['name','country-code'],
		onChange: function(value) {
			if (!value.length) return;
			s_sub1.disable();
			s_sub2.disable();
			s_sub2.clearOptions();
			s_sub1.clearOptions();
			jQuery.get('https://ebird.org/ws1.1/ref/location/list?rtype=subnational1&countryCode=' + value + '&fmt=xml',function(results){
				res=jQuery.parseJSON(xml2json(results).replace('undefined','')).response.result.subnational1;
				s_sub1.enable();
				s_sub1.addOption(res)
			});
		},
		onInitialize: function(){
			jQuery.get('https://ebird.org/ws1.1/ref/location/list?rtype=country&fmt=xml',function(results) {
				res=jQuery.parseJSON(xml2json(results).replace('undefined','')).response.result.country;
				s_country.addOption(res)
			});
		}
	});

	var $s_sub1 = jQuery('#sel-loc-subnational1').selectize({
		valueField: 'subnational1-code',
		labelField: 'name',
		searchField: ['name'],
		onChange: function(value) {
			if (!value.length) return;
			s_sub2.disable();
			s_sub2.clearOptions();
			jQuery.get('https://ebird.org/ws1.1/ref/location/list?rtype=subnational2&subnational1Code=' + value + '&fmt=xml',function(results){
				res=jQuery.parseJSON(xml2json(results).replace('undefined','')).response.result
				if (res){
					s_sub2.enable();
					s_sub2.addOption(res.subnational2)
				}
			});
		},
	});

	var $s_sub2 = jQuery('#sel-loc-subnational2').selectize({
		valueField: 'subnational2-code',
		labelField: 'name',
		searchField: ['name']
	});

	s_sub1  = $s_sub1[0].selectize;
	s_sub2  = $s_sub2[0].selectize;
	s_country = $s_country[0].selectize;

	s_sub1.disable();
	s_sub2.disable();


	// Date
	jQuery('#div-date-begin').datepicker({
		format: "mm-yyyy",
		startView: "months", 
		minViewMode: "months"
	});



	// Able to move the stuff in checklist-
	dragula([document.getElementById('panel-body-col-library'), document.getElementById('panel-body-col-checklist')],{
		copy: function (el, source) {
			return source === document.getElementById('panel-body-col-library')
		},
		accepts: function (el, target) {
			return target !== document.getElementById('panel-body-col-library')
		},
		removeOnSpill: true
	}).on('drop', function(){
		jQuery('#dropbox').remove()
	});



});
