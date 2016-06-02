Hello world!
<?php
echo "My first PHP script!";
?>


<?php 

   $item='example';
   $tmp = exec("python /var/www/zoziologie/wp-content/plugins/eBirdToLaTeX-Checklist-Generator/script_e2L.py .$item");
    echo $tmp;

//$command = escapeshellcmd('/var/www/zoziologie/wp-content/plugins/eBirdToLaTeX-Checklist-Generator/Script_Python.py');
//$output = shell_exec($command);
//echo $output;

?>
