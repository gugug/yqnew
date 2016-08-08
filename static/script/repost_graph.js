$.getJSON("/static/data/"+topic+"/name_list.json",function(data) {

    $("#nameList").append('<h4><center>' + data.nameList.join('，') + '</center></h4>')

    /*----------------graph---------------------*/

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
    var legends = function (a) {
        var res = [];
        for (var i = 0; i < a.length; i++) {
            res.push(a[i].name);
        }
        return res;
    };

    $.getJSON("/static/data/"+topic+"/repost_path7.json", function (data) {
        var chart_0 = echarts.init(document.getElementById('graph_0'), null, {
            renderer: 'canvas'
        });
        chart_0.setOption({
            title: {
                text: '最新网络图',
                left: "center"
            },
            legend: {
                top: 'bottom',
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
                categories: data.view.cates,
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

    $.getJSON("/static/data/"+topic+"/repost_path6.json", function (data) {
        var chart_1 = echarts.init(document.getElementById('graph_1'), null, {
            renderer: 'canvas'
        });
        chart_1.setOption({
            title: {
                text: '第一次检测网络图',
                left: "center"
            },
            legend: {
                top: 'bottom',
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
                categories: data.view.cates,
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
        $('#view1').append('<p><center>检测时间：' + data.view.time + "</center></p>");

    });

    $.getJSON("/static/data/"+topic+"/repost_path5.json", function (data) {
        var chart_2 = echarts.init(document.getElementById('graph_2'), null, {
            renderer: 'canvas'
        });
        chart_2.setOption({
            title: {
                text: '第二次检测网络图',
                left: "center"
            },
            legend: {
                top: 'bottom',
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
                categories: data.view.cates,
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
        $('#view2').append('<p><center>检测时间：' + data.view.time + "</center></p>");
    });

    $.getJSON("/static/data/"+topic+"/repost_path4.json", function (data) {
        var chart_3 = echarts.init(document.getElementById('graph_3'), null, {
            renderer: 'canvas'
        });
        chart_3.setOption({
            title: {
                text: '第三次检测网络图',
                left: "center"
            },
            legend: {
                top: 'bottom',
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
                categories: data.view.cates,
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
        $('#view3').append('<p><center>检测时间：' + data.view.time + "</center></p>");
    });

    $.getJSON("/static/data/"+topic+"/repost_path3.json", function (data) {
        var chart_4 = echarts.init(document.getElementById('graph_4'), null, {
            renderer: 'canvas'
        });
        chart_4.setOption({
            title: {
                text: '第四次检测网络图',
                left: "center"
            },
            legend: {
                top: 'bottom',
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
                categories: data.view.cates,
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
        $('#view4').append('<p><center>检测时间：' + data.view.time + "</center></p>");
    });

    $.getJSON("/static/data/"+topic+"/repost_path2.json", function (data) {
        var chart_5 = echarts.init(document.getElementById('graph_5'), null, {
            renderer: 'canvas'
        });
        chart_5.setOption({
            title: {
                text: '第五次检测网络图',
                left: "center"
            },
            legend: {
                top: 'bottom',
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
                categories: data.view.cates,
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
        $('#view5').append('<p><center>检测时间：' + data.view.time + "</center></p>");
    });

    $.getJSON("/static/data/"+topic+"/repost_path1.json", function (data) {
        var chart_6 = echarts.init(document.getElementById('graph_6'), null, {
            renderer: 'canvas'
        });
        chart_6.setOption({
            title: {
                text: '第六次检测网络图',
                left: "center"
            },
            legend: {
                top: 'bottom',
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
                categories: data.view.cates,
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
        $('#view6').append('<p><center>检测时间：' + data.view.time + "</center></p>");
    });
});