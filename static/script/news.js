$.getJSON('/static/data/'+topic+'/news.json',function(data) {
    //console.log(data.npm.nodes.length);
    /*----------------chart 3---------------------*/
    $('#demo').perfectScrollbar();

    var w = parseFloat($('li').css("width"));
    var h = w / 5;
    $('li').css("height", h + 'px');

    var chart3_data = data.news;
    console.log(chart3_data[0].title);
    var new_list = '';
    for (var i = 0; i < chart3_data.length; i++) {
        var ne = '<li><h3><abbr title="' + chart3_data[i].title + '">' + chart3_data[i].title +
            '</abbr></h3><p><abbr title="' + chart3_data[i].post_time + '">' + chart3_data[i].post_time +
            '&nbsp'+ chart3_data[i].origin+'</abbr><p><abbr title="'
            + chart3_data[i].content + '">' + chart3_data[i].content + '</abbr></p></li>';

        new_list += ne;
    }
    $('#news_content').append(new_list);
    var w = parseFloat($('li').css("width"));
    var h = w / 5;
    $('li').css("height", h + 'px');
    $('#Demo').perfectScrollbar('update');
});