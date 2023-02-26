var ec_center=echarts.init(document.getElementById('center2'),'dark');


var mydata = [{'name': '上海','value':318},{'name': '云南','value': 162}]
// {name: '上海',value: '' },{name: '重庆',value: '' },
// {name: '河北',value: '' },{name: '河南',value: '' },
// {name: '云南',value: '' },{name: '辽宁',value: '' },
// {name: '黑龙江',value: ''},{name: '湖南',value: ''},
// {name: '安徽',value: '' },{name: '山东',value: '' },
// {name: '新疆',value: '500' },{name: '江苏',value: '' },
// {name: '浙江',value: '' },{name: '江西',value: '' },
// {name: '湖北',value: '' },{name: '广西',value: '' },
// {name: '甘肃',value: '' },{name: '山西',value: '' },
// {name: '内蒙古',value: '' },{name: '陕西',value: '' },
// {name: '吉林',value: '' },{name: '福建',value: '' },
// {name: '贵州',value: '' },{name: '广东',value: '' },
// {name: '青海',value: '' },{name: '西藏',value: '' },
// {name: '四川',value: '' },{name: '宁夏',value: '' },
// {name: '海南',value: '' },{name: '台湾',value: '' },
// {name: '香港',value: '' },{name: '澳门',value: '' }
// ];
var ec_center_option = {
backgroundColor: '#333333',
title: {
text: '全国地图大数据',
subtext: '',
x:'left'
},
tooltip : {undefined,
trigger: 'item'
},
            //左侧小导航图标
            visualMap: {
                show : true,
                x: 'left',
                y: 'bottom',
                textStyle:{
                    fontSize:8,
                },
                splitList: [

                    {start: 10000},
                    {start: 100, end: 999},{start: 1000, end: 9999},
                    {start: 10, end: 99},{start: 1, end: 9},
                ],
                color: ['#f34d04', '#f57d04', '#db8324','#f5d09e', '#f6bd43', '#fff1aa']
            },

            //配置属性
            series: [{
                name: '累计确诊人数',
                type: 'map',
                mapType: 'china',
                roam: false, //拖动与缩放
                   itemStyle: {
                       normal: {
                           borderWidth: .5,
                           borderColor: '#009fe8',
                           areaColor: '#ffefd5',

                       },
                       emphasis: {//滑鼠滑过地图高亮相关
                           borderWidth: .5,
                           borderColor: '#4b0082',
                           areaColor: '#fff',
                       },
                   },
                label: {

                            normal: {
                                show: true,  //省份名称
                                fontSize:8
                            },
                            emphasis: {
                                show: true,
                                fontSize: 8
                            }
                        },
                data:[]//数据

                }]
        };


    //使用制定的配置项和数据显示图表
ec_center.setOption(ec_center_option);