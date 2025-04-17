// // 1js 混淆_源码乱码赛.先对s应用d1函数，得到d
// var s = "LBctVlQ7NS46OAYrXDZ3cwNmAwQVcDBdICshOT8mEHUjRzFdHGwlNToxNjBZMTAWXjtVVU07O1wEKiFvbB5vY3VBJV9vICc3LTJ7eGMYeWtRO0REViA1RigRICIjK1Y8dQ8fZRxsNTU6NXt4D3NleQR4FFtLNjFAb3R/fHpnQTs2RzAaCn5qeCQoNCtMZ294Aik="

// var _keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
// var _p = "W5D80NFZHAYB8EUI2T649RT2MNRMVE2O"

function d1(e) {
    var t, n, r, o, i, a, u = "", c = 0;
    for (e = e.replace(/[^A-Za-z0-9\+\/\=]/g, ""); c < e.length; )
        t = _keyStr.indexOf(e.charAt(c++)) << 2 | (o = _keyStr.indexOf(e.charAt(c++))) >> 4,
        n = (15 & o) << 4 | (i = _keyStr.indexOf(e.charAt(c++))) >> 2,
        r = (3 & i) << 6 | (a = _keyStr.indexOf(e.charAt(c++))),
        u += String.fromCharCode(t),
        64 != i && (u += String.fromCharCode(n)),
        64 != a && (u += String.fromCharCode(r));
    return u
}
// // 调用d1函数对s进行解码
// var d = d1(s);

function _u_d(e) {
    for (var t = "", n = 0, r = 0, o = 0, i = 0; n < e.length; )
        (r = e.charCodeAt(n)) < 128 ? (t += String.fromCharCode(r),
        n++) : r > 191 && r < 224 ? (o = e.charCodeAt(n + 1),
        t += String.fromCharCode((31 & r) << 6 | 63 & o),
        n += 2) : (o = e.charCodeAt(n + 1),
        i = e.charCodeAt(n + 2),
        t += String.fromCharCode((15 & r) << 12 | (63 & o) << 6 | 63 & i),
        n += 3);
    return t
}

function d2(e) {
    for (var t = "", n = 0; n < e.length; n++) {
        var r = _p.charCodeAt(n % _p.length);
        t += String.fromCharCode(e.charCodeAt(n) ^ r)
    }
    return t = _u_d(t)
}

// // 3访问逻辑_推心置腹赛.对d应用d2函数，得到y
// var y = d2(d);
// // 3.将y转换为json对象
// var v = JSON.parse(y);
// console.log(v);

//
// // s.payload先进行u.d（e1函数）加密再进行u.c(e2函数)加密得到最终的加密结果
// // p通过对f使用sig函数加密得到。
// // r = 1js 混淆_源码乱码赛.
const md5 = require('md5');

// Base64字符映射表
var _keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
// 密钥
var _p = "W5D80NFZHAYB8EUI2T649RT2MNRMVE2O";

// Base64编码函数
function e1(e) {
    if (null == e)
        return null;
    for (var t, n, r, o, i, a, u, c = "", l = 0; l < e.length; )
        o = (t = e.charCodeAt(l++)) >> 2,
        i = (3 & t) << 4 | (n = e.charCodeAt(l++)) >> 4,
        a = (15 & n) << 2 | (r = e.charCodeAt(l++)) >> 6,
        u = 63 & r,
        isNaN(n) ? a = u = 64 : isNaN(r) && (u = 64),
        c = c + _keyStr.charAt(o) + _keyStr.charAt(i) + _keyStr.charAt(a) + _keyStr.charAt(u);
    return c
}

// XOR加密函数
function e2(e) {
    if (null == (e = _u_e(e)))
        return null;
    for (var t = "", n = 0; n < e.length; n++) {
        var r = _p.charCodeAt(n % _p.length);
        t += String.fromCharCode(e.charCodeAt(n) ^ r)
    }
    return t
}

// 签名函数
function sig(e) {
    return md5(e + _p).toUpperCase()
}

// UTF-8编码函数
function _u_e(e) {
    if (null == e)
        return null;
    e = e.replace(/\r\n/g, "\n");
    for (var t = "", n = 0; n < e.length; n++) {
        var r = e.charCodeAt(n);
        r < 128 ? t += String.fromCharCode(r) : r > 127 && r < 2048 ? (t += String.fromCharCode(r >> 6 | 192),
        t += String.fromCharCode(63 & r | 128)) : (t += String.fromCharCode(r >> 12 | 224),
        t += String.fromCharCode(r >> 6 & 63 | 128),
        t += String.fromCharCode(63 & r | 128))
    }
    return t
}

// // 要加密的数据 - 这里是公司代码列表
// var s = {
//     "payload": {"codes": ['UEIV8197', 'hangzhouwoleikeji', 'dazujiqiren', '9F4EBX6Y', 'meiqiamande', '6G1X74EL', 'szhgxzhnkj79', 'WeAI', 'kbtCOBOT', 'wanyujixie']}
// }


// // 5. 对payload字符串进行e1和e2加密
// var encrypted_payload = e1(e2(JSON.stringify(s.payload)));

// // 6. 对加密后的payload生成签名
// var signature = sig(encrypted_payload);

// // 7. 构建最终的请求参数
// var requestParams = {
//     payload: encrypted_payload,
//     sig: signature,
//     v: 1js 混淆_源码乱码赛
// };

// // 输出结果
// console.log(JSON.stringify(requestParams));




