$(document).ready(function(){
     var cloudNum = 1;
    $("#item li").on("click",function(event){
        $("#item li").removeClass("item_doclick");
        $(this).addClass("item_doclick");
        var index=$(this).prevAll().length;
        $("div[class='content']").hide();
        //$("#contents div").eq(index).show();
        var id = index +1;
        if(id != "4"){
            $("#graph_4").hide();
        }
        if(id == "4" && cloudNum == 1){
            $.getJSON('/static/data/'+topic+'/wordcloud.json',function(data){
                /*----------------chart 4---------------------*/
                var chart4_data = data.wordCloud;
                $("#graph_4").jQCloud(chart4_data, {shape: "rectangular"});
            });
            cloudNum--;
            console.log(id);
        }
        //$("div[class='content']").hide();
        $("#graph_"+id).show();
    });
});


function HideContent(){
    //$("#graph_1").hide();
    $("#graph_2").hide();
    $("#graph_3").hide();
    $("#graph_4").hide();
    $("#graph_5").hide();
    $("#graph_6").hide();
    $("#graph_7").hide();
}


$.getJSON('/static/data/'+topic+'/repost_path7.json',function(data) {
//    /*----------------chart 2---------------------*/
    var chart_2 = echarts.init(document.getElementById('graph_2'), null, {
        renderer: 'canvas'
    });
    var convertNode = function (node) {
        console.log(node);
        var res = [];
        for (var i = 0; i < node.length; i++) {
            res.push({
                id: node[i].id,
                name: node[i].label,
                category: node[i].cateNum,
                symbolSize: node[i].size,
                /*itemStyle: {
                 normal: {
                 color: 'rgb(' + [
                 Math.round(Math.random() * 160),
                 Math.round(Math.random() * 160),
                 200
                 ].join(',') + ')'
                 }
                 }*/
            });
        }
//            console.log(res);
        return res;
    };
    var convertEdge = function (edge) {
        var res = [];
        for (var i = 0; i < edge.length; i++) {
            res.push({
                source: edge[i].sourceID,
                target: edge[i].targetID
            });
        }
        return res;
    };

    var legends = function (a){
        var res = [];
        for(var i = 0; i < a.length; i++){
            res.push(a[i].name);
        }
        return res;
    };

    chart_2.setOption({
        title: {
            text: '微博转发网络图',
            left: "center",
			textStyle: {
				color: '#5CC595',
                fontSize:28
			},
			subtext: '查看转发图变化趋势',
			sublink: 'repost',  //加链接
			subtarget: 'blank',
			subtextStyle: {
				color: '##5CC595',
                fontSize:16
			},
			itemGap:15
        },
        legend: {
            top:'bottom',
            data: legends(data.view.cates)
        },
        animation: false,
//            animationDurationUpdate: 1500,
//            animationEasingUpdate: 'quinticInOut',
        series: [{
            type: 'graph',
            layout: 'force',
            force: {
//                    repulsion: 500,
                edgeLength: 100
            },
            // progressiveThreshold: 700,
            categories:data.view.cates,
            data: convertNode(data.view.nodes),
            edges: convertEdge(data.view.edges),
            edgeSymbol: ['none', 'arrow'],
            animation: false,
            roam: true,
            draggable: true,
            label: {
                emphasis: {
                    position: 'right',
                    show: true
                }
            },
            roam: true,
            focusNodeAdjacency: true,
            lineStyle: {
                normal: {
                    width: 0.5,
                    curveness: 0.3,
                    opacity: 0.7
                }
            }
        }]
    });
    });
	//$("#graph_2").append(<div id="moreLink">查看转发图变化趋势</div>);

//    /*----------------chart 3---------------------*/
//    $('#demo').perfectScrollbar();
//
//    var w = parseFloat($('li').css("width"));
//    var h = w/5;
//    $('li').css("height",h+'px');
//
//    var chart3_data = data.news;
//    console.log(chart3_data[0].title);
//    var new_list = '';
//    for(var i = 0;i < chart3_data.length; i++){
//        var ne = '<li><div class="img_div"><img src="' + chart3_data[i].img + '"/ ></div><h3><abbr title="'+chart3_data[i].title+'">'+chart3_data[i].title+'</abbr></h3><p><abbr title="'+chart3_data[i].content+'">'+chart3_data[i].content+'</abbr></p></li>';
//        new_list += ne;
//    }
//    $('#news_content').append(new_list);
//    /*var w = parseFloat($('li').css("width"));
//     var h = w/5;
//     $('li').css("height",h+'px');*/
//    $('#Demo').perfectScrollbar('update');
//
//
//
//
//    /*----------------chart 5---------------------*/
//    var chart_5 = echarts.init(document.getElementById('graph_5'));
//    var chart5_data = data.ageDistribution;
//    chart_5.setOption({
//        title: {
//            text: "年龄分布图",
//            left: 'center',
//			textStyle: {
//				color: '#ACE1AF'
//			}
//        },
//        legend: {
//            data: [{
//                name: "分布百分比"
//            }],
//            y: 'bottom',
//            x: 'center',
//            tooltip: {
//                show: true
//            }
//        },
//        tooltip: {
//            formatter: '{a}<br/>{b}: {c}%'
//        },
//        xAxis: {
//            name: "年龄段",
//            data: ['70前','70后', '80后', '90后', '95后','其他'],
//			axisLine: {
//				lineStyle: {
//					color: '#C6CECB'
//				}
//			}
//        },
//        yAxis: {
//            name: "百分比",
//            axisLabel: {
//                formatter: '{value}%'
//            },
//			axisLine: {
//				lineStyle: {
//					color: '#C6CECB'
//				}
//			}
//        },
//        series: [{
//            type: "bar",
//            name: "分布百分比",
//            data: chart5_data,
//            itemStyle: {
//                normal: {
//                    color: "#ACE1AF"
//                }
//            }
//        }]
//    });
//
//    /*----------------chart 6---------------------*/
//    var chart_6 = echarts.init(document.getElementById('graph_6'));
//    var chart6_data = data.socialEmotion;
//    chart_6.setOption({
//        title: {
//            text: "社会情绪分布图",
//            left: 'center',
//			textStyle: {
//				color: '#ACE1AF'
//			}
//        },
//        legend: {
//            x : 'center',
//            y : 'bottom',
//            data: [{
//                name: "分布人数"
//            }],
//            tooltip: {
//                show: true
//            }
//        },
//        tooltip: {
//            formatter: '{a}<br/>{b} : {c}%'
//        },
//        series: [{
//            name: "情绪百分比",
//            type: "pie",
//            radius : [30, 110],
//            center: ['50%','50%'],
//            roseType: "area",
//            data: chart6_data
//        }]
//    });
//
//    /*----------------chart 7---------------------*/
//    var chart_7 = echarts.init(document.getElementById('graph_7'), null, {
//        renderer: 'canvas'
//    });
//    chart_7.setOption({
//        title: {
//            text: '地区分布图',
//            left: 'center',
//            textStyle: {
//				color: '#ACE1AF'
//			}
//        },
//        tooltip: {
//            trigger: 'item'
//        },
//        legend: {
//            orient: 'vertical',
//            left: 'right',
//            top:'bottom',
//            data:['参与者地域分布情况']
//        },
//        visualMap: {
//            min: 0,
//            max: 100,
//            left: 'left',
//            top: 'bottom',
//            text: ['高','低'],           // 文本，默认为数值文本
//            calculable: true,
//			inRange: {
//				color: ['#F5FFFB','#31A076']	//柱状的颜色，从下到上
//			}
//        },
//        toolbox: {
//            show: true,
//            orient: 'vertical',
//            left: 'right',
//            top: 'center',
//            feature: {
//                dataView: {readOnly: false},
//                restore: {},
//                saveAsImage: {}
//            }
//        },
//        series: [{
//            name: '参与者地域分布情况',
//            type: 'map',
////                    coordinateSystem: 'geo',
//            mapType: 'china',
//            roam: false,
//            data:data.map,
//            label: {
//                normal: {
//                    formatter: '{b}',
//                    position: 'right',
//                    show: true,
//					textStyle: {
//						color: '#76B77C'
//					}
//                },
//                emphasis: {
//                    show: true
//                }
//            },
//			itemStyle: {
//				normal: {
//					color: 'green'		//项目的颜色
//					//areaColor: '#fff'
//				},
//				emphasis: {
//					areaColor: '#76B77C'   //hover上去的颜色
//				}
//			}
//        }]
//    });
//
//});