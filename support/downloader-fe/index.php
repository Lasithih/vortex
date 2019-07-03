<!DOCTYPE html>
<html>

<head>
    <link rel="stylesheet" type="text/css" href="css/styles.css"/>
    <link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">

    <script src="js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.0/jquery.min.js"></script>

    <script type="text/javascript" src="js/index.js"></script>

</head>





<body>

<header class="bg-primary-color">
    <nav class="bg-primary-color navbar navbar-default" role="navigation">
        <!-- Brand and toggle get grouped for better mobile display -->
        <div class="navbar-header">
            <a class="navbar-brand" href="/">Cobalt Download Manager</a>
        </div>

    </nav>
</header>

<div class="container">
    <br/><br/>
    <form action="submit_job.php" method="post" role="form" class="needs-validation">
        <legend>Add New Download Job</legend>

        <div class="form-group">
            <label for="add_url">URL</label>
            <input type="text" class="form-control" name="add_url" id="add_url" required>
            <div class="invalid-feedback">
                A valid url is required
            </div>
        </div>

        <br/>


        <div id="youtube_container">
            <div class="form-group">
                <label for="download_format">Download Format</label>
                <select class="form-control" name="download_format" id="download_format">
                    <option>mp4</option>
                    <option>mp3</option>
                </select>
            </div>

            <br/>

            <div class="row">
                <div class="form-group col">
                    <label for="input_start_time">Start Time (Optional)</label>
                    <input type="text" class="form-control" name="input_start_time" id="input_start_time" placeholder="hh:mm:ss">
                    <div class="invalid-feedback">
                        Start time is invalid
                    </div>
                </div>

                <div class="form-group col">
                    <label for="input_end_time">End Time (Optional)</label>
                    <input type="text" class="form-control" name="input_end_time" id="input_end_time" placeholder="hh:mm:ss">
                    <div class="invalid-feedback">
                        End time is invalid
                    </div>
                </div>
            </div>
        </div>


        <br/>

        <div class="checkbox">
            <label>
                <input type="checkbox" value="off_peak" id="off_peak" name="off_peak" checked>
                Download in off peak hours
            </label>
        </div>

        <br/>

        <div class="form-group">
            <label for="download_type_disabled">Download Type</label>
            <select class="form-control" name="download_type_disabled" id="download_type_disabled" disabled>
                <option value="1">Direct download</option>
                <option value="0">Youtube</option>
            </select>
            <input type="hidden" name="download_type" id="download_type"/>
        </div>

        <br/>

        <div class="form-group">
            <label for="add_url">Password</label>
            <input type="password" class="form-control" name="pwd" id="pwd" placeholder="*******" required>
            <div class="invalid-feedback">
                Please enter a password
            </div>
        </div>

        <br/>

        <button type="submit" class="btn btn-primary">Submit</button>
    </form>
</div>

<br/><br/><br/>


<div id="tableHolder"></div>


</body>

</html>