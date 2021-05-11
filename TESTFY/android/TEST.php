<?php
  
    $link = mysqli_connect("localhost", "root", "", "test");
    $link -> set_charset("UTF8"); 

    $PlateNumber = $_GET["CarNumber"];
    $result = $link -> query("SELECT MoneyPaid FROM `paycheck` WHERE paycheck.PlateNumber='$PlateNumber'");
   
    while ($row = $result->fetch_assoc()) // 當該指令執行有回傳
    {
        $output[] = $row; // 就逐項將回傳的東西放到陣列中
        $answer = json_encode($output, true);
        
        echo $answer;
    
        header("Location:https://maker.ifttt.com/trigger/Payment_done/with/key/cPuM4Oj7HXzIqLx3nyET2c?value1='$PlateNumber'&value2='$answer'");
        
    }

?>