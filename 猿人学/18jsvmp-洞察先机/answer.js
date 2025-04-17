const CryptoJS = require("crypto-js")

function getEncrypteddata(page) {
    t = Date['parse'](new Date()) / 1000
    secret_key = t.toString(16) + t.toString(16)
    key = iv = CryptoJS.enc.Utf8.parse(secret_key);
    srcs = CryptoJS.enc.Utf8.parse(`${page}|56d400,56d400,56u400,56u400,136u16`);
    let encrypted = CryptoJS.AES.encrypt(srcs, key, {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });
    return {
        page: page,
        t: t,
        v: encrypted.toString(),
    }
}