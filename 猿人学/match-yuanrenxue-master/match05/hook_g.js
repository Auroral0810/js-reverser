(function hook_g() {
    var new_g = g;
    g = function (e) {
        var ret = new_g(e);
        // debugger
        console.log('_$Jy',_$Jy,'_$tT',_$tT,'_$6_',_$6_)
        console.log("加密前:", e, "加密后:", ret);
        return ret;
    }
})();

(function hook_0x474032() {
    var new_0x474032 = _0x474032;
    _0x474032 = function (e) {
        var ret = new_0x474032(e);
        // debugger
        console.log('_$Jy',_$Jy,'_$tT',_$tT,'_$6_',_$6_)
        console.log("加密前:", e, "加密后:", ret);
        return ret;
    }
})();

// console.log('_$Jy',_$Jy,'_$tT',_$tT,'_$6_',_$6_)
// hook window attr simple
Object.defineProperty(window, "_$Jy", {
    set: function (e) {
        console.log('set _$Jy_', e)
        return e;
    }
})

Object.defineProperty(window, "_$ss", {
    set: function (e) {
        console.log('set _$ss', e)
        debugger
        return e;
    }
})


// hook window attr
var window_flag_1 = '_$6_';
var window_flag_2 = 'ccc';

var key_value_map = {};
var window_value = window[window_flag_1];

Object.defineProperty(window, window_flag_1, {
    get: function () {
        console.log('Getting', window, window_flag_1, '=', window_value);
        //debugger;
        return window_value;
    },
    set: function (val) {
        console.log('Setting', window, window_flag_1, '=', val);
        //debugger;
        window_value = val;
        key_value_map[window[window_flag_1]] = window_flag_1;
        set_obj_attr(window[window_flag_1], window_flag_2);
    },
});

function set_obj_attr(obj, attr) {
    var obj_attr_value = obj[attr];
    Object.defineProperty(obj, attr, {
        get: function () {
            console.log('Getting', key_value_map[obj], attr, '=', obj_attr_value);
            //             debugger;
            return obj_attr_value;
        },
        set: function (val) {
            console.log('Setting', key_value_map[obj], attr, '=', val);
            //             debugger;
            obj_attr_value = val;
        },
    });
}

// _$Jy 461512024 _$tT -172015004 _$6_ 8821003647
// VM116825:7 加密前: 1607870499000 加密后: 5ebb09ca3d0199732a48ec64851405f9
// VM116825:6 _$Jy 461512024 _$tT -172015004 _$6_ 8821003647
// VM116825:7 加密前: 1607870499000 加密后: 5ebb09ca3d0199732a48ec64851405f9
// VM116825:6 _$Jy 1607870499151 _$tT -660478335 _$6_ 8821003647
// VM116825:7 加密前: 1607870499000 加密后: fee6da49dddffb869140a61488975937
// VM116825:6 _$Jy 1607870499151 _$tT -660478335 _$6_ 8821003647
// VM116825:7 加密前: 1607870499000 加密后: fee6da49dddffb869140a61488975937
// VM116825:6 _$Jy 1607870499201 _$tT -660478335 _$6_ 8821003647
// VM116825:7 加密前: 1607870499000 加密后: 17c5ef7b9ecd426562438845546818b1
// VM116825:6 _$Jy 1607870499201 _$tT -660478335 _$6_ 8821003647
// VM116825:7 加密前: 1607870499000 加密后: 17c5ef7b9ecd426562438845546818b1
// VM116825:6 _$Jy 1607870499202 _$tT -660478335 _$6_ 8821003647
// VM116825:7 加密前: 1607870499000 加密后: 8b3ac8dc2931d6471389cd6db88eaba5
// VM116825:6 _$Jy 1607870499202 _$tT -660478335 _$6_ 8821003647
// VM116825:7 加密前: 1607870499000 加密后: 8b3ac8dc2931d6471389cd6db88eaba5
// VM116188:formatted:1071 世上无难事，只要肯放弃
// VM116188:formatted:1071 世上无难事，只要肯放弃
// VM116825:6 _$Jy -405537848 _$tT -660478335 _$6_ -389564586
// VM116825:7 加密前: 1607870499329 加密后: 2748c6e844f3b62fd9d154316ba2ecf5
// VM116825:6 _$Jy -405537848 _$tT -660478335 _$6_ -389564586
// VM116825:7 加密前: 1607870499329 加密后: 2748c6e844f3b62fd9d154316ba2ecf5