const express = require('express');
const skydemo = require('./10.js');

const app = express();

app.get('/m', function (req, res) {
    console.log('收到客户端消息', req.query);
    var querys = req.query;
    var page = querys.page
    var v1 = querys.v1
    var v2 = querys.v2
    var v3 = querys.v3
    var offset = querys.offset
    console.log(page,v1,v2,v3,offset)
    console.log(`/api/match/10?page=${page}`)
    // 接收的参数是字符串需要转成数字，一个细节浪费我2小时，不知道原因的我又去控制流平坦化代码中转了一圈 Number(v1)
    res.send(skydemo.get_m(`/api/match/10?page=${page}`,Number(v1),Number(v2),Number(v3),Number(offset)))

})

app.get('/',(req,res)=>{
    res.send('hello world') 
})

app.listen(3000, () => {
    console.log('开启服务，http://localhost:3000');
})
