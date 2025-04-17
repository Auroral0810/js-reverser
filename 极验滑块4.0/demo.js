const CryptoJS = require('crypto-js');

// 添加 md5 函数定义
function md5(string) {
    return CryptoJS.MD5(string).toString();
}
function generateGUID() {
    // 辅助函数 - 生成一个4位的十六进制字符串
    function generatePart() {
        return (65536 * (1 + Math.random()) | 0).toString(16).substring(1);
    }

    // 连接4个部分形成一个16位的字符串
    return generatePart() + generatePart() + generatePart() + generatePart();
}

function arrayToHex(bytes) {
    const result = [];
    // 遍历字节数组，将每个字节转换为两位十六进制数
    for (let i = 0; i < bytes.length; i++) {
        const byte = bytes[i] & 0xFF; // 确保是 8 位字节
        // 将高 4 位和低 4 位分别转换为十六进制字符
        result.push((byte >>> 4).toString(16)); // 高 4 位
        result.push((byte & 0x0F).toString(16)); // 低 4 位
    }
    // 拼接所有字符并返回
    return result.join('');
}

function createSymmetricalEncryption(options) {
    // 常量定义
    const Sbox = [214, 144, 233, 254, 204, 225, 61, 183, 22, 182, 20, 194, 40, 251, 44, 5, 43, 103, 154, 118, 42, 190, 4, 195, 170, 68, 19, 38, 73, 134, 6, 153, 156, 66, 80, 244, 145, 239, 152, 122, 51, 84, 11, 67, 237, 207, 172, 98, 228, 179, 28, 169, 201, 8, 232, 149, 128, 223, 148, 250, 117, 143, 63, 166, 71, 7, 167, 252, 243, 115, 23, 186, 131, 89, 60, 25, 230, 133, 79, 168, 104, 107, 129, 178, 113, 100, 218, 139, 248, 235, 15, 75, 112, 86, 157, 53, 30, 36, 14, 94, 99, 88, 209, 162, 37, 34, 124, 59, 1, 33, 120, 135, 212, 0, 70, 87, 159, 211, 39, 82, 76, 54, 2, 231, 160, 196, 200, 158, 234, 191, 138, 210, 64, 199, 56, 181, 163, 247, 242, 206, 249, 97, 21, 161, 224, 174, 93, 164, 155, 52, 26, 85, 173, 147, 50, 48, 245, 140, 177, 227, 29, 246, 226, 46, 130, 102, 202, 96, 192, 41, 35, 171, 13, 83, 78, 111, 213, 219, 55, 69, 222, 253, 142, 47, 3, 255, 106, 114, 109, 108, 91, 81, 141, 27, 175, 146, 187, 221, 188, 127, 17, 217, 92, 65, 31, 16, 90, 216, 10, 193, 49, 136, 165, 205, 123, 189, 45, 116, 208, 18, 184, 229, 180, 176, 137, 105, 151, 74, 12, 150, 119, 126, 101, 185, 241, 9, 197, 110, 198, 132, 24, 240, 125, 236, 58, 220, 77, 32, 121, 238, 95, 62, 215, 203, 57, 72];
    const CK = [462357, 472066609, 943670861, 1415275113, 1886879365, 2358483617, 2830087869, 3301692121, 3773296373, 4228057617, 404694573, 876298825, 1347903077, 1819507329, 2291111581, 2762715833, 3234320085, 3705924337, 4177462797, 337322537, 808926789, 1280531041, 1752135293, 2223739545, 2695343797, 3166948049, 3638552301, 4110090761, 269950501, 741554753, 1213159005, 1684763257];

    // 辅助函数
    function convertKeyToUtf8ByteArray(key) {
        const byteArray = [];
        const length = key.length;

        for (let i = 0; i < length; i++) {
            const code = key.charCodeAt(i);
            if (code >= 0x10000 && code <= 0x10FFFF) {
                byteArray.push(((code >> 18) & 0x07) | 0xF0);
                byteArray.push(((code >> 12) & 0x3F) | 0x80);
                byteArray.push(((code >> 6) & 0x3F) | 0x80);
                byteArray.push((code & 0x3F) | 0x80);
            } else if (code >= 0x0800 && code <= 0xFFFF) {
                byteArray.push(((code >> 12) & 0x0F) | 0xE0);
                byteArray.push(((code >> 6) & 0x3F) | 0x80);
                byteArray.push((code & 0x3F) | 0x80);
            } else if (code >= 0x0080 && code <= 0x07FF) {
                byteArray.push(((code >> 6) & 0x1F) | 0xC0);
                byteArray.push((code & 0x3F) | 0x80);
            } else {
                byteArray.push(code);
            }
        }

        return byteArray;
    }

    function rotateLeft(value, bits) {
        return ((value << bits) | (value >>> (32 - bits))) >>> 0;
    }

    function tauTransform(value) {
        return (Sbox[(value >>> 24) & 0xFF] << 24) |
            (Sbox[(value >>> 16) & 0xFF] << 16) |
            (Sbox[(value >>> 8) & 0xFF] << 8) |
            (Sbox[value & 0xFF]);
    }

    function linearTransform2(value) {
        return value ^ rotateLeft(value, 13) ^ rotateLeft(value, 23);
    }

    function tTransform2(value) {
        const tau = tauTransform(value);
        return linearTransform2(tau);
    }

    function spawnEncryptRoundKeys(key) {
        const tempKey = new Array(4);
        const encryptRoundKeys = new Array(32);

        // 将密钥转换为32位整数
        tempKey[0] = (key[0] << 24) | (key[1] << 16) | (key[2] << 8) | key[3];
        tempKey[1] = (key[4] << 24) | (key[5] << 16) | (key[6] << 8) | key[7];
        tempKey[2] = (key[8] << 24) | (key[9] << 16) | (key[10] << 8) | key[11];
        tempKey[3] = (key[12] << 24) | (key[13] << 16) | (key[14] << 8) | key[15];

        const FK = [0xa3b1bac6, 0x56aa3350, 0x677d9197, 0xb27022dc];
        const tempKeys = new Array(36);

        // 初始化前4个临时密钥
        for (let i = 0; i < 4; i++) {
            tempKeys[i] = (tempKey[i] ^ FK[i]) >>> 0;
        }

        // 生成32轮加密密钥
        for (let i = 0; i < 32; i++) {
            tempKeys[i + 4] = (tempKeys[i] ^ tTransform2(
                tempKeys[i + 1] ^ tempKeys[i + 2] ^ tempKeys[i + 3] ^ CK[i]
            )) >>> 0;
            encryptRoundKeys[i] = tempKeys[i + 4];
        }

        return encryptRoundKeys;
    }

    // 主逻辑
    const keyBytes = convertKeyToUtf8ByteArray(options.key);
    if (keyBytes.length !== 16) {
        throw new Error("key should be a 16 bytes string");
    }

    const iv = new Array(16).fill(48);
    const encryptRoundKeys = spawnEncryptRoundKeys(keyBytes);
    const decryptRoundKeys = [...encryptRoundKeys].reverse();

    // 返回结果对象
    return {
        key: keyBytes,
        iv: iv,
        mode: options.mode.toLowerCase() || 'cbc',
        cipherType: 'base64',
        encryptRoundKeys: encryptRoundKeys,
        decryptRoundKeys: decryptRoundKeys
    };
}

var  duicheng1 = function (param1, param2) {
    const key = CryptoJS.enc.Utf8.parse(param2);
    const iv = CryptoJS.enc.Utf8.parse('0000000000000000');

    const encrypted = CryptoJS.AES.encrypt(param1, key, {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });

    // 转换为字节数组
    const words = encrypted.ciphertext.words;
    const sigBytes = encrypted.ciphertext.sigBytes;
    const result = [];

    for (let i = 0; i < sigBytes; i++) {
        const byte = (words[i >>> 2] >>> (24 - (i % 4) * 8)) & 0xff;
        result.push(byte);
    }

    return result;
}

// 首先定义_ᕸᖙᕹᕷ数组
var _ᕸᖙᕹᕷ = [
    null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null,
    null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null,
    null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null,
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
    null, null, null, null, null, null, null,
    10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
    null, null, null, null, null, null,
    10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35
];

function _ᖁᕺᖗᕿ() {
    var rsa = {
        'n': null,
        'e': 0,
        'd': null,
        'p': null,
        'q': null,
        'dmp1': null,
        'dmq1': null,
        'coeff': null
    };

    setPublic.call(rsa, '00C1E3934D1614465B33053E7F48EE4EC87B14B95EF88947713D25EECBFF7E74C7977D02DC1D9451F79DD5D1C10C29ACB6A9B4D6FB7D0A0279B6719E1772565F09AF627715919221AEF91899CAE08C0D686D748B20A3603BE2318CA6BC2B59706592A9219D0BF05C9F65023A21D2330807252AE0066D59CEEFA5F2748EA80BAB81', '10001');

    // 只保留需要的属性
    var result = {
        n: {},
        e: rsa.e,
        d: null,
        p: null,
        q: null,
        dmp1: null,
        dmq1: null,
        coeff: null
    };

    // 复制n的必要属性
    for (var i = 0; i < rsa.n.t; i++) {
        result.n[i] = rsa.n[i];
    }
    result.n.t = rsa.n.t;
    result.n.s = rsa.n.s;

    return result;
}

function setPublic(_ᕶᖉᖃᕾ, _ᕶᕴᕹᕶ) {
    null != _ᕶᖉᖃᕾ && null != _ᕶᕴᕹᕶ && 0 < _ᕶᖉᖃᕾ['length'] && 0 < _ᕶᕴᕹᕶ['length'] ? (this['n'] = function _ᖚᖆᖀᖃ(_ᕶᖉᖃᕾ, _ᕶᕴᕹᕶ) {
        return new b(_ᕶᖉᖃᕾ, _ᕶᕴᕹᕶ)
    }(_ᕶᖉᖃᕾ, 16),
        this['e'] = parseInt(_ᕶᕴᕹᕶ, 16)) : console && console['error'] && console['error']('Invalid RSA public key')
}

function b(_ᕶᖉᖃᕾ, _ᖄᕿᖚᕺ, _ᕶᖆᕷᕵ) {
    this.DB = 28; // 数字位数
    this.DM = (1 << 28) - 1; // 掩码
    this.DV = (1 << 28); // 除数
    this.FV = Math.pow(2, 52);
    this.F1 = 52 - 28;
    this.F2 = 2 * 28 - 52;

    // 初始化数组
    this.t = 0;
    this.s = 0;

    null != _ᕶᖉᖃᕾ && ('number' == typeof _ᕶᖉᖃᕾ ? this.fromNumber(_ᕶᖉᖃᕾ, _ᖄᕿᖚᕺ, _ᕶᖆᕷᕵ) : null == _ᖄᕿᖚᕺ && 'string' != typeof _ᕶᖉᖃᕾ ? this.fromString(_ᕶᖉᖃᕾ, 256) : this.fromString(_ᕶᖉᖃᕾ, _ᖄᕿᖚᕺ));
}

// 将fromString方法添加到b的原型中
b.prototype.fromString = function(_ᕶᖉᖃᕾ, _ᕶᕴᕹᕶ) {
    var _ᖉᕹᕺᖀ;
    if (16 == _ᕶᕴᕹᕶ)
        _ᖉᕹᕺᖀ = 4;
    else if (8 == _ᕶᕴᕹᕶ)
        _ᖉᕹᕺᖀ = 3;
    else if (256 == _ᕶᕴᕹᕶ)
        _ᖉᕹᕺᖀ = 8;
    else if (2 == _ᕶᕴᕹᕶ)
        _ᖉᕹᕺᖀ = 1;
    else if (32 == _ᕶᕴᕹᕶ)
        _ᖉᕹᕺᖀ = 5;
    else {
        if (4 != _ᕶᕴᕹᕶ)
            return void this.fromRadix(_ᕶᖉᖃᕾ, _ᕶᕴᕹᕶ);
        _ᖉᕹᕺᖀ = 2;
    }
    this.t = 0;
    this.s = 0;
    var _ᕺᖗᕾᖗ, _ᕿᕵᖆᕾ, _ᕶᖃᖁᕹ = _ᕶᖉᖃᕾ.length, _ᖗᖂᖉᖁ = !1, _ᕴᕺᖙᕷ = 0;
    while (0 <= --_ᕶᖃᖁᕹ) {
        var _ = 8 == _ᖉᕹᕺᖀ ? 255 & +_ᕶᖉᖃᕾ[_ᕶᖃᖁᕹ] : (_ᕺᖗᕾᖗ = _ᕶᖃᖁᕹ,
            null == (_ᕿᕵᖆᕾ = _ᕸᖙᕹᕷ[_ᕶᖉᖃᕾ.charCodeAt(_ᕺᖗᕾᖗ)]) ? -1 : _ᕿᕵᖆᕾ);
        _ < 0 ? '-' == _ᕶᖉᖃᕾ.charAt(_ᕶᖃᖁᕹ) && (_ᖗᖂᖉᖁ = !0) : (_ᖗᖂᖉᖁ = !1,
            0 == _ᕴᕺᖙᕷ ? this[this.t++] = _ : _ᕴᕺᖙᕷ + _ᖉᕹᕺᖀ > this.DB ? (this[this.t - 1] |= (_ & (1 << this.DB - _ᕴᕺᖙᕷ) - 1) << _ᕴᕺᖙᕷ,
                this[this.t++] = _ >> this.DB - _ᕴᕺᖙᕷ) : this[this.t - 1] |= _ << _ᕴᕺᖙᕷ,
            (_ᕴᕺᖙᕷ += _ᖉᕹᕺᖀ) >= this.DB && (_ᕴᕺᖙᕷ -= this.DB));
    }
    8 == _ᖉᕹᕺᖀ && 0 != (128 & _ᕶᖉᖃᕾ[0]) && (this.s = -1,
        0 < _ᕴᕺᖙᕷ && (this[this.t - 1] |= (1 << this.DB - _ᕴᕺᖙᕷ) - 1 << _ᕴᕺᖙᕷ));
    this.clamp();
    _ᖗᖂᖉᖁ && b.ZERO.subTo(this, this);
}

// 将clamp方法添加到b的原型中
b.prototype.clamp = function() {
    var _ᖀᖄᕴᖄ = this.s & this.DM;
    while (0 < this.t && this[this.t - 1] == _ᖀᖄᕴᖄ)
        --this.t;
}

// 添加subTo方法
b.prototype.subTo = function(a, r) {
    var i = 0, c = 0, m = Math.min(a.t, this.t);
    while (i < m) {
        c += this[i] - a[i];
        r[i++] = c & this.DM;
        c >>= this.DB;
    }
    if (a.t < this.t) {
        c -= a.s;
        while (i < this.t) {
            c += this[i];
            r[i++] = c & this.DM;
            c >>= this.DB;
        }
        c += this.s;
    } else {
        c += this.s;
        while (i < a.t) {
            c -= a[i];
            r[i++] = c & this.DM;
            c >>= this.DB;
        }
        c -= a.s;
    }
    r.s = (c < 0) ? -1 : 0;
    if (c < -1) r[i++] = this.DV + c;
    else if (c > 0) r[i++] = c;
    r.t = i;
    r.clamp();
}

// 添加ZERO静态属性
b.ZERO = new b('0', 16);

function jiamiW(_ᕶᖉᖃᕾ, _ᕶᕴᕹᕶ) {
    var _ᕺᖗᕾᖗ = _ᕶᕴᕹᕶ.options;
    if (!_ᕺᖗᕾᖗ['pt'] || 0 === _ᕺᖗᕾᖗ['pt'])
        return _ᖉᕹᕺᖀ['default']['urlsafe_encode'](_ᕶᖉᖃᕾ);//使用默认加密方式
    var _ᖂᖈᖗᕾ = generateGUID()
        , _ᖆᖚᖉᕾ = {
            //构造两种加密方式
            1: {
                symmetrical: duicheng1, ///对称加密
                asymmetric: _ᖁᕺᖗᕿ() //非对称加密
            },
            // 2: {
            //     symmetrical: createSymmetricalEncryption({
            //         key: '3f89fb970c7a6f62',
            //         mode: 'CBC',
            //         iv: '0000000000000000'
            //     }),
            //     asymmetric: _ᕸᖙᕹᕷ['default'] //非对称加密
            // }
        };
    //下面是实现具体的加密算法
    var a = _ᕺᖗᕾᖗ['pt']
        , _ = '9a7f48cd58889f03739ef234ce0bba198064f480c510b1d56fd569e5fb1329a79cc2342981b8829f46e64cebc2380335b4550767a7005ee98e38efcf4147cffaee508e32e45dc57804f031923ca688fed26611f3a3c3956fb2c8abf29c07cd4b04cd70222d2fa342ce97a52bf87199c6b1128c997901dd476289208b442f9527'
    while ((!_ || 256 !== _.length))
        _ᖂᖈᖗᕾ = generateGUID(),
            _ = '9a7f48cd58889f03739ef234ce0bba198064f480c510b1d56fd569e5fb1329a79cc2342981b8829f46e64cebc2380335b4550767a7005ee98e38efcf4147cffaee508e32e45dc57804f031923ca688fed26611f3a3c3956fb2c8abf29c07cd4b04cd70222d2fa342ce97a52bf87199c6b1128c997901dd476289208b442f9527'
    var u = duicheng1(_ᕶᖉᖃᕾ, _ᖂᖈᖗᕾ); //1的对称加密正确实现；
    return arrayToHex(u) + _
}

function getW(slide_distance, lot_number,captcha_id){
    var params =  {
    "setLeft": slide_distance,
    "passtime": 638,//固定
    "userresponse": slide_distance / 1.0059466666666665 + 2,//userresponse为distance计算得来，等于distance / 1.0059466666666665 + 2；
    "device_id": "",
    "lot_number": lot_number,// lot_number取load接口返回的lot_number；
    "pow_msg": `1|0|md5|${new Date().toISOString().replace('Z', '+08:00')}|${captcha_id}|${lot_number}|||${generateGUID()}`,// pow_msg = `1|0|md5|${datetime}|${captcha_id}|${lot_number}|||${guid()}`，由多个参数拼接而来；
    "pow_sign": md5(`1|0|md5|${new Date().toISOString().replace('Z', '+08:00')}|${captcha_id}|${lot_number}|||${generateGUID()}`),// pow_sign为pow_msg的md5加密；
    "geetest": "captcha",
    "lang": "zh",
    "ep": "123",
    "biht": "1426265548",
    "gee_guard": {
        "roe": {
            "aup": "3",
            "sep": "3",
            "egp": "3",
            "auh": "3",
            "rew": "3",
            "snh": "3",
            "res": "3",
            "cdc": "3"
        }
    },
    "So89": "1AnD",
    "f24835bf": {
        "83f7": "7f24"
    },
    "em": {
        "ph": 0,
        "cp": 0,
        "ek": "11",
        "wd": 1,
        "nt": 0,
        "si": 0,
        "sc": 0
    }
}
    return arrayToHex(duicheng1(JSON.stringify(params), '5b15648d49827d93'))+'9a7f48cd58889f03739ef234ce0bba198064f480c510b1d56fd569e5fb1329a79cc2342981b8829f46e64cebc2380335b4550767a7005ee98e38efcf4147cffaee508e32e45dc57804f031923ca688fed26611f3a3c3956fb2c8abf29c07cd4b04cd70222d2fa342ce97a52bf87199c6b1128c997901dd476289208b442f9527'
}
_ᖉᕹᕺᖀ = {
    'options': {
        "language": "zho",
        "riskType": "slide",
        "product": "float",
        "captchaId": "54088bb07d2df3c46b79f80300b0abbe",
        "protocol": "https://",
        "lotNumber": "fa77addc8e0341c49cb4019a5a3da9b6",
        "captchaType": "slide",
        "slice": "captcha_v4/e70fbf1d77/slide/1e8ffe6222/2022-04-21T09/slice/a5e7b1cc72a84330a1337957298ca333.png",
        "bg": "captcha_v4/e70fbf1d77/slide/1e8ffe6222/2022-04-21T09/bg/a5e7b1cc72a84330a1337957298ca333.png",
        "ypos": 75,
        "arrow": "arrow_1",
        "js": "/js/gcaptcha4.js",
        "css": "/css/gcaptcha4.css",
        "staticPath": "/v4/static/v1.8.8-6a26af",
        "gctPath": "/v4/gct/gct4.5a2e755576738ba0499d714db4f1c9e0.js",
        "showVoice": true,
        "feedback": "https://www.geetest.com/Helper",
        "logo": true,
        "pt": "1",
        "captchaMode": "risk_manage",
        "guard": true,
        "checkDevice": true,
        "langReverse": false,
        "customTheme": {
            "_style": "stereoscopic",
            "_color": "hsla(224,98%,66%,1)",
            "_gradient": "linear-gradient(180deg, hsla(224, 98%,  71%, 1) 0%, hsla(224,98%,66%,1) 100%)",
            "_hover": "linear-gradient(180deg, hsla(224,98%,66%,1) 0%, hsla(224, 98%,  71%, 1) 100%)",
            "_brightness": "system",
            "_radius": "4px"
        },
        "powDetail": {
            "version": "1",
            "bits": 0,
            "datetime": "2025-04-14T19:52:34.904219+08:00",
            "hashfunc": "md5"
        },
        "payload": "AgFD8gWUUuHFx-XvpP7J2ZV8R7ivXKGo_inwO0QFigSF0dHiUzGTUrLhe00sIzdIRaEMgX9RukN1mWP2Rhx4Xjy6h8piJ48mNTMHSTja_ozeyuRS6tTEcZiI83kelpwQYoUyGLkzvLAsSunaLIEMZ7sOuuFmXnWSsv_9MVvKL6OUqgZT_WOIlHZwZ3rMyORGaOcYo_TubSUSlma5JBayroSuAWbSxiNV1xbguTdUrTV5K2RqQT9hTqBzEwZ2amj7jgaMXKiyRwSuBnEEYWwo3L1Aero1ZuFPRSJ0FGXhNL3uOX5el_RaIGnhaAlQR-RvYSS6HMDLz_csTCSHwp0_64SNNJLajeaGuSm_9Y-DRXtgYLH94YXlYXF4kPt6PnQ-30qcSelgynkOOEE0VYt-tClhBBCZ22FBGB1hhqDGG6niTgQvz1JXgtnVQzj1qUzNAD0I2gyTYZLf0Hf5EKH8PW9iUQ8pu9t-V6Bg-_4tV5JBqlVmwlBkuKOidJMRUj5XaL9L2jjpo7xh3GQOwBP52RUyCZWzSLyIz2UkIh7gaD_DWl4laI4Gf4E-C0bkr9aHxUhRUrXehXt2PiqA4Mn_SGfWrN1Clmdru4CklJqSZsWuHU9QxZCSt98hXpdTk5BvGMTwv3NMPj_hjZJy-znFZ_p1KjP7oJc_h-IUeEGYFLL1t8CLkUoab_73uR_7P5EcP5B4st5zesNb4p-y0wArbgeHkhu_P9AfmbTU7R-ulfNwFb_AeNAXJ7srPujZ1pAq4wC0U1ePcb_3FfFucn4wOpcsphCvo7zw8Yj529GCNfxQe1b88jX9RHtc8Gz9yLqvRmpE_TXuySVXWudTrCygeMg9_EOrBVNW74t1rOI5YIjukqa8T9IRdpDBE1CzeIb3hbOpJI1Dvlf_all5gfrJ1ldfDdM1dn1-MqGaPTeik7G8e3vPZZojtXpqMXC6U-OwwGvZHqpwkIrkz4IX3_xwlVajAKJxYsP5t6jHf-ChBFA=",
        "processToken": "b0517c69a3314be5f86571568e062ecc27706e8533cc597652e4762d32c64677",
        "payloadProtocol": 1,
        "hash": "d1b91bba",
        "outside": true,
        "hideBindSuccess": false,
        "hideSuccess": false,
        "clientType": "web",
        "animate": true,
        "ques": 75,
        "imgs": [
            "captcha_v4/e70fbf1d77/slide/1e8ffe6222/2022-04-21T09/bg/a5e7b1cc72a84330a1337957298ca333.png",
            "captcha_v4/e70fbf1d77/slide/1e8ffe6222/2022-04-21T09/slice/a5e7b1cc72a84330a1337957298ca333.png"
        ],
        "deviceId": "",
        "powMsg": "1|0|md5|2025-04-14T19:52:34.904219+08:00|54088bb07d2df3c46b79f80300b0abbe|fa77addc8e0341c49cb4019a5a3da9b6||c21d5a3d9e61881a",
        "powSign": "7ea514b7039862419328c59a62cec62d",
        "geeGuard": {
            "roe": {
                "aup": "3",
                "sep": "3",
                "egp": "3",
                "auh": "3",
                "rew": "3",
                "snh": "3",
                "res": "3",
                "cdc": "3"
            }
        },
        "lot": {
            "$_BA_": [
                {
                    "$_BA_": [
                        {
                            "$_BA_": [
                                10,
                                17
                            ]
                        }
                    ]
                },
                {
                    "$_BA_": [
                        {
                            "$_BA_": [
                                13
                            ]
                        },
                        {
                            "$_BA_": [
                                18
                            ]
                        },
                        {
                            "$_BA_": [
                                8
                            ]
                        },
                        {
                            "$_BA_": [
                                2
                            ]
                        }
                    ]
                }
            ]
        },
        "lotRes": {
            "$_BA_": [
                {
                    "$_BA_": [
                        {
                            "$_BA_": [
                                9,
                                12
                            ]
                        }
                    ]
                }
            ]
        }
    }
}
_ᕶᖉᖃᕾ = {
    "setLeft": 213,
    "passtime": 638,//固定
    "userresponse": 213.74084775866186,//userresponse为distance计算得来，等于distance / 1.0059466666666665 + 2；
    "device_id": "",
    "lot_number": "e87ec603f7f24835bf342cfa9e53f33c",// lot_number取load接口返回的lot_number；
    "pow_msg": "1|0|md5|2025-04-14T15:26:49.529860+08:00|54088bb07d2df3c46b79f80300b0abbe|e87ec603f7f24835bf342cfa9e53f33c||c9af6d0ec4d6b3d6",// pow_msg = `1|0|md5|${datetime}|${captcha_id}|${lot_number}||${guid()()}`，由多个参数拼接而来；
    "pow_sign": "bb2812515a104e9cccb1bcf7eed0924a",// pow_sign为pow_msg的md5加密；
    "geetest": "captcha",
    "lang": "zh",
    "ep": "123",
    "biht": "1426265548",
    "gee_guard": {
        "roe": {
            "aup": "3",
            "sep": "3",
            "egp": "3",
            "auh": "3",
            "rew": "3",
            "snh": "3",
            "res": "3",
            "cdc": "3"
        }
    },
    "So89": "1AnD",
    "f24835bf": {
        "83f7": "7f24"
    },
    "em": {
        "ph": 0,
        "cp": 0,
        "ek": "11",
        "wd": 1,
        "nt": 0,
        "si": 0,
        "sc": 0
    }
}

// console.log(JSON.stringify(_ᕶᖉᖃᕾ))
var _ᖚᖆᖀᖃ = arrayToHex(duicheng1(JSON.stringify(_ᕶᖉᖃᕾ), '5b15648d49827d93'))+'9a7f48cd58889f03739ef234ce0bba198064f480c510b1d56fd569e5fb1329a79cc2342981b8829f46e64cebc2380335b4550767a7005ee98e38efcf4147cffaee508e32e45dc57804f031923ca688fed26611f3a3c3956fb2c8abf29c07cd4b04cd70222d2fa342ce97a52bf87199c6b1128c997901dd476289208b442f9527'
console.log(getW(213,"e87ec603f7f24835bf342cfa9e53f33c","54088bb07d2df3c46b79f80300b0abbe"))
// console.log(arrayToHex(duicheng1('{"setLeft":213,"passtime":638,"userresponse":213.74084775866186,"device_id":"","lot_number":"e87ec603f7f24835bf342cfa9e53f33c","pow_msg":"1|0|md5|2025-04-14T15:26:49.529860+08:00|54088bb07d2df3c46b79f80300b0abbe|e87ec603f7f24835bf342cfa9e53f33c||c9af6d0ec4d6b3d6","pow_sign":"bb2812515a104e9cccb1bcf7eed0924a","geetest":"captcha","lang":"zh","ep":"123","biht":"1426265548","gee_guard":{"roe":{"aup":"3","sep":"3","egp":"3","auh":"3","rew":"3","snh":"3","res":"3","cdc":"3"}},"So89":"1AnD","f24835bf":{"83f7":"7f24"},"em":{"ph":0,"cp":0,"ek":"11","wd":1,"nt":0,"si":0,"sc":0}}','5b15648d49827d93')) + '9a7f48cd58889f03739ef234ce0bba198064f480c510b1d56fd569e5fb1329a79cc2342981b8829f46e64cebc2380335b4550767a7005ee98e38efcf4147cffaee508e32e45dc57804f031923ca688fed26611f3a3c3956fb2c8abf29c07cd4b04cd70222d2fa342ce97a52bf87199c6b1128c997901dd476289208b442f9527')



// 045c37e315d5a38eba9fa9db7fa0818e4c790f629cf177f7e8c031b7f62b4b572cb6b8f1af5ae04719ec60b0a79b9a03a936369131e74cfe78afde63db159269369319ebd781aa19eca7014808b910ff7a0f7b1d2b57afc4b5dc583d8839b2936d578d068faea1092fbfc62d36ceb700e77324db08ba92662782a1b4bcbaa77fbb214b43607116a39c62044fbc0e4e1831ce160364f60da0243786fc87e5c5499196704d5506cbf25e2eaba7db851d00e71d7017a4202f9851a4ed011c4f0ca23f266935cca525d6b81b908488114879f710e3e75c38b0076f37ebc9eb95d43f6431d9171e7daa5a5af18b7c4bbbf9609ff9c8ea9934ba26a485872383bd72c4e8479184011887adeb728ab313b3593fcff179d3cc7dbaa9e0f92f2c2d535a6ceab8b34844ce0486ed585b99d2f68a649c7f35c3ab88063a2bb91c90e25da98d7d7ad8215bba74b6f716a1b7adc8abfd29eef697937b050e275ee71da0ff7955219d275d407039effa69e988773e370760fcb20aa455f083604578d0a9e2e463a1c875674a20dc7c67f4519ac10af90f207e92f0af7e8e60095ba0ec5456db97a072e238da811f42fb5cef55ed4f5a9529ea1ad4d2c36601cccf86534ec2e0304b2aded6504ab1d03830a49923fda9dca9357c3c02d27dd359782a8033d4b22f80a9bdf2b4b91079662c43e7c2eccb742c8d2b2b8138bdec94686920590ab74eb3d410682e5d61cefee9a45c2e546e5a4e4e7d35519d0009041816987726206f3d0accfb17531843f990b2fd8928cad370dfe9c5dd98e4b5733603c5276c7f7e9a7f48cd58889f03739ef234ce0bba198064f480c510b1d56fd569e5fb1329a79cc2342981b8829f46e64cebc2380335b4550767a7005ee98e38efcf4147cffaee508e32e45dc57804f031923ca688fed26611f3a3c3956fb2c8abf29c07cd4b04cd70222d2fa342ce97a52bf87199c6b1128c997901dd476289208b442f9527

