var IndexViewModel = {
    modal_error: null,
    btn_fetchYoutube: null,
    btn_addYtJob: null,
    txt_youtubeURL: null,
    section_youtubeDetails: null,
    image_youtubeThumbnail: null,
    label_youtubeTitle: null,
    select_youtubeFormat: null,
    select_youtubePreset: null,
    check_downloadOffpeak: null,
    check_directDownloadOffpeak: null,
    txt_directDownloadUrl: null,
    container_youtubeVideoSize: null,
    txt_youtubeVideoSize: null,
    table_jobs: null,
    txt_youtubeStartTime: null,
    txt_youtubeEndTime: null,
    check_youtubeTrimming: null,
    section_youtubeTrimming: null,
    label_youtubeTrimmingWarning: null,

    timer_loadJobs: null,
    timer_loadJobsInterval: 5000
}

var YTJobModel = {
    url: null,
    title: null,
    format: null,
    preset: null,
    isOffPeak: true,
    start_time: null,
    end_time: null,
    jobType: 1,

    reset: function() {
        this.url = null,
        this.title = null,
        this.format = null,
        this.preset = null,
        this.isOffPeak = true,
        this.start_time = null,
        this.end_time = null,
        this.jobType = 1
    }
}

var DDJobModel = {
    url: null,
    isOffPeak: true,
    jobType: 2,

    reset: function() {
        url = null,
        isOffPeak = true,
        jobType = 2
    }
}

$(function() {
    bindViews();

    toastr.options.closeButton = true;
    toastr.options.positionClass = "toastr-position";

    startLoadingJobs();

    IndexViewModel.check_youtubeTrimming.change(function() {
        if(this.checked) {
            enable_trimming();
        } else {
            disable_trimming();
        }
    });
      
});

function bindViews(){
    IndexViewModel.modal_error = $('#modal-error');

    IndexViewModel.btn_fetchYoutube = $('#btn-yt-fetch');
    IndexViewModel.btn_addYtJob = $('#btn-yt-add-job');
    IndexViewModel.txt_youtubeURL = $('#yt-url');
    IndexViewModel.section_youtubeDetails = $('#youtube-details');
    IndexViewModel.image_youtubeThumbnail = $('#yt-thumbnail');
    IndexViewModel.label_youtubeTitle = $('#yt-title');
    IndexViewModel.select_youtubeFormat = $('#yt-format');
    IndexViewModel.select_youtubePreset = $('#yt-preset');
    IndexViewModel.check_downloadOffpeak = $('#yt-offpeak');
    IndexViewModel.check_directDownloadOffpeak = $('#dd-offpeak');
    IndexViewModel.txt_directDownloadUrl = $('#dd-url');
    IndexViewModel.btn_addDdJob = $('#btn-dd-job');
    IndexViewModel.container_youtubeVideoSize = $('#yt-size-container');
    IndexViewModel.txt_youtubeVideoSize = $('#yt-size');
    IndexViewModel.table_jobs = $('#table-jobs');
    IndexViewModel.label_youtubeTrimmingWarning = $('#trimming-warn');

    IndexViewModel.section_youtubeTrimming = $('#yt-section-trim');
    IndexViewModel.check_youtubeTrimming = $('#yt-trimming');
    IndexViewModel.txt_youtubeStartTime = $('#yt-start-time');
    IndexViewModel.txt_youtubeEndTime = $('#yt-end-time');
}

function startLoadingJobs() {
    loadJobs();

    IndexViewModel.timer_loadJobs = setInterval(loadJobs, IndexViewModel.timer_loadJobsInterval);
}

function loadJobs() {
    
    $.ajax({
        type: "GET",
        url: "/api/v1/jobs/list",
        processData: false,
        contentType: "application/json",
        success: function(data, status, xhr) {
            if(data.success) {
                fillJobsTable(data.data);
            } 
        },
        error: function(xhr) {
            var exMessage = typeof xhr.responseJSON.Message == 'undefined' ?
                "Couldn't fetch event types." :
                xhr.responseJSON.Message;
            showErrorToast(exMessage);
        }
    });
}

function fillJobsTable(jobs) {
    var tableContent = "";
    for (let i = 0; i < jobs.length; i++) {
        const job = jobs[i];
        tableRow = "<tr>";
        tableRow += "<th scope='row'>"+job.id+"</th>";
        tableRow += "<td>"+job.url+"</td>";
        tableRow += "<td>"+job.title+"</td>";
        tableRow += "<td>";
        if(job.start_at_midnight === 1) {
            tableRow += "Yes";
        } else {
            tableRow += "No";
        }
        tableRow += "</td>";
        tableRow += "<td>";
        if(job.job_type === 1) {
            tableRow += "Youtube";
        } else {
            tableRow += "Direct Download";
        }
        tableRow += "</td>";
        tableRow += "<td>";
        if(job.status === 1) {
            tableRow += "Pending";
            tableRow = tableRow.replace("<tr>", "<tr class='table-warning'>");
        } else if(job.status === 2) {
            tableRow += "Downloading";
            tableRow = tableRow.replace("<tr>", "<tr class='table-primary'>");
        } else if(job.status === 3) {
            tableRow += "Success";
            tableRow = tableRow.replace("<tr>", "<tr class='table-success'>");
        } else if(job.status === 4) {
            tableRow += "Failed";
            tableRow = tableRow.replace("<tr>", "<tr class='table-danger'>");
        } else {
            tableRow += "Unknown";
        }
        tableRow += "</td>";
        tableRow += "<td>"+job.format+"</td>";
        tableRow += "<td><a href='javascript:removeJob("+job.id+")'>Remove</a></td>";
        tableRow += "</tr>";

        tableContent += tableRow;
    }

    $('#table-body').html(tableContent);
}

function removeJob(id) {
    $.ajax({
        url: "/api/v1/jobs/delete", //the page containing php script
        type: "POST", //request type,
        contentType: "application/json",
        processData: false,
        data: JSON.stringify({'id':id}),
        success: function(result) {
            if(result.success) {
                showSuccessToast("Job Successfully Deleted");
            } else {
                showErrorModal(result.data);
            }
            loadJobs();
        },
        error(e) {
            console.log(e.statusText);
            showErrorModal(e.statusText);
        }
    });
}

//Onclick - start
function fetchYTdata() {
    YTJobModel.reset();

    var url = IndexViewModel.txt_youtubeURL.val();
    if(url === '' || url === null) {
        alert("Enter the URL to continue");
        return;
    }

    if(!validURL(url)) {
        alert("Enter a valid URL to continue");
        return;
    }

    YTJobModel.url = url

    IndexViewModel.btn_addYtJob.prop("disabled",false);
    IndexViewModel.btn_fetchYoutube.prop("disabled",true);
    $.ajax({
        url: "/api/v1/yt/info", //the page containing php script
        type: "GET", //request type,
        dataType: 'json',
        data: {url: url},
        success: function(result) {
            if(result.success) {
                populateYTdetails(result.data);
                IndexViewModel.section_youtubeDetails.show();
            } else {
                IndexViewModel.section_youtubeDetails.hide();
                showErrorModal(result.data);
            }
            IndexViewModel.btn_fetchYoutube.prop("disabled",false);
        },
        error(e) {
            console.log(e.statusText);
            IndexViewModel.btn_fetchYoutube.prop("disabled",false);
            IndexViewModel.section_youtubeDetails.hide();
        }
    });
}

function addYTdownloadJob() {
    YTJobModel.format = IndexViewModel.select_youtubeFormat.val();
    YTJobModel.preset = IndexViewModel.select_youtubePreset.val();
    YTJobModel.isOffPeak = IndexViewModel.check_downloadOffpeak.is(':checked');
    YTJobModel.jobType = 1

    if (IndexViewModel.check_youtubeTrimming.is(':checked')) {
        try {
            YTJobModel.start_time = IndexViewModel.txt_youtubeStartTime.val().toSeconds();
            YTJobModel.end_time = IndexViewModel.txt_youtubeEndTime.val().toSeconds();
        } catch(err) {
            //Show error toast
            console.error(err);
        }
    }

    IndexViewModel.btn_addYtJob.prop("disabled",true);
    $.ajax({
        url: "/api/v1/jobs/save", //the page containing php script
        type: "POST", //request type,
        contentType: "application/json",
        processData: false,
        data: JSON.stringify(YTJobModel),
        success: function(result) {
            if(result.success) {
                resetYTdetails();
                IndexViewModel.section_youtubeDetails.hide();
                showSuccessToast("Job Successfully Added");
            } else {
                showErrorModal(result.data);
            }
            IndexViewModel.btn_addYtJob.prop("disabled",false);
            loadJobs();
        },
        error(e) {
            console.log(e.statusText);
            IndexViewModel.btn_addYtJob.prop("disabled",false);
            showErrorModal(e);
        }
    });
}

function AddDirectDownload() {

    DDJobModel.reset();

    var url = IndexViewModel.txt_directDownloadUrl.val();
    if(url === '' || url === null) {
        alert("Enter the URL to continue");
        return;
    }

    if(!validURL(url)) {
        alert("Enter a valid URL to continue");
        return;
    }

    DDJobModel.url = url;
    DDJobModel.isOffPeak = IndexViewModel.check_directDownloadOffpeak.is(':checked');
    DDJobModel.jobType = 2;

    IndexViewModel.btn_addDdJob.prop("disabled",true);
    $.ajax({
        url: "/api/v1/jobs/save", 
        type: "POST", 
        contentType: "application/json",
        processData: false,
        data: JSON.stringify(DDJobModel),
        success: function(result) {
            if(result.success) {
                showSuccessToast("Job Successfully Added");
            } else {
                showErrorModal(result.data);
            }
            IndexViewModel.btn_addDdJob.prop("disabled",false);
            loadJobs();
        },
        error(e) {
            console.log(e.statusText);
            IndexViewModel.btn_addDdJob.prop("disabled",false);
            showErrorModal(e);
        }
    });
}

//Onclick - end

function fillExtentions(yt_details) {
    var formats = yt_details.formats;
    var extracted = ['mp4','mp3'];

    extracted.forEach(element => {
        var opt = document.createElement("option");
        opt.value = element;
        opt.innerHTML = element;
        IndexViewModel.select_youtubeFormat.append(opt);
    });

    formats.forEach(format => {
        if(!extracted.includes(format.ext)){
            extracted.push(format.ext);
            var opt = document.createElement("option");
            opt.value = format.ext;
            opt.innerHTML = format.ext;
            IndexViewModel.select_youtubeFormat.append(opt);
        }
    });

    fillPresets(yt_details);

    IndexViewModel.select_youtubeFormat.on('change', function() {
        fillPresets(yt_details);
        fillYtPresetSize(yt_details);
        configure_trimming();
    });

    IndexViewModel.txt_youtubeVideoSize.text('N/A');
    IndexViewModel.select_youtubePreset.on('change', function() {
        configure_trimming();
        fillYtPresetSize(yt_details);
    });
}

function configure_trimming() {
    if(IndexViewModel.select_youtubePreset.val() === 'auto' && IndexViewModel.select_youtubeFormat.val() !== 'mp3') {
        disable_trimming_option();
    } else {
        enable_trimming_option();
    }
}

function fillYtPresetSize(yt_details) {

    var selected = IndexViewModel.select_youtubePreset.val();

    if(selected === 'auto'){
        IndexViewModel.container_youtubeVideoSize.hide();
        IndexViewModel.txt_youtubeVideoSize.text('N/A');
        return;
    }

    var preset = yt_details.formats.filter(function(format) {
        return format.format_id == selected;
    })[0];

    if(typeof preset === 'undefined' || typeof preset.filesize === 'undefined' || preset.filesize == null) {
        IndexViewModel.container_youtubeVideoSize.hide();
        IndexViewModel.txt_youtubeVideoSize.text('N/A');
        return;
    }
    IndexViewModel.txt_youtubeVideoSize.text(preset.filesize.fileSize());
    IndexViewModel.container_youtubeVideoSize.show();
}

function fillPresets(yt_details) {
    IndexViewModel.select_youtubePreset.find('option').remove().end().append('<option value="auto" selected>Auto</option>');

    var presets = yt_details.formats.filter(function(format) {
        return format.ext == IndexViewModel.select_youtubeFormat.val();
    });

    presets.forEach(preset => {
        var opt = document.createElement("option");
        opt.value = preset.format_id;
        opt.innerHTML = preset.format;
        IndexViewModel.select_youtubePreset.append(opt);
    });
}


function populateYTdetails(yt_details) {
    resetYTdetails();

    YTJobModel.title = yt_details.title

    IndexViewModel.image_youtubeThumbnail.attr("src",yt_details.thumbnail);
    IndexViewModel.label_youtubeTitle.html(yt_details.title);

    fillExtentions(yt_details);
}

function resetYTdetails() {
    IndexViewModel.container_youtubeVideoSize.hide();
    IndexViewModel.txt_youtubeVideoSize.text("N/A");

    IndexViewModel.image_youtubeThumbnail.attr("src",''); //TODO - Placeholder image
    IndexViewModel.label_youtubeTitle.html('');

    //Clear formats select
    IndexViewModel.select_youtubeFormat.find('option').remove().end();
    IndexViewModel.select_youtubeFormat.off('change');

    //Clear presets select
    IndexViewModel.select_youtubePreset.find('option').remove().end().append('<option value="auto" selected>Auto</option>');

    disable_trimming_option();
}

function enable_trimming() {
    IndexViewModel.txt_youtubeStartTime.removeAttr('disabled');
    IndexViewModel.txt_youtubeEndTime.removeAttr('disabled');
}

function disable_trimming() {
    IndexViewModel.txt_youtubeStartTime.attr('disabled', true);
    IndexViewModel.txt_youtubeEndTime.attr('disabled', true);
    IndexViewModel.txt_youtubeStartTime.val('');
    IndexViewModel.txt_youtubeEndTime.val('');
}

function enable_trimming_option() {
    IndexViewModel.section_youtubeTrimming.removeClass('special-card');
    IndexViewModel.check_youtubeTrimming.removeAttr('disabled');
    IndexViewModel.label_youtubeTrimmingWarning.hide();
}

function disable_trimming_option() {
    IndexViewModel.section_youtubeTrimming.addClass('special-card');
    IndexViewModel.check_youtubeTrimming.attr('disabled', true);
    IndexViewModel.txt_youtubeStartTime.attr('disabled', true);
    IndexViewModel.txt_youtubeEndTime.attr('disabled', true);

    IndexViewModel.check_youtubeTrimming.prop('checked', false);
    IndexViewModel.txt_youtubeStartTime.val('');
    IndexViewModel.txt_youtubeEndTime.val('');

    IndexViewModel.label_youtubeTrimmingWarning.show();
}

// HELPERS
function validURL(str) {
    var pattern = new RegExp('^(https?:\\/\\/)?'+ // protocol
      '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|'+ // domain name
      '((\\d{1,3}\\.){3}\\d{1,3}))'+ // OR ip (v4) address
      '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ // port and path
      '(\\?[;&a-z\\d%_.~+=-]*)?'+ // query string
      '(\\#[-a-z\\d_]*)?$','i'); // fragment locator
    return !!pattern.test(str);
}

Number.prototype.fileSize = function() {

    const gb = 1024 *1024 *1024;
    const mb = 1024 *1024;
    const kb = 1024;

    var val = this.valueOf();
    var str = "";
    var unit = "";

    if(val >= gb) {
        str =  (val/gb).toFixed().toString();
        unit = "GB"

    } else if(val >= mb) {
        str =  (val/mb).toFixed().toString();
        unit = "MB"

    } else if(val >= kb) {
        str =  (val/kb).toFixed().toString();
        unit = "KB"
    } else {
        str =  val.toFixed().toString();
        unit = "B"
    }
    
    var arr = str.split('.');
    if(arr.length === 2) {
        if(arr[1].length > 2) {
            str = arr[0] + '.' + arr[1].slice(0,2);
        }
    }

    return str + ' ' + unit
}

Number.prototype.toFixed = function() {
    var x = this.valueOf();
    if (Math.abs(x) < 1.0) {
      var e = parseInt(x.toString().split('e-')[1]);
      if (e) {
          x *= Math.pow(10,e-1);
          x = '0.' + (new Array(e)).join('0') + x.toString().substring(2);
      }
    } else {
      var e = parseInt(x.toString().split('+')[1]);
      if (e > 20) {
          e -= 20;
          x /= Math.pow(10,e);
          x += (new Array(e+1)).join('0');
      }
    }
    return x;
}

String.prototype.toSeconds = function() {
    var textTime = this.valueOf();
    
    var res = textTime.match(/^[\d]{2}:[\d]{2}:[\d]{2}$/g);
    if(res === null) {
        throw "Wrong time format";
    }

    var arr = textTime.split(':');
    var hours = parseInt(arr[0]);
    var minutes = parseInt(arr[1]);
    var seconds = parseInt(arr[2]);

    return seconds + (minutes * 60) + (hours * 60 * 60)
}

String.prototype.toTime = function() {
    // var textTime = this.valueOf();

    // if(textTime.isNan)
    
    // var res = textTime.match(/^[\d]{2}:[\d]{2}:[\d]{2}$/g);
    // if(res === null) {
    //     throw "Wrong time format";
    // }

    // var arr = textTime.split(':');
    // var hours = parseInt(arr[0]);
    // var minutes = parseInt(arr[1]);
    // var seconds = parseInt(arr[2]);

    // return seconds + (minutes * 60) + (hours * 60 * 60)
}