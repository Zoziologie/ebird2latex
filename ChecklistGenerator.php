Hello world!
<?php
echo "My first PHP script!";
?>


<?php 
$command = escapeshellcmd('/var/www/zoziologie/wp-content/plugins/eBirdToLaTeX-Checklist-Generator/Script_Python.py');
$output = shell_exec($command);
echo $output;

?>
