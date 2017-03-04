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
				color: '#000',
                fontSize:30
			},
			subtext: '查看转发图变化趋势',
			sublink: 'allGraph.html',  //加链接
			subtarget: 'blank',
			subtextStyle: {
				color: '#000',
                fontSize:30
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