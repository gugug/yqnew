$.getJSON('/static/data/age_distribution.json',function(data) {
    //console.log(data.npm.nodes.length);
    /*----------------chart 5---------------------*/
    var chart_5 = echarts.init(document.getElementById('graph_5'));
    var chart5_data = data.ageDistribution;
    chart_5.setOption({
        title: {
            text: "年龄分布图",
            left: 'center'
        },
        legend: {
            data: [{
                name: "分布百分比"
            }],
            y: 'bottom',
            x: 'center',
            tooltip: {
                show: true
            }
        },
        tooltip: {
            formatter: '{a}<br/>{b}: {c}%'
        },
        xAxis: {
            name: "年龄段",
            data: ['70前','70后', '80后', '90后', '95后','其他']
        },
        yAxis: {
            name: "百分比",
            axisLabel: {
                formatter: '{value}%'
            }
        },
        series: [{
            type: "bar",
            name: "分布百分比",
            data: chart5_data,
            itemStyle: {
                normal: {
                    color: "#7bbfea"
                }
            }
        }]
    });
})