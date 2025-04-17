const crypto = require('crypto');

const aesKey = "ydsecret://query/key/B*RGygVywfNBwpmBaZg*WT7SIOUP2T0C9WHMZN39j^DAdaZhAnxvGcCY6VYFwnHl";
const aesIv = "ydsecret://query/iv/C@lZe2YzHtZ2CYgaXKSVfsb7Y4QWHjITPPZ0nQp87fBeJ!Iv6v^6fvi2WN@bYpJ4";
function md5(text) {
    return crypto.createHash('md5').update(text).digest('hex');
}

function alloc(size, fill) {
    return Buffer.alloc(size, fill, 'hex');
}

function T(e) {
    return md5(e);
}

const O = (e, t, a) => {
    if (!e)
        return null;
    const o = alloc(16, T(t))
        , n = alloc(16, T(a))
        , r = crypto.createDecipheriv("aes-128-cbc", o, n);
    let s = r.update(e, "base64", "utf-8");
    return s += r.final("utf-8"),
        s;
};

// 有道翻译加密数据解密示例
// 这个示例数据可能不是最新的或者与当前的加密方式不匹配
// 根据demo.js和demo.py的内容，我们需要使用正确的加密方式
const d = "fanyideskweb";
const u = "webfanyi";
const t = 'asdjnjfenknafdfsdfsd';
const a = (new Date).getTime();
const sign = md5(`client=${d}&mysticTime=${a}&product=${u}&key=${t}`);

console.log("生成的sign:", sign);
console.log("时间戳:", a);

// 尝试解密一个新的示例数据
const e = 'Z21kD9ZK1ke6ugku2ccWu4n6eLnvoDT0YgGi0y3g-v0B9sYqg8L9D6UERNozYOHqObNkfQUzjCpVRbU1EBIynoFaCUQVN5p492mJkycxkvZ9LQ9sAblaNt2k1RQo1gileaiYUy4mofJNYcWLBuat_PYRF67lTxl43tVzF9dR1f0sVjhyBm8IONoaHG2vSZKml8RIGp0iKOyjHi-m4aeOTxKck_-KugSYXE4FtjSSFuyE-ky0WyTiastG9cKIqi0lJ6Fk4cJmuKjY456GVHKzxlZ__T8lPrhn9X002kTDVLiIpTZTHwwfMs3r_Sxnmxc8RLHI5sOKbXMYZiVr-L_h44cqw4GSr3sLyxtWKHr6f_uwtW4ubX9-V_kFich3u2q2AN3ABx1Bn2sBf5U55c-dBqnUYkjnwwzvAkFNgRp9IpVuPG9rdbt5khl5VsYX-SqO4EZzRTNaYe4R233spcOwPJA532RVPrdrZjmVZ3lZNTDxt6ArXNGQYYC6JDLNLbASbhT6nSBjJVs8QvryNAKSz8KsytlmeX9AftWJ7KHvKwwYavumEbKQ3GOBKawamdlluugZrewCPG_qFhxsDPfXnRFgBLhHOdZT3nOGZre0z23risk2UU0YRAjMrC5n2QVKX9RkFSFI9m2wzlh7k047fLZLLF2l1Wa2pAiHxPbGdXUP0ENcClorvkpZhxr-Ur4a23mbkEWvZldXiEjdklIH1SibV7Des2hgh8NeUKIQ8XHDH3al9JPGmX-sDeozpeNAFa9sHOd9sYCWj_szYZoiqA=='
console.log(O(e, aesKey, aesIv));