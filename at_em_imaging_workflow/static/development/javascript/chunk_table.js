var $ = django.jQuery;

function draw_chunks(msg) {
    // alert(msg["chunk_sections"]);
    for (chunk_index in msg['chunk_sections']) {
        computed_index = msg['chunk_sections'][chunk_index][0];
        chunk = msg['chunk_sections'][chunk_index][1];
        var chunk_row = $("<tr></tr>");
        var index_td = $("<td></td>").text(computed_index);
        chunk_row.append(index_td);

        for (s in chunk) {
            var section = chunk[s];
            var section_td = $("<td></td>");

            if (section['complete'] == 'T') {
                section_td.css('background-color', 'rgb(150,255,150)');
            } else {
                section_td.css('background-color', 'rgb(255,150,150)');
            }

            var content_span = $("<span></span>").text(section["z"]).prop(
                'title', section["z"]);
            section_td.append(content_span)
            chunk_row.append(section_td);
        }
        $('#chnk_table').append(chunk_row)
        // alert(chunk_index);
    }
}

$(document).ready(function(){
    fetch('/at_em/page_satchel?q=all_chunks', {
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    })
    .then((response) => {
        response.json().then(obj => {
            draw_chunks(obj['message'])
        })
    })
})
