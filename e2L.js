

function RunPython() {

	filtdiv = jQuery( ":radio.radio-filter:checked" ).parent().parent()[0];
	filt_cond = '[\''+filtdiv.querySelector('.freq-period').value+'\']';
	if (filtdiv.querySelector('.freq-period').value != 'year'){
		filt_cond=filt_cond+'['+filtdiv.querySelector('.freq-index').value+']';
	}

	params = {
		code_loc: '',
		project_name: encodeURIComponent(jQuery('#checklistname').html()),
		byear: jQuery('#div-date-begin').val().split('-')[0],
		eyear: jQuery('#div-date-end').val().split('-')[0],
		bmonth: jQuery('#div-date-begin').val().split('-')[1],
		emonth: jQuery('#div-date-end').val().split('-')[1],
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
	window.open("http://zoziologie.raphaelnussbaumer.com/ebird2latex/generate/?" + jQuery.param(params,true))
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



addToMapHotspot = function (){
	jQuery.getJSON( 'https://ebird.org/ws2.0/ref/hotspot/region?fmt=json&r='+ sel_loc.getValue(), function( hotspots ) {
		hotspots = Array.isArray(hotspots) ? hotspots : [hotspots] 
		hotspots.forEach(function(h){
			var mark = L.marker([h.lat,h.lng],{
				title: h.locName,
				alt: h.locName,
				icon: L.icon({
					iconUrl: "https://zoziologie.raphaelnussbaumer.com/assets/eBird2LaTeX/images/hotspot-icon-hotspot.png",
					iconAnchor: [15, 19],
					popupAnchor: [0, -19],
				})
			}).on('click',function(){
				loc = h.locId;
				jQuery('#checklistname').html(h.locName);
				map.panTo(this._latlng);
				this.bindPopup(h.locName+' selected').openPopup();
			})
			mark.addTo(layer);
		})
		map.invalidateSize();
		map.fitBounds(layer.getBounds());
	})
}




var params, sel_loc, LocationList, layer, map, loc;
var newloc=true;

jQuery(document).ready(function(){


	jQuery('.toggle').hide()

	// Date
	jQuery('#div-date-end').val(moment().format("YYYY-MM") );

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

	jQuery('#toggle-location').change( function(){
		if (jQuery(this).is(':checked')){
			jQuery('#map-col').show()
			if (newloc){
				addToMapHotspot()
				newloc=false
			}
		} else{
			jQuery('#map-col').hide()
		}
	})


	$sel_loc = jQuery('#sel-loc').selectize({
		valueField: 'code',
		labelField: 'name',
		searchField: ['name','code'],
		onChange: function(value){
			jQuery('#checklistname').html('Checklist of '+jQuery.grep(LocationList, function(e){ return e.code == value; })[0].name)
			jQuery('.toggle').show()
			jQuery('#toggle-location').bootstrapToggle('off')
			loc = value;
			newloc=true
		}
	});
	sel_loc  = $sel_loc[0].selectize;

	jQuery.get('https://zoziologie.raphaelnussbaumer.com/assets/eBird2LaTeX/LocationList.json',function(data) {
		LocationList = data;
		LocationList.forEach(function(l){
			l.name = l.name + " ("+l.code+")"
		})
		sel_loc.addOption(LocationList)
		sel_loc.updatePlaceholder()//setTextboxValue('Search a location...')
	});


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


	jQuery('#edit-checklistname').click(function(){
		jQuery('#checklistname').focus();
	});
});


