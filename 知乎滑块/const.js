const jsdom = require("jsdom");
const { JSDOM } = jsdom;
const dom = new JSDOM(`<!DOCTYPE html><p>Hello world</p>`);
window = dom.window;
document = window.document;
// function(module, exports, __webpack_require__) {
//    "use strict";
function t(e) {
    return (t = "function" == typeof Symbol && "symbol" == typeof Symbol.A ? function (e) {
                return typeof e
            }
            : function (e) {
                return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e
            }
    )(e)
}

Object.defineProperty(exports, "__esModule", {
    value: !0
});
var A = "2.0"
    , __g = {};

function s() {
}

function i(e) {
    this.t = (2048 & e) >> 11,
        this.s = (1536 & e) >> 9,
        this.i = 511 & e,
        this.h = 511 & e
}

function h(e) {
    this.s = (3072 & e) >> 10,
        this.h = 1023 & e
}

function a(e) {
    this.a = (3072 & e) >> 10,
        this.c = (768 & e) >> 8,
        this.n = (192 & e) >> 6,
        this.t = 63 & e
}

function c(e) {
    this.s = e >> 10 & 3,
        this.i = 1023 & e
}

function n() {
}

function e(e) {
    this.a = (3072 & e) >> 10,
        this.c = (768 & e) >> 8,
        this.n = (192 & e) >> 6,
        this.t = 63 & e
}

function o(e) {
    this.h = (4095 & e) >> 2,
        this.t = 3 & e
}

function r(e) {
    this.s = e >> 10 & 3,
        this.i = e >> 2 & 255,
        this.t = 3 & e
}

s.prototype.e = function (e) {
    e.o = !1
}
    ,
    i.prototype.e = function (e) {
        switch (this.t) {
            case 0:
                e.r[this.s] = this.i;
                break;
            case 1:
                e.r[this.s] = e.k[this.h]
        }
    }
    ,
    h.prototype.e = function (e) {
        e.k[this.h] = e.r[this.s]
    }
    ,
    a.prototype.e = function (e) {
        switch (this.t) {
            case 0:
                e.r[this.a] = e.r[this.c] + e.r[this.n];
                break;
            case 1:
                e.r[this.a] = e.r[this.c] - e.r[this.n];
                break;
            case 2:
                e.r[this.a] = e.r[this.c] * e.r[this.n];
                break;
            case 3:
                e.r[this.a] = e.r[this.c] / e.r[this.n];
                break;
            case 4:
                e.r[this.a] = e.r[this.c] % e.r[this.n];
                break;
            case 5:
                e.r[this.a] = e.r[this.c] == e.r[this.n];
                break;
            case 6:
                e.r[this.a] = e.r[this.c] >= e.r[this.n];
                break;
            case 7:
                e.r[this.a] = e.r[this.c] || e.r[this.n];
                break;
            case 8:
                e.r[this.a] = e.r[this.c] && e.r[this.n];
                break;
            case 9:
                e.r[this.a] = e.r[this.c] !== e.r[this.n];
                break;
            case 10:
                e.r[this.a] = t(e.r[this.c]);
                break;
            case 11:
                e.r[this.a] = e.r[this.c] in e.r[this.n];
                break;
            case 12:
                e.r[this.a] = e.r[this.c] > e.r[this.n];
                break;
            case 13:
                e.r[this.a] = -e.r[this.c];
                break;
            case 14:
                e.r[this.a] = e.r[this.c] < e.r[this.n];
                break;
            case 15:
                e.r[this.a] = e.r[this.c] & e.r[this.n];
                break;
            case 16:
                e.r[this.a] = e.r[this.c] ^ e.r[this.n];
                break;
            case 17:
                e.r[this.a] = e.r[this.c] << e.r[this.n];
                break;
            case 18:
                e.r[this.a] = e.r[this.c] >>> e.r[this.n];
                break;
            case 19:
                e.r[this.a] = e.r[this.c] | e.r[this.n];
                break;
            case 20:
                e.r[this.a] = !e.r[this.c]
        }
    }
    ,
    c.prototype.e = function (e) {
        e.Q.push(e.C),
            e.B.push(e.k),
            e.C = e.r[this.s],
            e.k = [];
        for (var t = 0; t < this.i; t++)
            e.k.unshift(e.f.pop());
        e.g.push(e.f),
            e.f = []
    }
    ,
    n.prototype.e = function (e) {
        e.C = e.Q.pop(),
            e.k = e.B.pop(),
            e.f = e.g.pop()
    }
    ,
    e.prototype.e = function (e) {
        switch (this.t) {
            case 0:
                e.u = e.r[this.a] >= e.r[this.c];
                break;
            case 1:
                e.u = e.r[this.a] <= e.r[this.c];
                break;
            case 2:
                e.u = e.r[this.a] > e.r[this.c];
                break;
            case 3:
                e.u = e.r[this.a] < e.r[this.c];
                break;
            case 4:
                e.u = e.r[this.a] == e.r[this.c];
                break;
            case 5:
                e.u = e.r[this.a] != e.r[this.c];
                break;
            case 6:
                e.u = e.r[this.a];
                break;
            case 7:
                e.u = !e.r[this.a]
        }
    }
    ,
    o.prototype.e = function (e) {
        switch (this.t) {
            case 0:
                e.C = this.h;
                break;
            case 1:
                e.u && (e.C = this.h);
                break;
            case 2:
                e.u || (e.C = this.h);
                break;
            case 3:
                e.C = this.h,
                    e.w = null
        }
        e.u = !1
    }
    ,
    r.prototype.e = function (e) {
        switch (this.t) {
            case 0:
                for (var t = [], n = 0; n < this.i; n++)
                    t.unshift(e.f.pop());
                e.r[3] = e.r[this.s](t[0], t[1]);
                break;
            case 1:
                for (var r = e.f.pop(), o = [], i = 0; i < this.i; i++)
                    o.unshift(e.f.pop());
                e.r[3] = e.r[this.s][r](o[0], o[1]);
                break;
            case 2:
                for (var a = [], c = 0; c < this.i; c++)
                    a.unshift(e.f.pop());
                e.r[3] = new e.r[this.s](a[0], a[1])
        }
    }
;
var k = function (e) {
    for (var t = 66, n = [], r = 0; r < e.length; r++) {
        var o = 24 ^ e.charCodeAt(r) ^ t;
        n.push(String.fromCharCode(o)),
            t = o
    }
    return n.join("")
};

function Q(e) {
    this.t = (4095 & e) >> 10,
        this.s = (1023 & e) >> 8,
        this.i = 1023 & e,
        this.h = 63 & e
}

function C(e) {
    this.t = (4095 & e) >> 10,
        this.a = (1023 & e) >> 8,
        this.c = (255 & e) >> 6
}

function B(e) {
    this.s = (3072 & e) >> 10,
        this.h = 1023 & e
}

function f(e) {
    this.h = 4095 & e
}

function g(e) {
    this.s = (3072 & e) >> 10
}

function u(e) {
    this.h = 4095 & e
}

function w(e) {
    this.t = (3840 & e) >> 8,
        this.s = (192 & e) >> 6,
        this.i = 63 & e
}

function G() {
    this.r = [0, 0, 0, 0],
        this.C = 0,
        this.Q = [],
        this.k = [],
        this.B = [],
        this.f = [],
        this.g = [],
        this.u = !1,
        this.G = [],
        this.b = [],
        this.o = !1,
        this.w = null,
        this.U = null,
        this.F = [],
        this.R = 0,
        this.J = {
            0: s,
            1: i,
            2: h,
            3: a,
            4: c,
            5: n,
            6: e,
            7: o,
            8: r,
            9: Q,
            10: C,
            11: B,
            12: f,
            13: g,
            14: u,
            15: w
        }
}

Q.prototype.e = function (e) {
    switch (this.t) {
        case 0:
            e.f.push(e.r[this.s]);
            break;
        case 1:
            e.f.push(this.i);
            break;
        case 2:
            e.f.push(e.k[this.h]);
            break;
        case 3:
            e.f.push(k(e.b[this.h]))
    }
}
    ,
    C.prototype.e = function (A) {
        switch (this.t) {
            case 0:
                var t = A.f.pop();
                A.r[this.a] = A.r[this.c][t];
                break;
            case 1:
                var s = A.f.pop()
                    , i = A.f.pop();
                A.r[this.c][s] = i;
                break;
            case 2:
                var h = A.f.pop();
                A.r[this.a] = eval(h)
        }
    }
    ,
    B.prototype.e = function (e) {
        e.r[this.s] = k(e.b[this.h])
    }
    ,
    f.prototype.e = function (e) {
        e.w = this.h
    }
    ,
    g.prototype.e = function (e) {
        throw e.r[this.s]
    }
    ,
    u.prototype.e = function (e) {
        var t = this
            , n = [0];
        e.k.forEach((function (e) {
                n.push(e)
            }
        ));
        var r = function (r) {
            var o = new G;
            return o.k = n,
                o.k[0] = r,
                o.v(e.G, t.h, e.b, e.F),
                o.r[3]
        };
        r.toString = function () {
            return "() { [native code] }"
        }
            ,
            e.r[3] = r
    }
    ,
    w.prototype.e = function (e) {
        switch (this.t) {
            case 0:
                for (var t = {}, n = 0; n < this.i; n++) {
                    var r = e.f.pop();
                    t[e.f.pop()] = r
                }
                e.r[this.s] = t;
                break;
            case 1:
                for (var o = [], i = 0; i < this.i; i++)
                    o.unshift(e.f.pop());
                e.r[this.s] = o
        }
    }
    ,
    G.prototype.D = function (e) {
        for (var t = window.atob(e), n = t.charCodeAt(0) << 8 | t.charCodeAt(1), r = [], o = 2; o < n + 2; o += 2)
            r.push(t.charCodeAt(o) << 8 | t.charCodeAt(o + 1));
        this.G = r;
        for (var i = [], a = n + 2; a < t.length;) {
            var c = t.charCodeAt(a) << 8 | t.charCodeAt(a + 1)
                , s = t.slice(a + 2, a + 2 + c);
            i.push(s),
                a += c + 2
        }
        this.b = i
    }
    ,
    G.prototype.v = function (e, t, n) {
        for (t = t || 0,
                 n = n || [],
                 this.C = t,
                 "string" == typeof e ? this.D(e) : (this.G = e,
                     this.b = n),
                 this.o = !0,
                 this.R = Date.now(); this.o;) {
            var r = this.G[this.C++];
            if ("number" != typeof r)
                break;
            var o = Date.now();
            if (500 < o - this.R)
                return;
            this.R = o;
            try {
                this.e(r)
            } catch (e) {
                this.U = e,
                this.w && (this.C = this.w)
            }
        }
    }
    ,
    G.prototype.e = function (e) {
        var t = (61440 & e) >> 12;
        new this.J[t](e).e(this)
    }
    ,
"undefined" != typeof window && (new G).v("AxjgB5MAnACoAJwBpAAAABAAIAKcAqgAMAq0AzRJZAZwUpwCqACQACACGAKcBKAAIAOcBagAIAQYAjAUGgKcBqFAuAc5hTSHZAZwqrAIGgA0QJEAJAAYAzAUGgOcCaFANRQ0R2QGcOKwChoANECRACQAsAuQABgDnAmgAJwMgAGcDYwFEAAzBmAGcSqwDhoANECRACQAGAKcD6AAGgKcEKFANEcYApwRoAAxB2AGcXKwEhoANECRACQAGAKcE6AAGgKcFKFANEdkBnGqsBUaADRAkQAkABgCnBagAGAGcdKwFxoANECRACQAGAKcGKAAYAZx+rAZGgA0QJEAJAAYA5waoABgBnIisBsaADRAkQAkABgCnBygABoCnB2hQDRHZAZyWrAeGgA0QJEAJAAYBJwfoAAwFGAGcoawIBoANECRACQAGAOQALAJkAAYBJwfgAlsBnK+sCEaADRAkQAkABgDkACwGpAAGAScH4AJbAZy9rAiGgA0QJEAJACwI5AAGAScH6AAkACcJKgAnCWgAJwmoACcJ4AFnA2MBRAAMw5gBnNasCgaADRAkQAkABgBEio0R5EAJAGwKSAFGACcKqAAEgM0RCQGGAYSATRFZAZzshgAtCs0QCQAGAYSAjRFZAZz1hgAtCw0QCQAEAAgB7AtIAgYAJwqoAASATRBJAkYCRIANEZkBnYqEAgaBxQBOYAoBxQEOYQ0giQKGAmQABgAnC6ABRgBGgo0UhD/MQ8zECALEAgaBxQBOYAoBxQEOYQ0gpEAJAoYARoKNFIQ/zEPkAAgChgLGgkUATmBkgAaAJwuhAUaCjdQFAg5kTSTJAsQCBoHFAE5gCgHFAQ5hDSCkQAkChgBGgo0UhD/MQ+QACAKGAsaCRQCOYGSABoAnC6EBRoKN1AUEDmRNJMkCxgFGgsUPzmPkgAaCJwvhAU0wCQFGAUaCxQGOZISPzZPkQAaCJwvhAU0wCQFGAUaCxQMOZISPzZPkQAaCJwvhAU0wCQFGAUaCxQSOZISPzZPkQAaCJwvhAU0wCQFGAkSAzRBJAlz/B4FUAAAAwUYIAAIBSITFQkTERwABi0GHxITAAAJLwMSGRsXHxMZAAk0Fw8HFh4NAwUABhU1EBceDwAENBcUEAAGNBkTGRcBAAFKAAkvHg4PKz4aEwIAAUsACDIVHB0QEQ4YAAsuAzs7AAoPKToKDgAHMx8SGQUvMQABSAALORoVGCQgERcCAxoACAU3ABEXAgMaAAsFGDcAERcCAxoUCgABSQAGOA8LGBsPAAYYLwsYGw8AAU4ABD8QHAUAAU8ABSkbCQ4BAAFMAAktCh8eDgMHCw8AAU0ADT4TGjQsGQMaFA0FHhkAFz4TGjQsGQMaFA0FHhk1NBkCHgUbGBEPAAFCABg9GgkjIAEmOgUHDQ8eFSU5DggJAwEcAwUAAUMAAUAAAUEADQEtFw0FBwtdWxQTGSAACBwrAxUPBR4ZAAkqGgUDAwMVEQ0ACC4DJD8eAx8RAAQ5GhUYAAFGAAAABjYRExELBAACWhgAAVoAQAg/PTw0NxcQPCQ5C3JZEBs9fkcnDRcUAXZia0Q4EhQgXHojMBY3MWVCNT0uDhMXcGQ7AUFPHigkQUwQFkhaAkEACjkTEQspNBMZPC0ABjkTEQsrLQ==");
var b = function (e) {
    console.log((encodeURIComponent(e)))
    return __g._encrypt(encodeURIComponent(e))
}
// exports.ENCRYPT_VERSION = A,
// exports.default = b
// e = "client_id=c3cef7c66a1843f8b3a9e6a1e3160e20&grant_type=password&timestamp=1611807648668&source=com.zhihu.web&signature=bf8a76bdc8f39b0f1083eb2529af5208ccfd4d5f&username=%2B8613213296461&password=fdjbcikjnverv&captcha=&lang=cn&utm_source=&ref_source=other_https%3A%2F%2Fwww.zhihu.com%2Fsignin%3Fnext%3D%252F"
//
// console.log(b(e))
