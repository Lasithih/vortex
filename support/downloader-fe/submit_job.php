<html>

<head>

    <?php include_once("db_access.php"); ?>
    <link rel="stylesheet" type="text/css" href="css/styles.css"/>
    <link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">

    <script src="js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.0/jquery.min.js"></script>


</head>


<body>

<header class="bg-primary-color">
    <nav class="bg-primary-color navbar navbar-default" role="navigation">
        <!-- Brand and toggle get grouped for better mobile display -->
        <div class="navbar-header">
            <a class="navbar-brand" href="/">NAS Downloader</a>
        </div>

    </nav>
</header>

<div class="jumbotron justify-content-center text-center">
    <h1 class="display-3" id="resultMsg">Jumbo heading</h1>
    <hr class="my-2">
</div>

<?php

$url = $_POST["add_url"];
$off_peak = 0;
$download_type = $_POST["download_type"];
$pwd = $_POST["pwd"];
$format = $_POST["download_format"];
$start = $_POST["input_start_time"];
$end = $_POST["input_end_time"];

if(!isset($_POST["pwd"]) || $pwd != "123asd123") {
    echo '<script type="text/javascript">document.getElementById("resultMsg").innerHTML = "Invalid password";</script>';
    return;
}

if($start == "") {
    $start = null;
}

if($end == "") {
    $end = null;
}

if(isset($_POST["off_peak"])) {
    $off_peak = 1;
} else {
    $off_peak = 0;
}

$dbaccess = new db_access();
$success = $dbaccess->add_job($url, $off_peak, $download_type, $format, $start, $end);

if ($success) {
    echo '<script type="text/javascript">document.getElementById("resultMsg").innerHTML = "New download job created successfully";</script>';
} else {
    echo '<script type="text/javascript">document.getElementById("resultMsg").innerHTML = "Failed to create a new download job";</script>';
}


?>


</body>
</html>