/* Project specific Javascript goes here. */

$("#id_sf").change(function () {
//  console.log( $(this).val() );
  if ($(this).val() == "mmgbsa" || $(this).val() == "mmpbsa") {
    $(".center").hide();
    $(".radius").hide();
    $(".size").hide();
    $(".mol2").hide();
    $(".pdb").show();
  } else {
    $(".pdb").hide();
    $(".mol2").show();
  }
  if ($(this).val() == "vina") {
    $(".center").show();
    $(".radius").hide();
    $(".size").show();
  } else if ($(this).val() == "chemplp" || $(this).val() == "plp95" || $(this).val() == "plp") {
    $(".center").show();
    $(".radius").show();
    $(".size").hide();
  }
});


function update_job_name_with_project_name() {
    var x = document.getElementById("id_project_name").value;
    var i = document.getElementById("id_job_name").value.split(" - ");
    document.getElementById("id_job_name").value = x + " - " + i[1];
    document.getElementById("id_job_name_errors").style.display = 'none';
};

function update_job_name_with_protocol() {
    var x = document.getElementById("id_protocol").value;
    var i = document.getElementById("id_job_name").value.split(" - ");
    document.getElementById("id_job_name").value = i[0] + " - " + x;
    document.getElementById("id_job_name_errors").style.display = 'none';
};

function update_required_field() {
    var sf = document.getElementById("id_sf").value
    if ( sf == 'mmgbsa' || sf == 'mmpbsa' ) {
        document.getElementById("id_center_x").required = false;
        document.getElementById("id_center_y").required = false;
        document.getElementById("id_center_z").required = false;

        document.getElementById("id_radius").required = false;

        document.getElementById("id_size_x").required = false;
        document.getElementById("id_size_y").required = false;
        document.getElementById("id_size_z").required = false;
    } else if ( sf == 'vina' ) {
        document.getElementById("id_center_x").required = true;
        document.getElementById("id_center_y").required = true;
        document.getElementById("id_center_z").required = true;

        document.getElementById("id_radius").required = false;

        document.getElementById("id_size_x").required = true;
        document.getElementById("id_size_y").required = true;
        document.getElementById("id_size_z").required = true;
    } else {
        document.getElementById("id_center_x").required = true;
        document.getElementById("id_center_y").required = true;
        document.getElementById("id_center_z").required = true;

        document.getElementById("id_radius").required = true;

        document.getElementById("id_size_x").required = false;
        document.getElementById("id_size_y").required = false;
        document.getElementById("id_size_z").required = false;
    }
};

function reset_sf(){
  document.getElementById('id_sf').value = 'vina';
};
