$.getJSON("/static/data/"+topic+"/map.json",function(data) {
    var chart_7 = echarts.init(document.getElementById('graph_7'), null, {
        renderer: 'canvas'
    });
    chart_7.setOption({
        title: {
            text: '地区分布图',
            left: 'center',
            textStyle: {
				color: '#5CC595',
                fontSize:30
			}
        },
        tooltip: {
            trigger: 'item'
        },
        legend: {
            orient: 'vertical',
            left: 'right',
            top:'bottom',
            data:['参与者地域分布情况']
        },
        visualMap: {
            min: 0,
            max: 100,
            left: 'left',
            top: 'bottom',
            text: ['高','低'],           // 文本，默认为数值文本
            calculable: true,
			inRange: {
				color: ['#F5FFFB','#31A076']	//柱状的颜色，从下到上
			}
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
            data:data.map,
            label: {
                normal: {
                    formatter: '{b}',
                    position: 'right',
                    show: true,
					textStyle: {
						color: '#76B77C'
					}
                },
                emphasis: {
                    show: true
                }
            },
			itemStyle: {
				normal: {
					color: '#76B77C'		//项目的颜色
					//areaColor: '#fff'
				},
				emphasis: {
					areaColor: '#003E3E'   //hover上去的颜色
				}
			}
        }]
    });
});
