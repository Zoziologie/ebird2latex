//Lets require/import the HTTP module
var url = require('url');
var PythonShell = require('python-shell');
var express = require('express');

app = express();




app.get('/', function (req, res) {
	res.writeHead(200, { 'Content-Type': 'text/html' });  
	res.write('<link href="/assets/css/main.css" type="text/css" rel="stylesheet" />')
	res.write('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">')
	res.write('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">')
	res.write('<link href="https://zoziologie.raphaelnussbaumer.com/assets/eBird2LaTeX/e2L.css" type="text/css" rel="stylesheet" />')

	res.write('<div class="initial-content"><div id="main" role="main">')
	res.write('<h1>eBird2LaTeX: Python script</h1>');
	res.write('<div class="alert alert-warning" id="info">Status: <b>RUNNING</b> <i class="fa fa-spinner fa-spin" style="font-size:24px"></i><br>');
	res.write('We are currently running the python script on our server with the parameters you choosed. This should take less than a minute.</div>');
	res.write('Python/LaTeX code (scroll to bottom if needed):')
	res.write('<br><div id="code" style="background-color: black;padding:20px;overflow:scroll;height:400px;">')
	res.write('<pre style="font-size: small; overflow: initial;color: white;">')
	

	var options = {
		mode: 'text',
		pythonPath: '/usr/bin/python3',
		pythonOptions: ['-u'],
		args: url.parse(decodeURIComponent(req.url)).query
	};

	PythonShell.PythonShell.run('script_web_e2L.py', options, function (err, results) {
		if (err){
			res.write(err.traceback+'<br>');
			res.write('</pre>')
			res.write('</div>')
			res.write('<script>');
			res.write('var element = document.getElementById("code");')
			res.write('element.scrollTop = element.scrollHeight;');
			res.write('var info = document.getElementById("info");');
			res.write('info.classList.add("alert-danger");');
			res.write('info.classList.remove("alert-warning");');
			res.write('info.innerHTML = "Status: <b>FAILURE</b> <i class=\'fa fa-exclamation-triangle\'></i><br> The python script has failed, sorry for this. Would you mind reporting this error to <a href=\'mailto:rafnuss@gmail.com?subject=Error with eBird2LaTeX&body=Hi Raphael, I got an issue when trying to generate a checklist with eBird2LaTeX with the following url:"+ encodeURIComponent(window.location.href)+". \'>rafnuss@gmail.com</a> by simply providing the url?";');
			//res.write("$('.alert').after("+link+")");
			res.write('</script>');
			res.end();
			return
		} else {
			res.write('</pre>')
			res.write('</div>')
			res.write('<form action="'+results[results.length-1]+'" target="_blank" style="margin-top:50px;text-align:center;"><button title="Open pdf" type="sumbit">Open generated PDF</button></form>');
			res.write('<form action="'+results[results.length-1].split('.pdf')[0]+'.tex" target="_blank" style="margin-top:50px;text-align:center;"><button title="View the .TeX file" type="sumbit">View the .TeX file</button></form>')
			res.write('<embed src="'+results[results.length-1]+'" type="application/pdf" width="100%" height="600px" />')
			res.write('<script>');
			res.write('var element = document.getElementById("code");')
			res.write('element.scrollTop = element.scrollHeight;');
			res.write('var info = document.getElementById("info");');
			res.write('info.classList.add("alert-success");');
			res.write('info.classList.remove("alert-warning");');
			res.write('info.innerHTML = "Status: <b>SUCCESS</b> <i class=\'fa fa-check\'></i><br> The python code finished successfully. Download the PDF with the button below the code.";');
			//res.write("$('.alert').after("+link+")");
			res.write('</script>');
			res.end();
		}


	}).on('message', function (message) {
		// received a message sent from the Python script (a simple "print" statement)
		res.write(message+'<br>');
	});
});

app.listen(8001, function () {
	console.log('Server lauched: listening to 8001');
});

