/* 
npm install 安装依赖然后node main.js 即可
*/
const getCookie = require("./02");
const axios = require('axios');

async function main() {
    var sums = 0
    for (var page = 1; page < 6; page++) {
        console.log("page:",page)
        let url = 'http://match.yuanrenxue.com/api/match/2?page=' + page;
        let response = await requestData1(url);
        var temp_list = JSON.parse(response).data;
        console.log(temp_list)
        temp_list.forEach(element => {
            sums += element.value;
        });
    }
    console.log(sums)
}


async function requestData1(url) {
    var config = {
        method: 'get',
        url: url,
        headers: {
            'Cookie': getCookie.getCookie(getCookie.getTime()),
            'User-Agent': 'yuanrenxue.project'
        }
    };
    try {
        var response = await axios(config);
        return JSON.stringify(response.data);
    } catch (error) {
        console.log(error);
        return null;
    }
    
}

// test
main();


