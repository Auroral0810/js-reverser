/* 启动一个服务用于用于加密时间戳
    使用方法npm install 安装依赖
    node 01server.js 启动服务
    01.py 请求数据
*/
const express = require('express');
const app = express();
const encparams = require('./match01-1');
var bodyParser = require('body-parser');
 
app.use(bodyParser());
 
app.post('/encrypt',function(req,res){
    var request = req.body;
    console.log('收到客户端消息',request);
    result = encparams.hex_md5(request['timestamp'])
    res.send(result);
}) 

app.get('/encrypt',function(req,res){
    console.log('收到客户端消息',req.query);
    result = encparams.hex_md5(req.query.timestamp)
    res.send(result);
}) 
 
 
app.listen(3000,()=>{
    console.log('开启服务，端口3000');
})