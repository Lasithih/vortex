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
    check_downloadOffpeak: null
}

var JobModel = {
    url: null,
    format: null,
    preset: null,
    isOffPeak: true
}

$(function() {
    bindViews();
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
}

//Onclick - start
function fetchYTdata() {
    var url = IndexViewModel.txt_youtubeURL.val();
    if(url === '' || url === null) {
        alert("Enter the URL to continue");
        return;
    }

    if(!validURL(url)) {
        alert("Enter a valid URL to continue");
        return;
    }

    JobModel.url = url

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
            }
            IndexViewModel.btn_fetchYoutube.prop("disabled",false);
        },
        error(e) {
            console.log(e.responseText);
            IndexViewModel.btn_fetchYoutube.prop("disabled",false);
            IndexViewModel.section_youtubeDetails.hide();
        }
    });
}

function addYTdownloadJob() {
    JobModel.format = IndexViewModel.select_youtubeFormat.val();
    JobModel.preset = IndexViewModel.select_youtubePreset.val();
    JobModel.isOffPeak = IndexViewModel.check_downloadOffpeak.is(':checked');

    IndexViewModel.btn_addYtJob.prop("disabled",true);
    $.ajax({
        url: "/api/v1/jobs/save", //the page containing php script
        type: "POST", //request type,
        contentType: "application/json",
        processData: false,
        data: JSON.stringify(JobModel),
        success: function(result) {
            if(result.success) {
                resetYTdetails();
                IndexViewModel.section_youtubeDetails.hide();
                showSuccessModal("Job Successfully Added");
            } else {
                showErrorModal(result.data);
            }
            IndexViewModel.btn_addYtJob.prop("disabled",false);
        },
        error(e) {
            console.log(e.responseText);
            IndexViewModel.btn_addYtJob.prop("disabled",false);
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
    });
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

    IndexViewModel.image_youtubeThumbnail.attr("src",yt_details.thumbnail);
    IndexViewModel.label_youtubeTitle.html(yt_details.title);

    fillExtentions(yt_details);
}

function resetYTdetails() {
    IndexViewModel.image_youtubeThumbnail.attr("src",''); //TODO - Placeholder image
    IndexViewModel.label_youtubeTitle.html('');

    //Clear formats select
    IndexViewModel.select_youtubeFormat.find('option').remove().end();
    IndexViewModel.select_youtubeFormat.off('change');

    //Clear presets select
    IndexViewModel.select_youtubePreset.find('option').remove().end().append('<option value="auto" selected>Auto</option>');
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