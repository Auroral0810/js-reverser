var f = 'U9876543210zyxwvutsrqpomnlkjihgfdecbaZXYWVUTSRQPONABHICESQWK2Fi+9876543210zyxwvutsrqpomnlkjihgfdecbaZXYWVUTSRQPONABHICESQWK2Fi'
const md5 = require('./md5.js');
function btoa(e) { //e是时间戳，即p_s，1744032143000
    var window = global
    if (/([^\u0000-\u00ff])/.test(e))
        throw new Error("INVALID_CHARACTER_ERR");
    for (var o, a, s, p = 0, c = []; p < e.length; ) {
        switch (a = e.charCodeAt(p),
        s = p % 6) {
        case 0:
            delete window,
            delete document,
            c.push(f.charAt(a >> 2));
            break;
        case 1:
            try {
                window && c.push(f.charAt(((2 & o) << 3) | a >> 4))
            } catch (e) {
                c.push(f.charAt((((3 & o) << 4) | a >> 4)))
            }
            break;
        case 2:
            c.push(f.charAt((((15 & o) << 2) | a >> 6))),
            c.push(f.charAt((a & 63)));
            break;
        case 3:
            c.push(f.charAt(a >> 3));
            break;
        case 4:
            c.push(f.charAt((((o &4) << 6) | a >> 6)));
            break;
        case 5:
            c.push(f.charAt((((o & 15) << 4) | a >> 8))),
            c.push(f.charAt((a & 63)))
        }
        o = a,
        p++
    }
    return 0 == s ? (c.push(f.charAt((o & 3) << 4)),
    c.push("FM")) : s == 1 && (c.push(f.charAt((15 & o) << 2)),
    c.push("K")),
    "123456789012345"+md5(c.join(""))+"1111111111"
}


