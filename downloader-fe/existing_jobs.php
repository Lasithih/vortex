
<div class="container-fluid">
    <h2>Existing Jobs</h2>
    <br/>

    <?php

    include_once("db_access.php");
    include_once("job.php");

    $dbaccess = new db_access();
        $jobs = $dbaccess->get_existing_jobs();

    ?>
    <table class="table">
        <thead class="thead-dark">
        <tr>
            <th scope="col">Job ID</th>
            <th scope="col">URL</th>
            <th scope="col">Path</th>
            <th scope="col">Off Peak</th>
            <th scope="col">Type</th>
            <th scope="col">Status</th>
            <th scope="col">Comment</th>
            <th scope="col"></th>
        </tr>
        </thead>
        <tbody>

        <?php
            foreach ($jobs as $job) {
                if($job->status == 0) {
                    echo "<tr class='table-warning'>";
                } else if($job->status == 1) {
                    echo "<tr class='table-primary'>";
                } else if($job->status == 2) {
                    echo "<tr class='table-danger'>";
                } else if($job->status == 3) {
                    echo "<tr class='table-success'>";
                } else {
                    echo "<tr>";
                }
                echo "<th scope=\"row\">". $job->job_id ."</th>";
                echo "<td>". $job->url ."</td>";
                echo "<td>". $job->path ."</td>";
                $offpeak = $job->start_at_midnight == 1 ? "Yes" : "No";
                echo "<td>". $offpeak ."</td>";
                $type = $job->job_type == 0 ? "Youtube" : "Direct";
                echo "<td>". $type ."</td>";
                $status = "Pending";
                if($job->status == 0)
                    $status = "Pending";
                else if($job->status == 1)
                    $status = "Downloading";
                else if($job->status == 2)
                    $status = "Error";
                else if($job->status == 3)
                    $status = "Downloaded";
                echo "<td>". $status ."</td>";
                echo "<td>". $job->comment ."</td>";
                echo '<td><a href="delete.php?id='.$job->job_id.'">Remove</a></td>';
                echo "</tr>";
            }
        ?>
        </tbody>
    </table>
</div>