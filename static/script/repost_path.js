$.getJSON('/static/data/repost_path7.json',function(data) {
    console.log(data.view.nodes.length);
    /*----------------chart 2---------------------*/
    var chart_2 = echarts.init(document.getElementById('graph_2'));
    var convertNode = function (node) {
        console.log(node);
        var res = [];
        for (var i = 0; i < node.length; i++) {
            res.push({
                x: node[i].x,
                y: node[i].y,
                id: node[i].id,
                name: node[i].label,
                symbolSize: node[i].size,
                itemStyle: {
                    normal: {
                        color: 'rgb(' + [
                            Math.round(Math.random() * 160),
                            Math.round(Math.random() * 160),
                            200
                        ].join(',') + ')'
                    }
                }
            });
        }
        console.log(res);
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

    chart_2.setOption({
        title: {
            text: '微博转发网络图',
            left: "center"
        },
        animationDurationUpdate: 1500,
        animationEasingUpdate: 'quinticInOut',
        series: [{
            type: 'graph',
            layout: 'none',
            // progressiveThreshold: 700,
            data: convertNode(data.view.nodes),
            edges: convertEdge(data.view.edges),
            edgeSymbol: ['none', 'arrow'],
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