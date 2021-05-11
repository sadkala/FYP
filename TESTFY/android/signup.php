<?php
require "DataBase.php";
$db = new DataBase();
if(isset($_POST['UserPhoneNumber']) && isset($_POST['Password']) ){
    if($db->dbConnect()){
        if($db->signUp("user",$_POST['UserPhoneNumber'],$_POST['Password'])){
            echo "Sign Up success";
        }else echo "Sign Up Failed";
    }else echo "Error:Database connection";
}else echo "All fields are required";
?>