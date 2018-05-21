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

    var section_row = $("<tr></tr>");
    var queue_td = $("<td></td>").text('z index');
    section_row.append(queue_td);

    var idx = 0;
    var qlen = qnames.length;
    for (idx = 0; idx < qlen; idx++) {
//        chunk = msg['chunk_sections'][chunk_index][1];
        queue_td = $("<td></td>").text(qnames[idx]);
        section_row.append(queue_td);

        $('#chnk_table').append(section_row)
    }

    var zlen = msg.length;
    for (var i = 0; i < zlen; i++) {
        section_row = $("<tr></tr>");
        var index_td = $("<td></td>").text(msg[i]['section']);
        section_row.append(index_td);
    for (var j = 0; j < qlen; j++) {
        var qname = qnames[j]
        var run_state_text = msg[i][qname]
        var run_state_td = $("<td></td>").text(run_state_text);
            if (run_state_text == 'SUCCESS') {
                run_state_td.css('background-color', 'rgb(150,255,150)');
            } else if (run_state_text == 'QUEUED') {
                run_state_td.css('background-color', 'rgb(255,255,150)');
            } else {
                run_state_td.css('background-color', 'rgb(255,150,150)');
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
