var DB = {
    config: {
        api: {}
    },

    renderDashBoard: function() {
        require(['echarts', 'echarts/chart/bar', 'echarts/chart/line', 'echarts/chart/map'],
        function(ec) {
            //--- 折柱 ---
            var myChart = ec.init(document.getElementById('main'));
            myChart.setOption({
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data: ['蒸发量', '降水量']
                },
                toolbox: {
                    show: true,
                    feature: {
                        mark: {
                            show: true
                        },
                        dataView: {
                            show: true,
                            readOnly: false
                        },
                        magicType: {
                            show: true,
                            type: ['line', 'bar']
                        },
                        restore: {
                            show: true
                        },
                        saveAsImage: {
                            show: true
                        }
                    }
                },
                calculable: true,
                xAxis: [{
                    type: 'category',
                    data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
                }],
                yAxis: [{
                    type: 'value',
                    splitArea: {
                        show: true
                    }
                }],
                series: [{
                    name: '蒸发量',
                    type: 'bar',
                    data: [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
                },
                {
                    name: '降水量',
                    type: 'bar',
                    data: [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
                }]
            });

            // --- 地图 ---
            if(!document.getElementById('mainMap')){
                return;
            }

            var myChart2 = ec.init(document.getElementById('mainMap'));
            myChart2.setOption({
                tooltip: {
                    trigger: 'item',
                    formatter: '{b}'
                },
                series: [{
                    name: '中国',
                    type: 'map',
                    mapType: 'china',
                    selectedMode: 'multiple',
                    itemStyle: {
                        normal: {
                            label: {
                                show: true
                            }
                        },
                        emphasis: {
                            label: {
                                show: true
                            }
                        }
                    },
                    data: [{
                        name: '广东',
                        selected: true
                    }]
                }]
            });
        });
    },

    userIdentity: function() {
        var genderChartOption = {
            title : {
                text: '性别',
                subtext: '',
                x:'center'
            },
            tooltip : {
                show: true,
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                orient : 'vertical',
                x : 'left',
                y : '60',
                data:['男','女']
            },
            toolbox: {
                show : true,
                feature : {
                    mark : {show: false},
                    dataView : {show: false, readOnly: false},
                    magicType : {
                        show: false,
                        type: ['pie', 'funnel'],
                        option: {
                            funnel: {
                                x: '25%',
                                width: '50%',
                                funnelAlign: 'center',
                                max: 1548
                            }
                        }
                    },
                    restore : {show: true},
                    saveAsImage : {show: true}
                }
            },
            calculable : true,
            series : [
                {
                    name:'性别',
                    type:'pie',
                    radius : ['50%', '65%'],
                    itemStyle : {
                        normal : {
                            label : {
                                show : false
                            },
                            labelLine : {
                                show : false
                            }
                        },
                        emphasis : {
                            label : {
                                show : true,
                                position : 'center',
                                textStyle : {
                                    fontSize : '30',
                                    fontWeight : 'bold'
                                }
                            }
                        }
                    },
                    data:[
                        {value:335, name:'男'},
                        {value:310, name:'女'}
                    ]
                }
            ]
        };

        var ageOption = {
            title : {
                text: '年龄',
                subtext: '',
                x:'center'
            },
            tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                orient : 'vertical',
                x : 'right',
                y : '60',
                data:['55以上','35-55','16-35','16岁一下']
            },
            toolbox: {
                show : true,
                feature : {
                    mark : {show: true},
                    dataView : {show: true, readOnly: false},
                    magicType : {
                        show: true,
                        type: ['pie', 'funnel'],
                        option: {
                            funnel: {
                                x: '25%',
                                width: '50%',
                                funnelAlign: 'center',
                                max: 1548
                            }
                        }
                    },
                    restore : {show: true},
                    saveAsImage : {show: true}
                }
            },
            calculable : true,
            series : [
                {
                    name:'年龄',
                    type:'pie',
                    radius : ['50%', '70%'],
                    itemStyle : {
                        normal : {
                            label : {
                                show : false
                            },
                            labelLine : {
                                show : false
                            }
                        },
                        emphasis : {
                            label : {
                                show : true,
                                position : 'center',
                                textStyle : {
                                    fontSize : '30',
                                    fontWeight : 'bold'
                                }
                            }
                        }
                    },
                    data:[
                        {value:335, name:'55以上'},
                        {value:310, name:'35-55'},
                        {value:234, name:'16-35'},
                        {value:135, name:'16岁一下'}
                    ]
                }
            ]
        };

        var jobMapOption = {
            title: {
                x: 'center',
                text: '职业',
                subtext: '',
                link: ''
            },
            tooltip: {
                trigger: 'item'
            },
            toolbox: {
                show: true,
                feature: {
                    dataView: {show: true, readOnly: false},
                    restore: {show: true},
                    saveAsImage: {show: true}
                }
            },
            calculable: false,
            grid: {
                borderWidth: 0,
                y: 80,
                y2: 60
            },
            xAxis: [
                {
                    type: 'category',
                    show: false,
                    data: ['工程师', '销售', '教师', '学生', '军人', '公务员', '管理人员', '自由职业', '其他']
                }
            ],
            yAxis: [
                {
                    type: 'value',
                    show: false
                }
            ],
            series: [
                {
                    name: '职业',
                    type: 'bar',
                    itemStyle: {
                        normal: {
                            color: function(params) {
                                // build a color map as your need.
                                var colorList = [
                                  '#C1232B','#B5C334','#FCCE10','#E87C25','#27727B',
                                   '#FE8463','#9BCA63','#FAD860','#F3A43B','#60C0DD',
                                   '#D7504B','#C6E579','#F4E001','#F0805A','#26C0C0'
                                ];
                                return colorList[params.dataIndex]
                            },
                            label: {
                                show: true,
                                position: 'top',
                                formatter: '{b}\n{c}'
                            }
                        }
                    },
                    data: [12,21,10,4,12,5,6,5,2],
                    markPoint: {
                        tooltip: {
                            trigger: 'item',
                            backgroundColor: 'rgba(0,0,0,0)'
                        },
                        data: [
                            {xAxis:0, y: 350, name:'工程师', symbolSize:0},
                            {xAxis:1, y: 350, name:'销售', symbolSize:0},
                            {xAxis:2, y: 350, name:'教师', symbolSize:0},
                            {xAxis:3, y: 350, name:'学生', symbolSize:0},
                            {xAxis:4, y: 350, name:'军人', symbolSize:0},
                            {xAxis:5, y: 350, name:'公务员', symbolSize:0},
                            {xAxis:6, y: 350, name:'管理人员', symbolSize:0},
                            {xAxis:7, y: 350, name:'自由职业', symbolSize:0},
                            {xAxis:8, y: 350, name:'其他', symbolSize:0}
                        ]
                    }
                }
            ]
        };

        var professionMapOption = {
            title: {
                x: 'center',
                text: '专业',
                subtext: '',
                link: ''
            },
            tooltip: {
                trigger: 'item'
            },
            toolbox: {
                show: true,
                feature: {
                    dataView: {show: true, readOnly: false},
                    restore: {show: true},
                    saveAsImage: {show: true}
                }
            },
            calculable: false,
            grid: {
                borderWidth: 0,
                y: 80,
                y2: 60
            },
            xAxis: [
                {
                    type: 'category',
                    show: false,
                    data: ['IT', '贸易', '法律', '体育', '医务', '人力', '金融', '建筑', '人文科学', '自然科学', '制造业']
                }
            ],
            yAxis: [
                {
                    type: 'value',
                    show: false
                }
            ],
            series: [
                {
                    name: '专业',
                    type: 'bar',
                    itemStyle: {
                        normal: {
                            color: function(params) {
                                // build a color map as your need.
                                var colorList = [
                                  '#C1232B','#B5C334','#FCCE10','#E87C25','#27727B',
                                   '#FE8463','#9BCA63','#FAD860','#F3A43B','#60C0DD',
                                   '#D7504B','#C6E579','#F4E001','#F0805A','#26C0C0'
                                ];
                                return colorList[params.dataIndex]
                            },
                            label: {
                                show: true,
                                position: 'top',
                                formatter: '{b}\n{c}'
                            }
                        }
                    },
                    data: [12,21,10,4,12,5,6,5,2,3,1],
                    markPoint: {
                        tooltip: {
                            trigger: 'item',
                            backgroundColor: 'rgba(0,0,0,0)'
                        },
                        data: [
                            {xAxis:0, y: 350, name:'IT', symbolSize:0},
                            {xAxis:1, y: 350, name:'贸易', symbolSize:0},
                            {xAxis:2, y: 350, name:'法律', symbolSize:0},
                            {xAxis:3, y: 350, name:'体育', symbolSize:0},
                            {xAxis:4, y: 350, name:'医务', symbolSize:0},
                            {xAxis:5, y: 350, name:'人力', symbolSize:0},
                            {xAxis:6, y: 350, name:'金融', symbolSize:0},
                            {xAxis:7, y: 350, name:'建筑', symbolSize:0},
                            {xAxis:8, y: 350, name:'人文科学', symbolSize:0},
                            {xAxis:9, y: 350, name:'自然科学', symbolSize:0},
                            {xAxis:10, y: 350, name:'制造业', symbolSize:0}
                        ]
                    }
                }
            ]
        };


        require(['echarts', 'echarts/chart/bar', 'echarts/chart/line', 'echarts/chart/map', 'echarts/chart/pie'],
        function(ec) {
            // 性别信息图render
            if(!document.getElementById('genderMap')){
                return;
            }
            var genderChart = ec.init(document.getElementById('genderMap'));
            genderChart.setOption(genderChartOption);

            // 年龄信息图render
            if(!document.getElementById('ageMap')){
                return;
            }
            var ageMap = ec.init(document.getElementById('ageMap'));
            ageMap.setOption(ageOption);

            // 职业信息图render
            if(!document.getElementById('jobMap')){
                return;
            }
            var jobMap = ec.init(document.getElementById('jobMap'));
            jobMap.setOption(jobMapOption);

            // 专业信息图render
            if(!document.getElementById('professionMap')){
                return;
            }
            var professionMap = ec.init(document.getElementById('professionMap'));
            professionMap.setOption(professionMapOption);
        });
    },

    userHobby: function() {
        var hobbyMapOption = {
            title: {
                x: 'center',
                text: '兴趣爱好（未完待完善）',
                subtext: '',
                link: ''
            },
            tooltip : {
                trigger: 'axis',
                showDelay : 0,
                axisPointer:{
                    show: true,
                    type : 'cross',
                    lineStyle: {
                        type : 'dashed',
                        width : 1
                    }
                }
            },
            legend: {
                show: false,
                data:['兴趣爱好']
            },
            toolbox: {
                show : true,
                feature : {
                    mark : {show: true},
                    dataZoom : {show: true},
                    dataView : {show: true, readOnly: false},
                    restore : {show: false},
                    saveAsImage : {show: true}
                }
            },
            xAxis : [
                {
                    type : 'value',
                    splitNumber: 4,
                    scale: true,
                    show: false
                }
            ],
            yAxis : [
                {
                    type : 'value',
                    splitNumber: 4,
                    scale: true,
                    show: false
                }
            ],
            series : [
                {
                    name:'出境游',
                    type:'scatter',
                    symbolSize: function (value){
                        return Math.round(value[2] / 5);
                    },
                    data: [[190,93,501]]
                },
                {
                    name:'爬山',
                    type:'scatter',
                    symbolSize: function (value){
                        return Math.round(value[2] / 5);
                    },
                    data: [[30,93,101]]
                },
                {
                    name:'爬山',
                    type:'scatter',
                    symbolSize: function (value){
                        return Math.round(value[2] / 5);
                    },
                    data: [[-30,-93,101]]
                }
            ]
        };

        require(['echarts', 'echarts/chart/bar', 'echarts/chart/line', 'echarts/chart/map', 'echarts/chart/pie', 'echarts/chart/scatter'],
        function(ec) {
            // 兴趣爱好render
            if(!document.getElementById('hobbyMap')){
                return;
            }
            var hobbyMap = ec.init(document.getElementById('hobbyMap'));
            hobbyMap.setOption(hobbyMapOption);
        });
    },

    userMatrimony: function() {
        var marriageMapOption = {
            title : {
                text: '婚姻情况',
                subtext: '',
                x:'center'
            },
            tooltip : {
                show: true,
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                orient : 'vertical',
                x : 'left',
                y : '60',
                data:['未婚','已婚']
            },
            toolbox: {
                show : true,
                feature : {
                    mark : {show: false},
                    dataView : {show: false, readOnly: false},
                    magicType : {
                        show: false, 
                        type: ['pie', 'funnel'],
                        option: {
                            funnel: {
                                x: '25%',
                                width: '50%',
                                funnelAlign: 'center',
                                max: 1548
                            }
                        }
                    },
                    restore : {show: true},
                    saveAsImage : {show: true}
                }
            },
            calculable : true,
            series : [
                {
                    name:'婚姻情况',
                    type:'pie',
                    radius : ['50%', '65%'],
                    itemStyle : {
                        normal : {
                            label : {
                                show : false
                            },
                            labelLine : {
                                show : false
                            }
                        },
                        emphasis : {
                            label : {
                                show : true,
                                position : 'center',
                                textStyle : {
                                    fontSize : '30',
                                    fontWeight : 'bold'
                                }
                            }
                        }
                    },
                    data:[
                        {value:335, name:'未婚'},
                        {value:310, name:'已婚'}
                    ]
                }
            ]
        };

        var pregnantMapOption = {
            title : {
                text: '怀孕情况',
                subtext: '',
                x:'center'
            },
            tooltip : {
                show: true,
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                orient : 'vertical',
                x : 'left',
                y : '60',
                data:['怀孕中','非孕中']
            },
            toolbox: {
                show : true,
                feature : {
                    mark : {show: false},
                    dataView : {show: false, readOnly: false},
                    magicType : {
                        show: false, 
                        type: ['pie', 'funnel'],
                        option: {
                            funnel: {
                                x: '25%',
                                width: '50%',
                                funnelAlign: 'center',
                                max: 1548
                            }
                        }
                    },
                    restore : {show: true},
                    saveAsImage : {show: true}
                }
            },
            calculable : true,
            series : [
                {
                    name:'怀孕情况',
                    type:'pie',
                    radius : ['50%', '65%'],
                    itemStyle : {
                        normal : {
                            label : {
                                show : false
                            },
                            labelLine : {
                                show : false
                            }
                        },
                        emphasis : {
                            label : {
                                show : true,
                                position : 'center',
                                textStyle : {
                                    fontSize : '30',
                                    fontWeight : 'bold'
                                }
                            }
                        }
                    },
                    data:[
                        {value:35, name:'怀孕中'},
                        {value:310, name:'非孕中'}
                    ]
                }
            ]
        };

        require(['echarts', 'echarts/chart/bar', 'echarts/chart/line', 'echarts/chart/map', 'echarts/chart/pie', 'echarts/chart/scatter'],
        function(ec) {
            // 兴趣爱好render
            if(!document.getElementById('marriageMap')){
                return;
            }
            var marriageMap = ec.init(document.getElementById('marriageMap'));
            marriageMap.setOption(marriageMapOption);

            // 怀孕情况
            if(!document.getElementById('pregnantMap')){
                return;
            }
            var pregnantMap = ec.init(document.getElementById('pregnantMap'));
            pregnantMap.setOption(pregnantMapOption);
        });
    },

    userConsumption: function() {
        var consumerAbilityMapOption = {
            title : {
                x: 'center',
                text: '消费能力',
                subtext: ''
            },
            tooltip : {
                trigger: 'axis'
            },
            legend: {
                show: false,
                data:['2011年']
            },
            toolbox: {
                show : true,
                feature : {
                    mark : {show: true},
                    dataView : {show: true, readOnly: false},
                    magicType: {show: true, type: ['line', 'bar']},
                    restore : {show: true},
                    saveAsImage : {show: true}
                }
            },
            calculable : true,
            xAxis : [
                {
                    type : 'value',
                    boundaryGap : [0, 0.01]
                }
            ],
            yAxis : [
                {
                    type : 'category',
                    data : ['5000以下','5000-10000','10000-20000','20000以上']
                }
            ],
            series : [
                {
                    name:'消费能力',
                    type:'bar',
                    data:[600, 588, 200, 100]
                }
             ]
        };

        var carMapOption = {
            title : {
                text: '有车与否',
                subtext: '',
                x:'center'
            },
            tooltip : {
                show: true,
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                orient : 'vertical',
                x : 'left',
                y : '60',
                data:['无车','有车']
            },
            toolbox: {
                show : true,
                feature : {
                    mark : {show: false},
                    dataView : {show: false, readOnly: false},
                    magicType : {
                        show: false,
                        type: ['pie', 'funnel'],
                        option: {
                            funnel: {
                                x: '25%',
                                width: '50%',
                                funnelAlign: 'center',
                                max: 1548
                            }
                        }
                    },
                    restore : {show: true},
                    saveAsImage : {show: true}
                }
            },
            calculable : true,
            series : [
                {
                    name:'有车与否',
                    type:'pie',
                    radius : ['50%', '65%'],
                    itemStyle : {
                        normal : {
                            label : {
                                show : false
                            },
                            labelLine : {
                                show : false
                            }
                        },
                        emphasis : {
                            label : {
                                show : true,
                                position : 'center',
                                textStyle : {
                                    fontSize : '30',
                                    fontWeight : 'bold'
                                }
                            }
                        }
                    },
                    data:[
                        {value:335, name:'无车'},
                        {value:310, name:'有车'}
                    ]
                }
            ]
        };

        var petMapOption = {
            title : {
                text: '养宠物与否',
                subtext: '',
                x:'center'
            },
            tooltip : {
                show: true,
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                orient : 'vertical',
                x : 'left',
                y : '60',
                data:['养','不养']
            },
            toolbox: {
                show : true,
                feature : {
                    mark : {show: false},
                    dataView : {show: false, readOnly: false},
                    magicType : {
                        show: false,
                        type: ['pie', 'funnel'],
                        option: {
                            funnel: {
                                x: '25%',
                                width: '50%',
                                funnelAlign: 'center',
                                max: 1548
                            }
                        }
                    },
                    restore : {show: true},
                    saveAsImage : {show: true}
                }
            },
            calculable : true,
            series : [
                {
                    name:'养宠物与否',
                    type:'pie',
                    radius : ['50%', '65%'],
                    itemStyle : {
                        normal : {
                            label : {
                                show : false
                            },
                            labelLine : {
                                show : false
                            }
                        },
                        emphasis : {
                            label : {
                                show : true,
                                position : 'center',
                                textStyle : {
                                    fontSize : '30',
                                    fontWeight : 'bold'
                                }
                            }
                        }
                    },
                    data:[
                        {value:335, name:'养'},
                        {value:510, name:'不养'}
                    ]
                }
            ]
        };


        require(['echarts', 'echarts/chart/bar', 'echarts/chart/line', 'echarts/chart/map', 'echarts/chart/pie'],
        function(ec) {
            // 消费能力
            if(!document.getElementById('consumerAbilityMap')){
                return;
            }
            var consumerAbilityMap = ec.init(document.getElementById('consumerAbilityMap'));
            consumerAbilityMap.setOption(consumerAbilityMapOption);

            // 车
            if(!document.getElementById('carMap')){
                return;
            }
            var carMap = ec.init(document.getElementById('carMap'));
            carMap.setOption(carMapOption);

            // 宠物
            if(!document.getElementById('petMap')){
                return;
            }
            var petMap = ec.init(document.getElementById('petMap'));
            petMap.setOption(petMapOption);
        });
    },

    userLocation: function() {
        var locationMapOption = {
            title : {
                text: '地理位置',
                subtext: '搜索指数',
                x:'center'
            },
            tooltip : {
                trigger: 'item'
            },
            legend: {
                show: false,
                orient: 'vertical',
                x:'left',
                data:['搜索指数']
            },
            dataRange: {
                min: 0,
                max: 2500,
                x: 'left',
                y: 'bottom',
                text:['高','低'],           // 文本，默认为数值文本
                calculable : true
            },
            toolbox: {
                show: true,
                orient : 'vertical',
                x: 'right',
                y: 'center',
                feature : {
                    mark : {show: true},
                    dataView : {show: true, readOnly: false},
                    restore : {show: true},
                    saveAsImage : {show: true}
                }
            },
            roamController: {
                show: true,
                x: 'right',
                mapTypeControl: {
                    'china': true
                }
            },
            series : [
                {
                    name: '搜索排名',
                    type: 'map',
                    mapType: 'china',
                    roam: false,
                    itemStyle:{
                        normal:{label:{show:true}},
                        emphasis:{label:{show:true}}
                    },
                    data:[
                        {name: '北京',value: Math.round(Math.random()*1000)},
                        {name: '天津',value: Math.round(Math.random()*1000)},
                        {name: '上海',value: Math.round(Math.random()*1000)},
                        {name: '重庆',value: Math.round(Math.random()*1000)},
                        {name: '河北',value: Math.round(Math.random()*1000)},
                        {name: '河南',value: Math.round(Math.random()*1000)},
                        {name: '云南',value: Math.round(Math.random()*1000)},
                        {name: '辽宁',value: Math.round(Math.random()*1000)},
                        {name: '黑龙江',value: Math.round(Math.random()*1000)},
                        {name: '湖南',value: Math.round(Math.random()*1000)},
                        {name: '安徽',value: Math.round(Math.random()*1000)},
                        {name: '山东',value: Math.round(Math.random()*1000)},
                        {name: '新疆',value: Math.round(Math.random()*1000)},
                        {name: '江苏',value: Math.round(Math.random()*1000)},
                        {name: '浙江',value: Math.round(Math.random()*1000)},
                        {name: '江西',value: Math.round(Math.random()*1000)},
                        {name: '湖北',value: Math.round(Math.random()*1000)},
                        {name: '广西',value: Math.round(Math.random()*1000)},
                        {name: '甘肃',value: Math.round(Math.random()*1000)},
                        {name: '山西',value: Math.round(Math.random()*1000)},
                        {name: '内蒙古',value: Math.round(Math.random()*1000)},
                        {name: '陕西',value: Math.round(Math.random()*1000)},
                        {name: '吉林',value: Math.round(Math.random()*1000)},
                        {name: '福建',value: Math.round(Math.random()*1000)},
                        {name: '贵州',value: Math.round(Math.random()*1000)},
                        {name: '广东',value: Math.round(Math.random()*1000)},
                        {name: '青海',value: Math.round(Math.random()*1000)},
                        {name: '西藏',value: Math.round(Math.random()*1000)},
                        {name: '四川',value: Math.round(Math.random()*1000)},
                        {name: '宁夏',value: Math.round(Math.random()*1000)},
                        {name: '海南',value: Math.round(Math.random()*1000)},
                        {name: '台湾',value: Math.round(Math.random()*1000)},
                        {name: '香港',value: Math.round(Math.random()*1000)},
                        {name: '澳门',value: Math.round(Math.random()*1000)},
                        {name: '兰州',value: Math.round(Math.random()*1000)}
                    ]
                }
            ]
        };

        require(['echarts', 'echarts/chart/bar', 'echarts/chart/line', 'echarts/chart/map'],
        function(ec) {
            // 地理位置
            if(!document.getElementById('locationMap')){
                return;
            }
            var locationMap = ec.init(document.getElementById('locationMap'));
            locationMap.setOption(locationMapOption);
        });
                    
    },

    sceneMap: function() {
        var sceneMapOption = option = {
            title : {
                text: '情景',
                subtext: ''
            },
            tooltip : {
                trigger: 'axis'
            },
            legend: {
                data:['在家','在公司','在上班路上', '在回家路上']
            },
            toolbox: {
                show : true,
                feature : {
                    mark : {show: true},
                    dataView : {show: true, readOnly: false},
                    magicType : {show: true, type: ['line', 'bar', 'stack', 'tiled']},
                    restore : {show: true},
                    saveAsImage : {show: true}
                }
            },
            calculable : true,
            xAxis : [
                {
                    type : 'category',
                    boundaryGap : false,
                    data : [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
                }
            ],
            yAxis : [
                {
                    type : 'value'
                }
            ],
            series : [
                {
                    name:'在家',
                    type:'line',
                    smooth:true,
                    itemStyle: {normal: {areaStyle: {type: 'default'}}},
                    data:[1000, 1200, 2100, 540, 1260, 1830, 1710,1110, 1112, 1121, 1154, 260, 830, 710,1110, 1112, 1121, 1154, 1260, 830, 710,54, 260, 830]
                },
                {
                    name:'在公司',
                    type:'line',
                    smooth:true,
                    itemStyle: {normal: {areaStyle: {type: 'default'}}},
                    data:[1130, 1182, 1434, 1791, 1390, 1130, 1110,1130, 1182, 1434, 1791, 1390, 1130, 1110,1130, 1182, 1434, 1791, 390, 1130, 1110,1130, 1182, 1134]
                },
                {
                    name:'在上班路上',
                    type:'line',
                    smooth:true,
                    itemStyle: {normal: {areaStyle: {type: 'default'}}},
                    data:[1320, 1132, 601, 234, 120, 90, 20,1320, 1132, 601, 234, 120, 90, 20,1320, 1132, 601, 234, 120, 90, 20,456]
                },
                {
                    name:'在回家路上',
                    type:'line',
                    smooth:true,
                    itemStyle: {normal: {areaStyle: {type: 'default'}}},
                    data:[1120, 832, 601, 654, 620, 190, 200,1120, 832, 601, 654, 620, 190, 200,1120, 832, 601, 654, 620, 190, 20,678]
                }
            ]
        };

        require(['echarts', 'echarts/chart/bar', 'echarts/chart/line', 'echarts/chart/map'],
        function(ec) {
            
            if(!document.getElementById('sceneMap')){
                return;
            }
            var sceneMap = ec.init(document.getElementById('sceneMap'));
            sceneMap.setOption(sceneMapOption);
        });
                    
    },

    eventMap: function() {
        
        var eventMapOption = {
            title : {
                text: '事件频次',
                subtext: ''
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                show: false,
                data: ['蒸发量']
            },
            toolbox: {
                show: true,
                feature: {
                    mark: {
                        show: true
                    },
                    dataView: {
                        show: true,
                        readOnly: false
                    },
                    magicType: {
                        show: true,
                        type: ['line', 'bar']
                    },
                    restore: {
                        show: true
                    },
                    saveAsImage: {
                        show: true
                    }
                }
            },
            calculable: true,
            xAxis: [{
                type: 'category',
                data: ['参加艺术活动', '郊游', '在景区吃饭', '看电影', '上课中', '商圈工作中', '户外教练', '室内教练', '购物', '音乐', '戏剧', '讲座', '聚会', '展览', '公益', '旅行', '其他']
            }],
            yAxis: [{
                type: 'value',
                splitArea: {
                    show: true
                }
            }],
            series: [{
                name: '事件频次',
                type: 'bar',
                data: [20, 49, 70, 232, 256, 77, 136, 162, 126, 200, 64, 33,56,78,50,78,43]
            }]
        }

        require(['echarts', 'echarts/chart/bar', 'echarts/chart/line', 'echarts/chart/map'],
        function(ec) {
            //--- 折柱 ---
            if(!document.getElementById('eventMap')){
                return;
            }

            var eventMap = ec.init(document.getElementById('eventMap'));
            eventMap.setOption(eventMapOption);
        })
    },

    init: function() {
        require.config({
            paths: {
                echarts: '../../static/lib/echarts-2.2.7/build/dist'
            }
        });
        //this.renderDashBoard();
        //this.userIdentity();
        //this.userHobby();
        //this.userMatrimony();
        //this.userConsumption();
        //this.userLocation();
        //this.sceneMap();
        //this.eventMap();
    }
};

(function() {
    DB.init();
})();