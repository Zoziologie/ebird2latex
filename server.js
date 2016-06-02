//Lets require/import the HTTP module
var http = require('http');
var fs = require('fs');
var url = require('url');
var qs = require('querystring');
var rq = require('request')
var osmosis = require('osmosis');

//Lets define a port we want to listen to
const PORT=8001; 


http.createServer(function(request, response){
	var path = url.parse(request.url).pathname;
	var parms = qs.parse(url.parse(request.url).query);
	if(path=="/pdf"){
		
	}else{
		/*
		fs.readFile('./index.html', function(err, file) {  
			if(err) {  
				throw err; // write an error response or nothing here  
				return;  
			}  
			response.writeHead(200, { 'Content-Type': 'text/html' });  
			response.end(file, "utf-8");
		});
		*/
		response.writeHead(301,
			  {Location:'http://zoziologie.raphaelnussbaumer.com/ebirdtolatex-beta/'}
			);
		response.end()

		alert('hello')
	}
}).listen(PORT);
console.log("server initialized");
