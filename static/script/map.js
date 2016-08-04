$.getJSON("/static/data/map.json",function(data) {
    var chart_7 = echarts.init(document.getElementById('graph_7'), null, {
        renderer: 'canvas'
    });
    chart_7.setOption({
        //                backgroundColor: '#404a59',
        title: {
            text: '地区分布图',
            left: 'center',
            textStyle: {
                color: '#000'
            }
        },
        tooltip: {
            trigger: 'item'
        },
        legend: {
            orient: 'vertical',
            left: 'right',
            top: 'bottom',
            data: ['参与者地域分布情况']
        },
        visualMap: {
            min: 0,
            max: 100,
            left: 'left',
            top: 'bottom',
            text: ['高', '低'],           // 文本，默认为数值文本
            calculable: true
        },
        toolbox: {
            show: true,
            orient: 'vertical',
            left: 'right',
            top: 'center',
            feature: {
                dataView: {readOnly: false},
                restore: {},
                saveAsImage: {}
            }
        },
        series: [{
            name: '参与者地域分布情况',
            type: 'map',
            //                    coordinateSystem: 'geo',
            mapType: 'china',
            roam: false,
            data: data.map,
            label: {
                normal: {
                    formatter: '{b}',
                    position: 'right',
                    show: true
                },
                emphasis: {
                    show: true
                }
            },
        }]
    });
});
