<?php

include_once ("job.php");
include_once ("config.php");

class db_access
{
    private $servername = "localhost";
    private $username = "root";
    private $password = "root";
    private $dbname = "downloads";

    function add_job($url, $off_peak, $download_type, $download_format, $start_time, $end_time) {
        // Create connection
        $conn = new mysqli($this->servername, $this->username, $this->password, $this->dbname);

        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }

        if ($start_time == null) {
            $start = "null";
        } else {
            $start = "'".$start_time."'";
        }

        if ($end_time == null) {
            $end = "null";
        } else {
            $end = "'".$end_time."'";
        }
        $sql = "INSERT INTO jobs (url,start_at_midnight,job_type, format,start_time, end_time) VALUES ('" . $url . "', " . $off_peak .", " . $download_type . ", '" . $download_format . "', " . $start. ", " . $end .")";

        $success = $conn->query($sql);

        $conn->close();
        return $success;
    }

    function get_existing_jobs() {

        // Create connection
        $conn = new mysqli($this->servername, $this->username, $this->password, $this->dbname);

        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }

        $sql = "SELECT * FROM jobs order by job_id desc;";
        $result = $conn->query($sql);

        $jobs = array();
        if ($result->num_rows > 0) {

            $count = 0;
            while($row = $result->fetch_assoc()) {
                $job = new job_t();
                $job->job_id = $row["job_id"];
                $job->url = $row["url"];
                $job->start_at_midnight = $row["start_at_midnight"];
                $job->path = $row["path"];
                $job->job_type = $row["job_type"];
                $job->format = $row["format"];
                $job->status = $row["status"];
                $job->comment = $row["comment"];
                $jobs[$count] = $job;
                $count++;
            }
        }
        $conn->close();
        return $jobs;
    }

    function delete($id) {
        // Create connection
        $conn = new mysqli($this->servername, $this->username, $this->password, $this->dbname);

        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }

        $sql = "DELETE FROM jobs WHERE job_id=". $id;

        $success=$conn->query($sql);

        $conn->close();
        return $success;
    }

}
