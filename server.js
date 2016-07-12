//Lets require/import the HTTP module
var url = require('url');
var PythonShell = require('python-shell');
var express = require('express');

app = express();


app.get('/', function (req, res) {
    res.writeHead(200, { 'Content-Type': 'text/html' });  

    res.write('<div style="background-color: #d7d6d6;position:absolute;top:0;left:0;width:100%;height:100%;">');
    res.write('<div style="max-width:1230px;margin:auto;background-color:white;padding:30px;">')
    res.write('<h1>Python script in progres...</h1>');
    res.write('This should not take more than 1minute');
    res.write('<div style="background-color: black;color: white;padding:20px;overflow:scroll;height:400px;">')
    res.write('<pre>')

    var options = {
        mode: 'text',
        pythonPath: '/usr/bin/python3',
        pythonOptions: ['-u'],
        args: url.parse(decodeURIComponent(req.url)).query
    };

    PythonShell.run('script_web_e2L.py', options, function (err, results) {
        if (err){
            res.write('The python script has fail. Sorry for this. Would you mind reporting the error to rafnuss@gmail.com. Thanks<br><br>Error Traceback:<br>')
            res.write(err.traceback+'<br>');
            return
        }
        res.write('</pre>')
        res.write('</div>')
        res.write('<form action="'+results[results.length-1]+'" target="_blank" style="margin-top:50px;text-align:center;"><button title="Open pdf" type="sumbit">Open generated PDF</button></form>')
        res.write('<form action="'+results[results.length-1].split('.pdf')[0]+'.tex" target="_blank" style="margin-top:50px;text-align:center;"><button title="View the .TeX file" type="sumbit">View the .TeX file</button></form>')
        res.write('</div>')
        res.write('</div>')
        res.end();
        
    }).on('message', function (message) {
        // received a message sent from the Python script (a simple "print" statement)
        res.write(message+'<br>');
    });
});

app.listen(8001, function () {
    console.log('Server lauched: listening to 8001');
});

