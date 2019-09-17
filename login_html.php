<html>
<head>
<meta name="viewport" content="width=device-width" />
<title>Raspberry Pi WiFi Controlled LED</title>
</head>
       <body>
       <center><h1>Control Door Lock</h1>      
         <form method="get" action="login_html.php">                
            <input type="submit" style = "font-size: 14 pt" value="Open" name="off">
            <input type="submit" style = "font-size: 14 pt" value="Close" name="on">
            <a href="logout.php">  <input type="button" style = "font-size: 14 pt" value="Logout"> </a>
         </form>​​​
            </center>
<?php






    shell_exec("/usr/local/bin/gpio -g mode 13 out");
    if(isset($_GET['off']))
        {
                        echo "Door is Unlocked";
                        shell_exec("/usr/local/bin/gpio -g write 13 0");
        }
            else if(isset($_GET['on']))
            {
                        echo "Door is Locked";
                        shell_exec("/usr/local/bin/gpio -g write 13 1");
            }
?>
   </body>
</html>
