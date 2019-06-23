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

$id = $_GET['id'];
$dbaccess = new db_access();
$success = $dbaccess->delete($id);

if ($success) {
    echo '<script type="text/javascript">document.getElementById("resultMsg").innerHTML = "Job deleted successfully";</script>';
} else {
    echo '<script type="text/javascript">document.getElementById("resultMsg").innerHTML = "Failed deleting download job";</script>';
}

?>


</body>
</html>