$.getJSON('/static/data/'+topic+'/social_emotion.json',function(data) {
    //console.log(data.npm.nodes.length);
/*----------------chart 6---------------------*/
    var chart_6 = echarts.init(document.getElementById('graph_6'));
    var chart6_data = data.socialEmotion;
    chart_6.setOption({
        title: {
            text: "社会情绪分布图",
            left: 'center',
			textStyle: {
				color: '#5CC595',
                fontSize:30
			}
        },
        legend: {
            x : 'center',
            y : 'bottom',
            data: [{
                name: "分布人数"
            }],
            tooltip: {
                show: true
            }
        },
        tooltip: {
            formatter: '{a}<br/>{b} : {c}%'
        },
        series: [{
            name: "情绪百分比",
            type: "pie",
            radius : [30, 110],
            center: ['50%','50%'],
            roseType: "area",
            data: chart6_data
        }]
    });

});