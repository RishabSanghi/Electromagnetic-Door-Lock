<?php
   session_start();
   $_SESSION['useradmin']="";
   echo "On logout";
   header("location:index.php");
   session_destroy();
?>
