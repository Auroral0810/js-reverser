const CryptoJS = require('crypto-js');

// 创建必要的对象和变量
window = {};
dd = {
    'a': CryptoJS
};

// AES加密所需的密钥和向量
let kkkk = CryptoJS.enc.Utf8.parse('xxxxxxxxoooooooo');
let iiii = CryptoJS.enc.Utf8.parse('0123456789ABCDEF');

// 核心加密/解密函数
function xxxxoooo(text) {
    let encryptedData = CryptoJS.enc.Utf8.parse(text);
    let decrypted = CryptoJS.AES.decrypt({
        ciphertext: encryptedData
    }, kkkk, {
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7,
        iv: iiii
    });
    return decrypted.toString(CryptoJS.enc.Utf8);
}

// MD5相关函数的简化实现
function md5(string) {
    return CryptoJS.MD5(string).toString();
}

// SHA256函数
function sha256(string) {
    return CryptoJS.SHA256(string).toString();
}

// 重新实现eeee函数
window.eeee = function(text) {
    return md5(text);
};

function getX(time) {
    // 生成加密参数
     var sign = window.eeee('xialuo' + time);
     var x_param = CryptoJS.SHA256(sign + 'xxoo').toString();
     return x_param;
}
function getM(time) {
    return window.eeee('xialuo' + time);
}
function getHeaders(time) {
    var headers = {
        'ts' : time,
        'm' : getM(time)
    }
    return headers;
}
// 生成加密参数
const time = '1744211770195';
const sign = window.eeee('xialuo' + time);
const x_param = CryptoJS.SHA256(sign + 'xxoo').toString();

console.log('时间戳：', time);
console.log('签名：', sign);
console.log('x参数：', x_param);

// 构建URL
const baseURL = "https://example.com/api";
const finalURL = baseURL + "?t=" + time + "&x=" + encodeURIComponent(x_param);
console.log('最终URL：', finalURL);
