function PopulateCountrySelect() {
	var url = 'https://ebird.org/ws1.1/ref/location/list?rtype=country&fmt=xml';
  var sel = document.getElementById('sel-loc-country');
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
      var countries = xhttp.responseXML.getElementsByTagName("country");
      for (var i = 0; i <countries.length; i++) { 
        var opt = document.createElement('option');
        opt.appendChild( document.createTextNode(countries[i].getElementsByTagName("name")[0].childNodes[0].nodeValue) );
        opt.value = countries[i].getElementsByTagName("country-code")[0].childNodes[0].nodeValue;
        sel.appendChild(opt);
      }
    }
  };
  xhttp.open("GET", url, true);
  xhttp.send();
}


var selLocCountry = document.getElementById('sel-loc-country');
selLocCountry.onchange = function(){
	document.getElementById('div-loc-subnat1').style.display = 'inline';
  var url = 'https://ebird.org/ws1.1/ref/location/list?rtype=subnational1&countryCode='+this.value+'&fmt=xml';
  var sel = document.getElementById('sel-loc-subnat1');
  for (var i=sel.length; i; i--) {
    sel.removeChild( sel[i-1] );
  }
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
  	if (xhttp.readyState == 4 && xhttp.status == 200) {
      var subnational1 = xhttp.responseXML.getElementsByTagName("subnational1");
      sel.appendChild(opt);
      for (var i = 0; i <subnational1.length; i++) { 
        var opt = document.createElement('option');
        opt.appendChild( document.createTextNode(subnational1[i].getElementsByTagName("name")[0].childNodes[0].nodeValue) );
        opt.value = subnational1[i].getElementsByTagName("subnational1-code")[0].childNodes[0].nodeValue;
        sel.appendChild(opt);
      }
  	}
  };
  xhttp.open("GET", url, true);
  xhttp.send();
};


var selLocSubnat1 = document.getElementById('sel-loc-subnat1');
selLocSubnat1.onchange = function(){
	document.getElementById('div-loc-subnat2').style.display = 'inline';
  var url = 'https://ebird.org/ws1.1/ref/location/list?rtype=subnational2&subnational1Code='+this.value+'&fmt=xml';
  var sel = document.getElementById('sel-loc-subnat2');
  for (var i=sel.length; i; i--) {
    sel.removeChild( sel[i-1] );
  }
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
  	if (xhttp.readyState == 4 && xhttp.status == 200) {
      var subnational2 = xhttp.responseXML.getElementsByTagName("subnational2");
      sel.appendChild(opt);
      for (var i = 0; i <subnational2.length; i++) { 
        var opt = document.createElement('option');var opt = document.createElement('option');
        opt.appendChild( document.createTextNode(subnational2[i].getElementsByTagName("name")[0].childNodes[0].nodeValue) );
        opt.value = subnational2[i].getElementsByTagName("subnational2-code")[0].childNodes[0].nodeValue;
        sel.appendChild(opt);
      }
  	}
  };
  xhttp.open("GET", url, true);
  xhttp.send();
};




jQuery(document).ready(function(){
	PopulateCountrySelect()
});
