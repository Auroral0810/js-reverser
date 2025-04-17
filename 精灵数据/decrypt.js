// 引入CryptoJS库
const CryptoJS = require('crypto-js');

/**
 * 解密数据函数
 * @param {string} encryptedData - 加密的数据
 * @returns {Object} - 解密后的数据对象
 */
function decryptData(encryptedData) {
    // 检查数据是否已经是解密状态
    if (typeof encryptedData === 'object' && encryptedData !== null) {
        return encryptedData;
    }
    
    // IV字符串和密钥
    const j = "DXZWdxUZ5jgsUFPF";
    const z = CryptoJS.enc.Utf8.parse(j);
    
    // 从IV字符串生成IV
    const iv = CryptoJS.enc.Utf8.parse(j.substr(0, 16));
    
    // 使用AES-ECB模式解密
    const decrypted = CryptoJS.AES.decrypt(encryptedData, z, {
        iv: iv,
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7
    });
    
    // 转换为UTF-8字符串并解析JSON
    const decryptedStr = decrypted.toString(CryptoJS.enc.Utf8);
    return JSON.parse(decryptedStr);
}

/**
 * 使用示例
 */
function decrypt(data) {
    return decryptData(data);
}

// 使用方法:
// const decryptedData = decrypt(e.data.data);
// console.log(decryptedData);

module.exports = {
    decryptData,
    decrypt
}; 