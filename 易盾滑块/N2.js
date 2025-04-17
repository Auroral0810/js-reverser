function F(N) {
    return N < -0x80 ? F(0x100 + N) : N > 0x7f ? F(N - 0x100) : N;
}

function A(N) {
    N = '' + N;
    for (var X = [], J = 0x0, Z = 0x0, B = N['length'] / 0x2; J < B; J++) {
        var E = parseInt(N['charAt'](Z++), 0x10) << 0x4
            , P = parseInt(N['charAt'](Z++), 0x10);
        X[J] = F(E + P);
    }
    return X;
}

function O(N) {
    //N = window["encodeURIComponent"](N);
    N = encodeURIComponent(N);
    for (var X = [], J = 0x0, Z = N["length"]; J < Z; J++)
        '%' === N["charAt"](J) ? J + 0x2 < Z && X["push"](A('' + N['charAt'](++J) + N["charAt"](++J))[0x0]) : X['push'](F(N["charCodeAt"](J)));
    return X;
}


function T_wm() {
    for (var N = arguments['length'] > 0x0 && void 0x0 !== arguments[0x0] ? arguments[0x0] : [], X = arguments['length'] > 0x1 && void 0x0 !== arguments[0x1] ? arguments[0x1] : [], J = [], Z = X['length'], B = 0x0, E = N['length']; B < E; B++)
        J[B] = K(N[B], X[B % Z]);
    return J;
}

function K(N, X) {
    return F(F(N) ^ F(X));
}


function T_wO(q) {
    var H = ['i', '/', 'x', '1', 'X', 'g', 'U', '0', 'z', '7', 'k', '8', 'N', '+', 'l', 'C', 'p', 'O', 'n', 'P', 'r', 'v', '6', '\x5c', 'q', 'u', '2', 'G', 'j', '9', 'H', 'R', 'c', 'w', 'T', 'Y', 'Z', '4', 'b', 'f', 'S', 'J', 'B', 'h', 'a', 'W', 's', 't', 'A', 'e', 'o', 'M', 'I', 'E', 'Q', '5', 'm', 'D', 'd', 'V', 'F', 'L', 'K', 'y']
        , M = '3';
    return k(q, H, M);
}

function k(q, H, M) {
    if (!q || 0x0 === q['length'])
        return '';
    try {
        for (var j = 0x0, N = []; j < q['length'];) {
            if (!(j + 0x3 <= q['length'])) {
                var X = q['slice'](j);
                N['push'](NewF(X, H, M));
                break;
            }
            var J = q['slice'](j, j + 0x3);
            N['push'](NewF(J, H, M)),
                j += 0x3;
        }
        return N['join']('');
    } catch (Z) {
        return '';
    }
}

function NewF(q, H, M) {
    var j = void 0x0
        , N = void 0x0
        , X = void 0x0
        , J = [];
    switch (q['length']) {
        case 0x1:
            j = q[0x0],
                N = X = 0x0,
                J['push'](H[j >>> 0x2 & 0x3f], H[(j << 0x4 & 0x30) + (N >>> 0x4 & 0xf)], M, M);
            break;
        case 0x2:
            j = q[0x0],
                N = q[0x1],
                X = 0x0,
                J['push'](H[j >>> 0x2 & 0x3f], H[(j << 0x4 & 0x30) + (N >>> 0x4 & 0xf)], H[(N << 0x2 & 0x3c) + (X >>> 0x6 & 0x3)], M);
            break;
        case 0x3:
            j = q[0x0],
                N = q[0x1],
                X = q[0x2],
                J['push'](H[j >>> 0x2 & 0x3f], H[(j << 0x4 & 0x30) + (N >>> 0x4 & 0xf)], H[(N << 0x2 & 0x3c) + (X >>> 0x6 & 0x3)], H[0x3f & X]);
            break;
        default:
            return '';
    }
    return J['join']('');
}

function N_as_w8(wq, wH) {
    var wp = O(wH);  // wK(wH)
    var wo = O(wq); // wK(wq)
    // return wO(wm(wp, wo));
    return T_wO(T_wm(wp, wo));
}

// var res = N_as_w8(process.argv[2], process.argv[3]);
// console.log(res);