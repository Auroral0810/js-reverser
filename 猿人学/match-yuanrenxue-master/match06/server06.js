const express = require('express');
const app = express();
const encparams = require('./06.js');
var bodyParser = require('body-parser');
 
app.use(bodyParser());
 
app.post('/encrypt',function(req,res){
    var request = req.body;
    console.log('收到客户端消息',request);
    result = encparams.get_m(request['timestamp'],request['count'])
    res.send(result);
}) 

// app.get('/encrypt',function(req,res){
//     console.log('收到客户端消息',req.query);
//     result = encparams.get_m(req.query.timestamp)
//     res.send(result);
// }) 
 
 
app.listen(3000,()=>{
    console.log('开启服务，端口3000');
})