
const _0x38addf = _0x66a7;
const CryptoJS = require('crypto-js');
(function (_0x59b24b, _0x16d38a) {
    const _0x3e5f1c = _0x66a7, _0x14ae46 = _0x59b24b();
    while (!![]) {
        try {
            const _0x5e1110 = parseInt(_0x3e5f1c(0xca)) / 0x1 + -parseInt(_0x3e5f1c(0xd4)) / 0x2 * (-parseInt(_0x3e5f1c(0xd5)) / 0x3) + parseInt(_0x3e5f1c(0xc8)) / 0x4 + -parseInt(_0x3e5f1c(0xcc)) / 0x5 * (-parseInt(_0x3e5f1c(0xd0)) / 0x6) + -parseInt(_0x3e5f1c(0xd3)) / 0x7 + -parseInt(_0x3e5f1c(0xcd)) / 0x8 + -parseInt(_0x3e5f1c(0xcf)) / 0x9;
            if (_0x5e1110 === _0x16d38a) break; else _0x14ae46['push'](_0x14ae46['shift']());
        } catch (_0x4fbd75) {
            _0x14ae46['push'](_0x14ae46['shift']());
        }
    }
}(_0x4f0d, 0x897b4), dd = {'a': CryptoJS});
let key = dd['a'][_0x38addf(0xd6)][_0x38addf(0xc7)][_0x38addf(0xc9)](_0x38addf(0xce)),
    iv = dd['a'][_0x38addf(0xd6)]['Utf8'][_0x38addf(0xc9)]('0123456789ABCDEF');

function _0x4f0d() {
    const _0x341c37 = ['2440720SaQcQw', 'jo8j9wGw%6HbxfFn', '9735516pjwmiO', '68862pbatqQ', 'mode', 'AES', '1923264HnviQd', '36906bPsIrd', '12hEJHOd', 'enc', 'pad', 'encrypt', 'Hex', 'Utf8', '689460JbShaf', 'parse', '957060HmuxSn', 'toString', '445UZKyxv'];
    _0x4f0d = function () {
        return _0x341c37;
    };
    return _0x4f0d();
}
function _0x66a7(_0x7461a9, _0x14ffcc) {
    const _0x4f0d09 = _0x4f0d();
    return _0x66a7 = function (_0x66a780, _0x2abc15) {
        _0x66a780 = _0x66a780 - 0xc5;
        let _0x477d8f = _0x4f0d09[_0x66a780];
        return _0x477d8f;
    }, _0x66a7(_0x7461a9, _0x14ffcc);
}

function encrypt(_0x277028) {
    const _0x4d843e = _0x38addf;
    let _0x2703a2 = dd['a'][_0x4d843e(0xd6)]['Utf8']['parse'](_0x277028),
        _0x50fcf0 = dd['a'][_0x4d843e(0xd2)][_0x4d843e(0xc5)](_0x2703a2, key, {
            'mode': dd['a'][_0x4d843e(0xd1)]['CBC'],
            'padding': dd['a'][_0x4d843e(0xd7)]['Pkcs7'],
            'iv': iv
        });
    return _0x50fcf0['ciphertext'][_0x4d843e(0xcb)](CryptoJS[_0x4d843e(0xd6)][_0x4d843e(0xc6)]);
}
function getxl(i) {
    const timestamp = new Date().getTime();
    const params = {
        page: i,
        _ts: timestamp,
    };
    const jsonString = JSON.stringify(params);
    let encrypted = encrypt(jsonString);
    return encrypted;
}