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

var duicheng1 = function (param1, param2) {
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
b.prototype.fromString = function (_ᕶᖉᖃᕾ, _ᕶᕴᕹᕶ) {
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
b.prototype.clamp = function () {
    var _ᖀᖄᕴᖄ = this.s & this.DM;
    while (0 < this.t && this[this.t - 1] == _ᖀᖄᕴᖄ)
        --this.t;
}

// 添加subTo方法
b.prototype.subTo = function (a, r) {
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

function getW( lot_number, captcha_id) {
    pow_msg = `1|0|md5|${new Date().toISOString().replace('Z', '+08:00')}|${captcha_id}|${lot_number}|||${generateGUID()}`
    pow_sign = md5(pow_msg)
    var params = {
        "device_id": "",
        "lot_number": lot_number,// lot_number取load接口返回的lot_number；
        "pow_msg": pow_msg,// pow_msg = `1|0|md5|${datetime}|${captcha_id}|${lot_number}|||${guid()}`，由多个参数拼接而来；
        "pow_sign": pow_sign,// pow_sign为pow_msg的md5加密；
        "geetest": "captcha",
        "lang": "zh",
        "ep": "123",
        "biht": "1426265548",
        "So89": "1AnD",
        "c34368bc": {
            "31df": "9c34"
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
    return arrayToHex(duicheng1(JSON.stringify(params), "a91a21262bde001a")) + "2aa9084809ae753f240f3be144abe74982870ba331c34a308eb90b72dced80bc317b2c6034529d2da9b3bf00d18afeb07dad2125a73f43b297651f36dfd352b7094fa8aea4511108ab961e86b60af3f66f6de96e7d7ab63cdb5a822b8595941c6e2ed4d107dbe40951f3ac1002795e6f196b888ce6a66507b194ec828de68f9d"
}
