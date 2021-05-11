<?php
  
    $link = mysqli_connect("localhost", "root", "", "test");
    $link -> set_charset("UTF8"); 

    $PhoneNumber = $_GET["PhoneNumber"];
    $result = $link -> query("SELECT PocketMoney FROM `user` WHERE UserPhoneNumber='$PhoneNumber'");
    while ($row = $result->fetch_assoc()) // 當該指令執行有回傳
    {
        $output[] = $row; // 就逐項將回傳的東西放到陣列中
    }

    // 將資料陣列轉成 Json 並顯示在網頁上，並要求不把中文編成 UNICODE
    print(json_encode($output, JSON_UNESCAPED_UNICODE));
    $link -> close(); // 關閉資料庫連線

?>