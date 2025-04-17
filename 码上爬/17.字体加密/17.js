var _js = 'jsjiami.com.v7';
(function(c, d, e, f, g, h, i) {
    return c = c >> 0x3,
    h = 'hs',
    i = 'hs',
    function(j, k, l, m, n) {
        const q = b;
        m = 'tfi',
        h = m + h,
        n = 'up',
        i += n,
        h = l(h),
        i = l(i),
        l = 0x0;
        const o = j();
        while (!![] && --f + k) {
            try {
                m = -parseInt(q(0x176)) / 0x1 + parseInt(q(0x17a)) / 0x2 + parseInt(q(0x178)) / 0x3 + -parseInt(q(0x17b)) / 0x4 + parseInt(q(0x16e)) / 0x5 + parseInt(q(0x16b)) / 0x6 + -parseInt(q(0x163)) / 0x7;
            } catch (p) {
                m = l;
            } finally {
                n = o[h]();
                if (c <= f)
                    l ? g ? m = n : g = n : l = n;
                else {
                    if (l == g['replace'](/[IfnkMhEqdbJtAyeQUN=]/g, '')) {
                        if (m === k) {
                            o['un' + h](n);
                            break;
                        }
                        o[i](n);
                    }
                }
            }
        }
    }(e, d, function(j, k, l, m, n, o, p) {
        return k = '\x73\x70\x6c\x69\x74',
        j = arguments[0x0],
        j = j[k](''),
        l = '\x72\x65\x76\x65\x72\x73\x65',
        j = j[l]('\x76'),
        m = '\x6a\x6f\x69\x6e',
        (0x19846f,
        j[m](''));
    });
}(0x650, 0x3a5d4, a, 0xcc),
a) && (_js = 0x5ea);
const FONT_DECRYPT_MAP = {
    'ꙮ': '0',
    'ઊ': '1',
    'સ': '2',
    'ત': '3',
    'ধ': '4',
    'ન': '5',
    'પ': '6',
    'ફ': '7',
    'બ': '8',
    'ભ': '9'
};
function b(c, d) {
    const e = a();
    return b = function(f, g) {
        f = f - 0x161;
        let h = e[f];
        if (b['UAbxcV'] === undefined) {
            var i = function(m) {
                const n = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/=';
                let o = ''
                  , p = '';
                for (let q = 0x0, r, s, t = 0x0; s = m['charAt'](t++); ~s && (r = q % 0x4 ? r * 0x40 + s : s,
                q++ % 0x4) ? o += String['fromCharCode'](0xff & r >> (-0x2 * q & 0x6)) : 0x0) {
                    s = n['indexOf'](s);
                }
                for (let u = 0x0, v = o['length']; u < v; u++) {
                    p += '%' + ('00' + o['charCodeAt'](u)['toString'](0x10))['slice'](-0x2);
                }
                return decodeURIComponent(p);
            };
            b['BvDJwr'] = i,
            c = arguments,
            b['UAbxcV'] = !![];
        }
        const j = e[0x0]
          , k = f + j
          , l = c[k];
        return !l ? (h = b['BvDJwr'](h),
        c[k] = h) : h = l,
        h;
    }
    ,
    b(c, d);
}
function a() {
    const u = (function() {
        return [_js, 'efjsJqjIEiamkQiU.MAcqkoybtm.v7UNAkheMdne==', 'AM9PBG', 'CgrMvMLLD2vYrw5HyMXLza', 'C3bSAxq', 'u0rLDhu', 'A0nPsuy', 'y3vYCMvUDf9HCNjHEq', 'odiXnJzbr3b5twm', 'txbPyLC', 'mti2ndyYmhPxEKHOqG', 'Bhn0tgO', 'mty3nJC4BgnPzw9H'].concat((function() {
            return ['mtuXndyZnLnPuufzAG', 'Ag9PEhG', 'BgvUz3rO', 'CgfNAw5HDgLVBG', 'uefLtfG', 'BwfW', 'C3rYAw5N', 'v3HQzM4', 'q2LMz1u', 'DvP6vKG', 'yvHvsw8', 'mtmWnJK2m0jODKXADq', 'ChvZAa'].concat((function() {
                return ['ChjVDg9JB2W', 'AhjLzG', 'A1DNsvu', 'zw9csei', 'ENryuMG', 'AKnzExO', 'mtq3mJeZnLjzDKrtqW', 'CLLmsLu', 'AxnbCNjHEq', 'nJC5mJK1yMnquu1M', 'tvvoAM0'];
            }()));
        }()));
    }());
    a = function() {
        return u;
    }
    ;
    return a();
}
;function decryptFontNumber(c) {
    const r = b
      , d = {
        'ztXRh': function(f, g) {
            return f !== g;
        },
        'PAeLX': function(f, g) {
            return f || g;
        },
        'CifgU': function(f, g) {
            return f !== g;
        },
        'kWgIU': r(0x181)
    };
    if (d[r(0x183)](typeof c, d[r(0x167)]))
        return c;
    const e = c[r(0x172)]('')[r(0x180)](f => {
        const s = r
          , g = FONT_DECRYPT_MAP[f];
        if (!g && d[s(0x169)](f, '\x20')) {}
        return d[s(0x17f)](g, f);
    }
    )[r(0x170)]('');
    return e;
}
function updateCounter(c) {
    const t = b
      , d = {
        'jCYyz': function(j, k) {
            return j(k);
        },
        'lstLj': function(j, k) {
            return j(k);
        },
        'SDetu': function(j, k) {
            return j === k;
        },
        'aXUIo': t(0x16f),
        'Wxjfn': function(j, k) {
            return j !== k;
        },
        'eoBHB': t(0x161),
        'rYLJU': t(0x174),
        'MpibW': function(j, k) {
            return j < k;
        },
        'hoixx': function(j, k) {
            return j > k;
        }
    };
    let e;
    var f = []
      , g = {};
    e = c;
    for (var h = 0x0; d[t(0x177)](h, e[t(0x17d)]); h++) {
        font = d[t(0x179)](decryptFontNumber, e[h]),
        f[t(0x164)](font);
    }
    return f;
}

