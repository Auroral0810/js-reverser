// 将哈希对象转换为十六进制字符串
function hashToHex(hashObj) {
  const { words, sigBytes } = hashObj;
  
  let hexChars = [];
  for (let i = 0; i < sigBytes / 4; i++) {
    // 获取32位整数并转换为无符号
    const word = words[i];
    // 确保得到8位十六进制字符（32位 = 8个十六进制字符）
    const wordHex = ((word < 0 ? 0x100000000 + word : word).toString(16)).padStart(8, '0');
    hexChars.push(wordHex);
  }
  
  return hexChars.join('');
}

// 测试示例
const testHashObj = {
  "words": [
    -139150184,
    -2109764048,
    5968042,
    54920123,
    906837558,
    477176362,
    1079459614,
    -768177352
  ],
  "sigBytes": 32
};

const hexSignature = hashToHex(testHashObj);
console.log("转换后的签名字符串: " + hexSignature);

// 验证URL
const testUrl = "//tousu.sina.com.cn/api/index/feed?ts=1744607532747&rs=oeSlvfKbEuDtmTI1&signature=" + hexSignature;
console.log("完整URL: " + testUrl); 