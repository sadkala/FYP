<?php
require "DataBaseConfig.php";

class DataBase
{
    public $connect;
    public $data;
    private $sql;
    protected $servername;
    protected $username;
    protected $password;
    protected $databasename;

    public function __construct()
    {
        $this->connect = null;
        $this->data = null;
        $this->sql = null;
        $dbc = new DataBaseConfig();
        $this->servername = $dbc->servername;
        $this->username = $dbc->username;
        $this->password = $dbc->password;
        $this->databasename = $dbc->databasename;
    }

    function dbConnect()
    {
        $this->connect = mysqli_connect($this->servername, $this->username, $this->password, $this->databasename);
        return $this->connect;
    }

    function prepareData($data)
    {
        return mysqli_real_escape_string($this->connect, stripslashes(htmlspecialchars($data)));
    }

    function logIn($table, $UserPhoneNumber, $Password)
    {
        $UserPhoneNumber = $this->prepareData($UserPhoneNumber);
        $Password = $this->prepareData($Password);
        $this->sql = "select * from " . $table . " where UserPhoneNumber = '" . $UserPhoneNumber . "'";
        $result = mysqli_query($this->connect, $this->sql);
        $row = mysqli_fetch_assoc($result);
        if (mysqli_num_rows($result) != 0) {
            $dbusername = $row['UserPhoneNumber'];
            $dbpassword = $row['Password'];
            if ($dbusername == $UserPhoneNumber && password_verify($Password, $dbpassword)) {
                $login = true;
            } else $login = false;
        } else $login = false;

        return $login;
    }

    function signUp($table, $UserPhoneNumber, $Password)
    {
        $UserPhoneNumber = $this->prepareData($UserPhoneNumber);
        $Password = password_hash($Password, PASSWORD_DEFAULT);
        $this->sql =
            "INSERT INTO " . $table . " (UserPhoneNumber, Password) VALUES ('" . $UserPhoneNumber . "','" . $Password . "')";
        if (mysqli_query($this->connect, $this->sql)) {
            return true;
        } else return false;
    }

}

?>