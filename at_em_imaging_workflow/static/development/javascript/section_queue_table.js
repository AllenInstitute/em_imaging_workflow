var $ = django.jQuery;

function draw_chunks(msg) {
    var qnames = [
    "Generate Render Stack",
    "Generate MIPMaps",
    "Apply MIPMaps",
    "Wait for Lens Correction",
    "Apply Lens Correction",
    "Create Tile Pairs",
    "2D Montage Point Match",
    "2D Montage Solver",
    "Detect Defects",
    "Manual QC / High Degree Polynomial or Point Match Regeneration",
    "Generate Downsampled Montage",
    "Make Montage Scapes",
    "Chunk Assignment"
    ];

    var run_state_class = {
            "PENDING": "run_state_pending",
            "QUEUED": "run_state_queued",
            "RUNNING": "run_state_running",
            "SUCCESS": "run_state_success",
            "FAILED_EXECUTION": "run_state_failed_execution",
            "FAILED": "run_state_failed",
            "PROCESS_KILLED": "run_state_process_killed",
        }; 

    var section_row = $("<tr></tr>");
    var queue_td = $("<td></td>").text('z index');
    section_row.append(queue_td);

    var idx = 0;
    var qlen = qnames.length;
    for (idx = 0; idx < qlen; idx++) {
        queue_td = $("<td></td>").text(qnames[idx]);
        section_row.append(queue_td);

        $('#chnk_table').append(section_row)
    }

    var zlen = msg.length;
    for (var i = 0; i < zlen; i++) {
        section_row = $("<tr></tr>");
        var index_td = $("<td></td>").text(msg[i]['z_index']);
        section_row.append(index_td);
        for (var j = 0; j < qlen; j++) {
            var qname = qnames[j]

            var job_info = msg[i][qname];
            var job_and_state = [null, null]
            if (job_info) {
                job_and_state = msg[i][qname].split('/');
            }
            var job_id = job_and_state[0];
            var state_name = job_and_state[1];
            var em_montage_set_id = job_and_state[2]

            // pandas can't have ints and NaNs in same columns, so convert
            try {
                em_montage_set_id = Math.floor(em_montage_set_id); 
            } catch(err) {
                em_montage_set_id = -1
            }

            var run_state_text = state_name;
            var run_state_td = $("<td></td>");

            if (job_id != null) {
                var run_state_link = $("<a>");
                run_state_link.attr(
                    "href",
                    "/admin/workflow_engine/job/" + job_id);
                run_state_link.attr("title", msg[i]['z_index'])
                run_state_link.text(run_state_text);
                run_state_td.append(run_state_link);
                
                var em_montage_link = $("<a>");
                em_montage_link.attr(
                    "href",
                    "/admin/development/emmontageset/" + em_montage_set_id);
                em_montage_link.text('(' + em_montage_set_id + ')');
                run_state_td.append(em_montage_link);

                // run state and montage set links open in admin tab/window
                run_state_link.attr("target", "workflow_admin");
                em_montage_link.attr("target", "workflow_admin");

                try {
                    run_state_td.attr(
                        'class',
                        run_state_class[run_state_text]);
                } catch (err) {
                    run_state_td.attr('class', 'run_state_unknown');
                }
            }

            section_row.append(run_state_td);
        }
        $('#chnk_table').append(section_row)
    }
}

$(document).ready(function(){
    progress_url = '/at_em/progress.json';
    fetch(progress_url, {
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    })
    .then((response) => {
        response.json().then(msg => {
            draw_chunks(msg)
        })
    })
})
