//Lets require/import the HTTP module
var url = require('url');
var PythonShell = require('python-shell');
var express = require('express');

app = express();


app.get('/', function (req, res) {
    res.writeHead(200, { 'Content-Type': 'text/html' });  

    res.write('<div style="background-color: #d7d6d6;">');
    res.write('<div style="width:1100px;margin:auto;backgroud-color:white;padding:20px">')
    res.write('<h1>Python script in progres...</h1>');
    res.write('This should not take more than 1minute');
    res.write('<div style="background-color: black;color: white;padding:10px;">')
    res.write('<pre>')

    var options = {
        mode: 'text',
        pythonPath: '/usr/bin/python3',
        pythonOptions: ['-u'],
        args: url.parse(decodeURIComponent(req.url)).query
    };

    PythonShell.run('script_web_e2L.py', options, function (err, results) {
        if (err){
            throw err;
        }
            res.write('</pre>')
            res.write('</div>')
            res.write('</div>')
            res.write('</div>')
    
      res.writeHead(301,
           {Location: results[results.length - 1]
          });
       res.end();
        
    }).on('message', function (message) {
        // received a message sent from the Python script (a simple "print" statement)
        res.write(message+'<br>');
    });
});

app.listen(8001, function () {
    console.log('Server lauched: listening to 8001');
});

