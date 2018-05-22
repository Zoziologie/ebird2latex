/*
BUILT LocationList.json
var resultats=[];
var res
var rtype=['country','subnational1','subnational2'];
for (var i = 0; i < 3; i++ ){
	jQuery.get('https://ebird.org/ws1.1/ref/location/list?rtype=' + rtype[i] + '&fmt=xml',function(data){
		res = jQuery.parseJSON(xml2json(data).replace('undefined','')).response;
		list= res.result[res.header.criteria["region-type"]];
		jQuery.each(list,function( key, value){
			list[key].code = value[res.header.criteria["region-type"]+'-code'];
		})
		resultats= resultats.concat(list);
	});
}
JSON.stringify(resultats); 
*/



function RunPython() {

	filtdiv = jQuery( ":radio.radio-filter:checked" ).parent()[0];
	filt_cond = '[\''+filtdiv.querySelector('.freq-period').value+'\']';
	if (filtdiv.querySelector('.freq-period').value != 'year'){
		filt_cond=filt_cond+'['+filtdiv.querySelector('.freq-index').value+']';
	}

	params = {
		code_loc: '',
		project_name: jQuery('#checklistname').html(),
		byear: jQuery('#div-date-begin .form-control')[0].value.split('-')[1],
		eyear: jQuery('#div-date-begin .form-control')[1].value.split('-')[1],
		bmonth: jQuery('#div-date-begin .form-control')[0].value.split('-')[0],
		emonth: jQuery('#div-date-begin .form-control')[1].value.split('-')[0],
		cat: [],
		col: [],
		condition: [filt_cond,jQuery('#threshold_rarity').val()/100, jQuery('#threshold_display').val()/100],
		format: jQuery('input[type=radio][name=format]:checked').val()+',margin='+jQuery('#margin').val()+'mm,'+jQuery('input[type=radio][name=column]:checked').val(),
		spacing: jQuery('#linespacing').val()/100,
		family: jQuery('input[value=family_name]').is(':checked')
	};

	// Location
	if (loc){
		params.code_loc = loc;
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
		//target.parentElement.querySelector('.radio-filter').value="['year']";
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



var params, sel_loc, LocationList, layer, map, loc;

jQuery(document).ready(function(){

	
	$sel_loc = jQuery('#sel-loc').selectize({
		valueField: 'code',
		labelField: 'name',
		searchField: ['name','code'],
		onInitialize: function(){
			jQuery.get('https://zoziologie.raphaelnussbaumer.com/wp-content/plugins/e2L/LocationList.json',function(data) {
				LocationList = data;
				sel_loc.addOption(LocationList)
			});
		},
		onChange: function(value){
			jQuery('#checklistname').html('Checklist of '+jQuery.grep(LocationList, function(e){ return e.code == value; })[0].name)
			jQuery('#sel-hotspot').show()
			loc = value;
		}
	});
	sel_loc  = $sel_loc[0].selectize;


	// Date
	jQuery('#div-date-begin').datepicker({
		format: "mm-yyyy",
		startView: "months", 
		minViewMode: "months"
	});


	/*jQuery('#margin').change(function(e){
		switch(jQuery('input[type=radio][name=format]:checked').val()) {
			case 'a4paper':
			wid=210;
			break;
			case 'a5paper':
			wid=148;
			break;
			case 'a3paper':
			wid=297;
			break;
			case 'letterpaper':
			wid=216;
			break;
		}
		console.log(jQuery(this).val())
		jQuery('#panel-body-col-checklist').css('margin',(jQuery(this).val()/wid*100).toString()+'%')
	})
	*/

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

	jQuery('.fa-pencil').click(function() {
		var el = document.getElementById("checklistname");
		var range = document.createRange();
		var sel = window.getSelection();
		range.setStart(el.childNodes[0], 0);
		range.collapse(true);
		sel.removeAllRanges();
		sel.addRange(range);
		el.focus();
	});

	jQuery('#sel-hotspot').click(function(){
		jQuery('#map').show()
		jQuery.get( 'https://ebird.org/ws1.1/ref/hotspot/region?fmt=xml&r='+ sel_loc.getValue() , function( xml ) {
			var json = jQuery.parseJSON(xml2json(xml).replace('undefined',''))
			if (json.response.result){
				layer.clearLayers();
				var hotspots=json.response.result.location;
				if (!Array.isArray(hotspots)){ 
					hotspots = [hotspots] 
				}
				hotspots.forEach(function(h){
					var mark = L.marker([h.lat,h.lng],{
						title: h['loc-name'],
						alt: h['loc-name'],
						icon: L.icon({
							iconUrl: "https://zoziologie.raphaelnussbaumer.com/wp-content/plugins/improvedBiolovisionVisualisation/hotspot-icon-hotspot.png",
							iconAnchor: [15, 19],
							popupAnchor: [0, -19],
						})
					}).on('click',function(){
						loc = h['loc-id'];
						jQuery('#checklistname').html(h['loc-name']);
						console.log(this)
					})
					/*var popup = jQuery('<div/>') 
					popup.html('\
						Set Location of the Checklist with the eBird hostpot:<br>\
						<button type="button" class="btn btn-default" id="setLocation" title="Define as location of the checklist">'+h['loc-name']+'</button><br>\
						<a href="https://ebird.org/ebird/hotspot/'+h['loc-id']+'" target="_blank" title="See on eBird">View on eBird</a>');
					popup.on('click', '#setLocation', function() {
						form.name = jQuery(this).html();
						jQuery('#f-'+form.id+' #location').val(form.name);
						jQuery('#li-f-'+form.id+' a').html(form.name);
						form.lat = h.lat;
						form.lon = h.lng;
						jQuery.get( 'https://nominatim.openstreetmap.org/reverse?lat='+form.lat.toString()+'&lon='+form.lon.toString(), function( xml ) {
							var json = jQuery.parseJSON(xml2json(xml).replace('undefined',''))
							form.country = json.reversegeocode.addressparts.country_code;
						});
						form.map.closePopup();
					});*/
					mark.addTo(layer);//.bindPopup(popup[0]);
				})
			}
			map.invalidateSize();
			map.fitBounds(layer.getBounds());
		});
	})


	map = L.map('map').setView(L.latLng(46.57591, 7.84956), 8);

	var mapbox = L.tileLayer.provider('MapBox', {
		id: 'rafnuss.npl3amec',
		accessToken: token.mapbox
	}).addTo(map);

	layer = L.markerClusterGroup({
		showCoverageOnHover: false,
		maxClusterRadius: 50,
		spiderfyDistanceMultiplier: 2
	}).addTo(map);

});
