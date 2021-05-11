<?php
require "DataBase.php";
$db = new DataBase();
if (isset($_POST['UserPhoneNumber']) && isset($_POST['Password'])){
    if($db->dbConnect()){
        if($db->logIn("user",$_POST['UserPhoneNumber'],$_POST['Password'])){
            echo"Login Success";
        }else echo "Username Or Password error";
    }else echo "Error:DataBase connection";
}else echo "All fields are required";
?>