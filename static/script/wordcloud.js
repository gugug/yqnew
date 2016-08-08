$.getJSON('/static/data/'+topic+'/wordcloud.json',function(data) {
    //console.log(data.npm.nodes.length);
    /*----------------chart 4---------------------*/
        var chart4_data = data.wordCloud;
        $("#graph_4").jQCloud(chart4_data);
});