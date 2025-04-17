blockSize: 16
function c(t, r) {
    return new finalize(t)
}


function _doFinalize() {
    var t = this._data
        , r = t.words
        , n = 8 * this._nDataBytes
        , i = 8 * t.sigBytes;
    return r[i >>> 5] |= 128 << 24 - i % 32,
        r[14 + (i + 64 >>> 9 << 4)] = e.floor(n / 4294967296),
        r[15 + (i + 64 >>> 9 << 4)] = n,
        t.sigBytes = 4 * r.length,
        this._process(),
        this._hash
}

l = {
    stringify: function (e) {
        for (var t = e.words, r = e.sigBytes, n = [], i = 0; i < r; i++) {
            var a = t[i >>> 2] >>> 24 - i % 4 * 8 & 255;
            n.push(String.fromCharCode(a))
        }
        return n.join("")
    },
    parse: function (e) {
        for (var t = e.length, r = [], n = 0; n < t; n++)
            r[n >>> 2] |= (255 & e.charCodeAt(n)) << 24 - n % 4 * 8;
        return new d.init(r, t)
    }
}

function parse(e) {
    return l.parse(unescape(encodeURIComponent(e)))
}

function _append(e) {
    "string" == typeof e && (e = parse(e)),
        this._data.concat(e),
        this._nDataBytes += e.sigBytes
}

function finalize(e) {
    return e && _append(e),
        _doFinalize()
}

var d = (new Date).getTime()
    , h = function (e, t, r) {
    var n = ""
        , i = t
        ,
        a = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"];
    e && (i = Math.round(Math.random() * (r - t)) + t);
    for (var o = 0; o < i; o++) {
        n += a[Math.round(Math.random() * (a.length - 1))]
    }
    return n
}(!1, 16)


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
signature = c("$d6eb7ff91ee257475%1110" + d + h)
signature_par = hashToHex(signature)
console.log(signature)
// console.log(h)
url = 'https://tousu.sina.com.cn/api/index/feed?ts=' + d + '&rs=' + h + '&signature=' + signature_par