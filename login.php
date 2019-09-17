
<?php



$con=mysqli_connect('localhost','pi_username','pi_pwd');

$db=mysqli_select_db($con,'db_name');



if(isset($_REQUEST['adminlog'])){  //Login for Admin

    $u=$_POST['adusn'];
    $p=$_POST['adpass'];
    
   $result=mysqli_query($con,"select * from admin where Username='$u' and Password='$p'");
   if(mysqli_num_rows($result)>0)
   {
	   
	   
	  $t=time();
	  date_default_timezone_set('Asia/Kolkata');
      $current_time = date("Y-m-d h:i:s",$t);
	   
	   $insert  = mysqli_query($con,"INSERT INTO access_log SET user_name = '$u', rfid_presented_datetime = '$current_time'");


		//echo "Redirect to home.php";
     $_SESSION['useradmin']=$u;
    header("location:login_html.php");
    ?>
    <script>
       alert("You have logged in");
    </script>
  <?php
   }
   else
   {
    ?>
    <script>
       alert("Please Sign-Up first");
    </script>
  <?php
   }
  }






?>
