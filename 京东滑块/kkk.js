var JDJRValidate = function(a, b) {
    this['params'] = a;
    this['callback'] = b;
    this['init']();
};
JDJRValidate['prototype'] = {
    'init': function() {
        this['lang'] = this['params'] == undefined ? null : this['params']['lang'];
        this['slideTimer'] = null;
        this['mousePos'] = [];
        this['clickProductData'] = [];
        this['disX'] = 0x0;
        this['passValidate'] = ![];
        this['validateID'] = null;
        this['isDraging'] = ![];
        this['warp'] = this['getByID'](this['params']['id']);
        this['clickResult'] = ![];
        this['i18nParams'] = this['i18n'](this['lang']);
        this['protocol'] = this['params']['protocol'] ? this['params']['protocol'] + ':' : '';
        this['apiServer'] = this['protocol'] + (this['lang'] && this['lang'] != 'zh_CN' ? '//iv.joybuy.com' : '//iv.jd.com');
        this['bottomSlide'] = this['params']['bottomSlide'] !== ![];
        this['initHtml']();
        this['getInstance']();
    },
    'i18n': function(a) {
        var b = {};
        b['zh_CN'] = {
            'default-placeholder': '向右滑动完成拼图',
            'default-title': '完成拼图验证',
            'default-refresh': '换一张',
            'default-click': '点击完成验证',
            'default-slide-success': '拼接成功',
            'default-suspend-success': '验证成功',
            'default-action-block': '操作过于频繁',
            'default-slide-fail': '没有对齐，请再来一次'
        };
        b['en_US'] = {
            'default-placeholder': 'Swipe\x20to\x20complete\x20puzzle',
            'default-title': 'Complete\x20the\x20image',
            'default-refresh': 'Refresh',
            'default-click': 'Confirm\x20registration',
            'default-slide-success': 'Verification\x20complete',
            'default-suspend-success': 'Verification\x20complete',
            'default-action-block': 'You\x20have\x20performed\x20this\x20action\x20too\x20many\x20times.',
            'default-slide-fail': 'Incorrect.\x20Please\x20try\x20again.'
        };
        b['ru_RU'] = {
            'default-placeholder': 'Проведите\x20вправо',
            'default-title': 'Завершите\x20пазл',
            'default-refresh': 'Обновить',
            'default-click': 'Подтверждение\x20регистрации',
            'default-slide-success': 'Проверка\x20успешно',
            'default-suspend-success': 'Проверка\x20успешно',
            'default-action-block': 'Превышено\x20допустимое\x20количество\x20попыток.',
            'default-slide-fail': 'Ошибка.\x20Попробуйте\x20еще\x20раз.'
        };
        b['es_ES'] = {
            'default-placeholder': 'completar\x20la\x20pieza',
            'default-title': 'Completar\x20la\x20imagen',
            'default-refresh': 'Actualizar',
            'default-click': 'Haga\x20clic\x20para\x20la\x20verificación',
            'default-slide-success': 'Verificado\x20con\x20éxito',
            'default-suspend-success': 'Verificado\x20con\x20éxito',
            'default-action-block': 'Has\x20realizado\x20esta\x20acción\x20muchas\x20veces.',
            'default-slide-fail': 'Incorrecto.\x20Inténtalo\x20de\x20nuevo.'
        };
        b['th_TH'] = {
            'default-placeholder': 'เลื่อนชิ้นส่วนจิ๊กซอว์ให้เข้าที่',
            'default-title': 'เล่มเกมเพื่อลงทะเบียน',
            'default-refresh': 'เปลี่ยนรูป',
            'default-click': 'ถัดไป',
            'default-slide-success': 'ยินดีด้วย!',
            'default-suspend-success': 'ยินดีด้วย!',
            'default-action-block': 'You\x20have\x20performed\x20this\x20action\x20too\x20many\x20times.',
            'default-slide-fail': 'Incorrect.\x20Please\x20try\x20again.'
        };
        b['en_TH'] = {
            'default-placeholder': 'Swipe\x20to\x20complete\x20puzzle',
            'default-title': 'Complete\x20the\x20puzzle',
            'default-refresh': 'Change',
            'default-click': 'Next',
            'default-slide-success': 'Congratulations!',
            'default-suspend-success': 'Congratulations!',
            'default-action-block': 'You\x20have\x20performed\x20this\x20action\x20too\x20many\x20times.',
            'default-slide-fail': 'Incorrect.\x20Please\x20try\x20again.'
        };
        b['id_ID'] = {
            'default-placeholder': 'Geser\x20untuk\x20teka-teki',
            'default-title': 'Lengkapi\x20gambarnya',
            'default-refresh': 'Refresh',
            'default-click': 'Klik\x20verifikasi',
            'default-slide-success': 'Verifikasi\x20selesai',
            'default-suspend-success': 'Verifikasi\x20selesai',
            'default-action-block': 'You\x20have\x20performed\x20this\x20action\x20too\x20many\x20times.',
            'default-slide-fail': 'Incorrect.\x20Please\x20try\x20again.'
        };
        b['zh_TW'] = {
            'default-placeholder': '向右滑動完成拼圖',
            'default-title': '完成拼圖驗證',
            'default-refresh': '換一張',
            'default-click': '點擊完成驗證',
            'default-slide-success': '拼接成功',
            'default-suspend-success': '驗證成功',
            'default-action-block': '操作過於頻繁',
            'default-slide-fail': '沒有對齊，請再來一次'
        };
        if (b['hasOwnProperty'](a)) {
            return b[a];
        } else {
            return b['zh_CN'];
        }
    },
    'getByID': function(a) {
        return document['getElementById'](a);
    },
    'initGetElementsByName': function(a) {
        a['getElementsByClassName'] = function(b) {
            var c = (a || document)['getElementsByTagName']('*');
            var e = new Array();
            for (var f = 0x0; f < c['length']; f++) {
                var g = c[f];
                var h = g['className']['split']('\x20');
                for (var k = 0x0; k < h['length']; k++) {
                    if (h[k] == b) {
                        e['push'](g);
                        break;
                    }
                }
            }
            return e;
        }
        ;
    },
    'initHtml': function() {
        var a = this;
        var b = 'JDJRV-' + (this['params']['product'] ? this['params']['product'] : 'embed');
        var c = this['params']['width'] ? this['params']['width'] : '100%';
        var d = this['params']['placeholder'] ? this['params']['placeholder'] : a['i18nParams']['default-placeholder'];
        var e = this['params']['refreshRight'] ? this['params']['refreshRight'] : '0px';
        var f = a['lang'] && a['lang'] != 'zh_CN' ? 'JDJRV-joybuy' : '';
        var g = this['protocol'] + (a['lang'] && a['lang'] != 'zh_CN' ? '//static.joybuy.com/risk-cdn/iv/images/wait.gif' : '//ivs.jd.com/slide/i/wait.gif');
        var i = navigator['userAgent']['indexOf']('compatible') > -0x1 && navigator['userAgent']['indexOf']('MSIE') > -0x1;
        var j = '';
        if (this['params']['product'] == 'bind' || this['params']['product'] == 'popup' || this['params']['product'] == 'click-popup' || this['params']['product'] == 'e-pic-popup') {
            j += '<div\x20id=\x22JDJRV-wrap-' + this['params']['id'] + '\x22\x20class=\x22JDJRV-pop-wrap\x20JDValidate-wrap\x20' + f + '\x22><div\x20class=\x22JDJRV-pop-bg\x22></div><div\x20class=\x22JDJRV-pop-content\x22><a\x20class=\x22JDJRV-close\x22></a>';
            e = '15px';
        }
        if (this['params']['product'] == 'click-suspend') {
            j += '<div\x20id=\x22JDJRV-wrap-' + this['params']['id'] + '\x22\x20class=\x22JDJRV-click-suspend-wrap\x20JDValidate-wrap\x20' + f + '\x22><a\x20class=\x22JDJRV-close\x22></a><a\x20class=\x22JDJRV-arrow\x22></a>';
            e = '15px';
        }
        if (this['params']['product'] == 'click-bind-suspend') {
            var m = this['clickWarp']['getBoundingClientRect']()['left'] + document['documentElement']['scrollLeft'];
            var p = this['clickWarp']['getBoundingClientRect']()['top'] + document['documentElement']['scrollTop'];
            c = c['indexOf']('%') > 0x0 ? c['replace']('%', '') * 0.01 * this['clickWarp']['offsetWidth'] + 'px' : c;
            if (c['indexOf']('px') > 0x0) {
                p -= 0x8c / (0x168 / (c['replace']('px', '') - 0x18)) + 0x78;
            }
            j += '<div\x20class=\x22JDJRV-suspend-warp\x20JDJRV-bind-suspend-wrap\x20' + f + '\x22\x20id=\x22JDJRV-wrap-' + this['params']['id'] + '\x22\x20style=\x22width:\x20' + c + ';top:' + (typeof this['params']['top'] != 'undefined' ? this['params']['top'] : p + 'px') + ';left:' + m + 'px;height:' + (p + 0x70) + 'px\x22><div\x20class=\x22JDJRV-suspend-slide\x22><div\x20style=\x22\x22\x20class=\x22\x20JDValidate-wrap\x22><a\x20class=\x22JDJRV-close\x22></a>' + (typeof this['params']['top'] != 'undefined' ? '' : '<a\x20class=\x22JDJRV-arrow\x22></a>');
            e = '15px';
        }
        if (this['params']['product'] == 'i-dsc') {
            var m = this['clickWarp']['getBoundingClientRect']()['left'] + document['documentElement']['scrollLeft'];
            var p = this['clickWarp']['getBoundingClientRect']()['top'] + document['documentElement']['scrollTop'];
            c = c['indexOf']('%') > 0x0 ? c['replace']('%', '') * 0.01 * this['clickWarp']['offsetWidth'] + 'px' : c;
            if (c['indexOf']('px') > 0x0) {
                p -= 0x8c / (0x168 / (c['replace']('px', '') - 0x18)) + 0x78;
            }
            j += '<div\x20class=\x22JDJRV-suspend-warp\x20JDJRV-i-dsc-wrap\x20' + f + '\x22\x20id=\x22JDJRV-wrap-' + this['params']['id'] + '\x22\x20style=\x22width:\x20' + c + ';top:' + (typeof this['params']['top'] != 'undefined' ? this['params']['top'] : p + 'px') + ';left:' + m + 'px;height:' + (p + 0x70) + 'px\x22><div\x20class=\x22JDJRV-suspend-i-dsc\x22><div\x20style=\x22\x22\x20class=\x22\x20JDValidate-wrap\x22><a\x20class=\x22JDJRV-close\x22></a>' + (typeof this['params']['top'] != 'undefined' ? '' : '<a\x20class=\x22JDJRV-arrow\x22></a>');
            e = '15px';
        } else if (this['params']['product'] == 'i-pic-click') {
            var m = this['clickWarp']['getBoundingClientRect']()['left'] + document['documentElement']['scrollLeft'];
            var p = this['clickWarp']['getBoundingClientRect']()['top'] + document['documentElement']['scrollTop'];
            c = c['indexOf']('%') > 0x0 ? c['replace']('%', '') * 0.01 * this['clickWarp']['offsetWidth'] + 'px' : c;
            if (c['indexOf']('px') > 0x0) {
                p -= 0x14d / (0x280 / (c['replace']('px', '') - 0x18)) + 0x46;
            }
            j += '<div\x20class=\x22JDJRV-suspend-warp\x20JDJRV-i-pic-click-wrap\x20' + f + '\x22\x20id=\x22JDJRV-wrap-' + this['params']['id'] + '\x22\x20style=\x22width:\x20' + c + ';top:' + (typeof this['params']['top'] != 'undefined' ? this['params']['top'] : p + 'px') + ';left:' + m + 'px;height:' + (p + 0x70) + 'px\x22><div\x20class=\x22JDJRV-suspend-i-pic-click\x22><div\x20style=\x22\x22\x20class=\x22\x20JDValidate-wrap\x22><a\x20class=\x22JDJRV-close\x22></a>' + (typeof this['params']['top'] != 'undefined' ? '' : '<a\x20class=\x22JDJRV-arrow\x22></a>');
            e = '15px';
        }
        if (this['params']['product'] != 'click' && this['params']['product'] != 'click-bind' && this['params']['product'] != 'suspend' && this['params']['product'] != 'bind-suspend' && this['params']['product'] != 'dsc' && this['params']['product'] != 'i-dsc' && this['params']['product'] != 'pic-click' && this['params']['product'] != 'i-pic-click' && this['params']['product'] != 'e-pic-popup') {
            var q = c;
            if (this['params']['product'] == 'bind' || this['params']['product'] == 'popup' || this['params']['product'] == 'click-popup' || this['params']['product'] == 'click-suspend' || this['params']['product'] == 'click-bind-suspend') {
                q = 'auto';
            }
            j += '<div\x20class=\x22JDJRV-slide\x20' + f + '\x22\x20style=\x22width:\x20' + q + '\x22>' + '<div\x20class=\x22JDJRV-img-panel\x20' + b + '\x20' + (this['bottomSlide'] ? '' : 'JDJRV-bottom-slide-hide') + '\x22>' + '<div\x20class=\x22JDJRV-refresh\x22\x20style=\x22margin-right:\x20' + e + '\x22><div\x20class=\x22JDJRV-lable-refresh\x22>' + a['i18nParams']['default-title'] + '</div><div\x20class=\x22JDJRV-img-refresh\x22><span>' + a['i18nParams']['default-refresh'] + '</span><div></div></div></div>' + '<div\x20class=\x22JDJRV-img-wrap\x22>' + '<div\x20class=\x22JDJRV-bigimg\x22><img\x20src=\x22\x22\x20' + (i ? 'height=\x220px\x22' : '') + '></div>' + '<div\x20class=\x22JDJRV-smallimg\x22><img\x20src=\x22\x22\x20' + (i ? 'height=\x220px\x22' : '') + '></div>' + '</div>' + '</div>' + '<div\x20class=\x22JDJRV-slide-bg\x20' + (this['bottomSlide'] ? '' : 'JDJRV-hide') + '\x22>' + '<div\x20class=\x22JDJRV-slide-inner\x20JDJRV-slide-text\x22>' + '<div\x20class=\x22JDJRV-slide-left\x22></div>' + '<div\x20class=\x22JDJRV-slide-center\x22>' + d + '</div>' + '<div\x20class=\x22JDJRV-slide-right\x22></div>' + '</div>' + '<div\x20class=\x22JDJRV-slide-inner\x20JDJRV-slide-bar\x22><div\x20class=\x22JDJRV-slide-bar-left\x22></div><div\x20class=\x22JDJRV-slide-bar-center\x22></div><div\x20class=\x22JDJRV-slide-bar-right\x22></div></div>' + '<div\x20class=\x22JDJRV-slide-inner\x20JDJRV-slide-btn\x22><!--<span\x20class=\x22JDJRV-slide-icon\x22></span>--></div></div>' + '</div>';
        }
        if (this['params']['product'] == 'dsc' || this['params']['product'] == 'i-dsc') {
            if (this['params']['product'] == 'i-dsc')
                c = '100%';
            j += '<div\x20class=\x22JDJRV-dsc\x22\x20style=\x22width:\x20' + c + '\x22>' + '<div\x20class=\x22JDJRV-img-panel\x20' + b + '\x22>' + '<div\x20class=\x22JDJRV-question\x22><div\x20class=\x22JDJRV-question-lable\x22></div><div\x20class=\x22JDJRV-question-refresh\x22\x20style=\x22right:\x20' + e + '\x22><span>' + a['i18nParams']['default-refresh'] + '</span><div></div></div></div>' + '<div\x20class=\x22JDJRV-img-wrap\x22>' + '<div\x20class=\x22JDJRV-bigimg\x22><img\x20src=\x22\x22\x20' + (i ? 'height=\x220px\x22' : '') + '></div>' + '<div\x20class=\x22JDJRV-dsc-result\x22></div>' + '</div>' + '</div>' + '</div>';
        }
        if (this['params']['product'] == 'pic-click' || this['params']['product'] == 'i-pic-click' || this['params']['product'] == 'e-pic-popup') {
            if (this['params']['product'] == 'i-pic-click')
                c = '100%';
            j += '<div\x20class=\x22JDJRV-pic-click\x22\x20style=\x22width:\x20' + c + '\x22>' + '<div\x20class=\x22JDJRV-img-panel\x20' + b + '\x22>' + '<div\x20class=\x22JDJRV-question\x22><div\x20class=\x22JDJRV-question-lable\x22></div><div\x20class=\x22JDJRV-smallimg\x22></div><div\x20class=\x22JDJRV-question-refresh\x22\x20style=\x22right:\x20' + e + '\x22><span>' + a['i18nParams']['default-refresh'] + '</span><div></div></div></div>' + '<div\x20class=\x22JDJRV-img-wrap\x22>' + '<div\x20class=\x22JDJRV-bigimg\x22><img\x20src=\x22\x22\x20' + (i ? 'height=\x220px\x22' : '') + '></div>' + '<div\x20class=\x22JDJRV-oper\x22>' + '<div\x20class=\x22JDJRV-seq\x22\x20data-i=\x221\x22>1</div>' + '<div\x20class=\x22JDJRV-seq\x22\x20data-i=\x222\x22>2</div>' + '<div\x20class=\x22JDJRV-seq\x22\x20data-i=\x223\x22>3</div>' + '<div\x20class=\x22JDJRV-seq\x22\x20data-i=\x224\x22>4</div>' + '<div\x20class=\x22JDJRV-seq\x22\x20data-i=\x225\x22>5</div>' + '<div\x20class=\x22JDJRV-seq\x22\x20data-i=\x226\x22>6</div>' + '<div\x20class=\x22JDJRV-seq\x22\x20data-i=\x227\x22>7</div>' + '<div\x20class=\x22JDJRV-seq\x22\x20data-i=\x228\x22>8</div>' + '<div\x20class=\x22JDJRV-seq\x22\x20data-i=\x229\x22>9</div>' + '</div>' + '<div\x20class=\x22JDJRV-pic-click-result\x22></div>' + '</div>' + '</div>' + '</div>';
        }
        if (this['params']['product'] == 'bind' || this['params']['product'] == 'popup' || this['params']['product'] == 'click-popup' || this['params']['product'] == 'e-pic-popup') {
            j += '</div></div>';
            var s = document['createElement']('div');
            s['innerHTML'] = j;
            var u = document['createDocumentFragment']();
            while (s['firstChild']) {
                u['appendChild'](s['firstChild']);
            }
            var w = this['getByID']('JDJRV-wrap-' + this['params']['id']);
            if (w) {
                document['body']['removeChild'](w);
            }
            document['body']['appendChild'](u);
            this['warp'] = this['getByID']('JDJRV-wrap-' + this['params']['id']);
            if (!this['warp']['getElementsByClassName'])
                this['initGetElementsByName'](this['warp']);
            this['closeBtn'] = this['warp']['getElementsByClassName']('JDJRV-close')[0x0];
            this['popContent'] = this['warp']['getElementsByClassName']('JDJRV-pop-content')[0x0];
            if (this['params']['product'] == 'popup') {
                this['clickWarp'] = this['getByID'](this['params']['id']);
                var B = '<div\x20class=\x22JDJRV-click-warp\x20' + f + '\x22\x20style=\x22width:\x20' + c + '\x22><img\x20class=\x22JDJRV-click-img\x22\x20src=\x22' + g + '\x22><div\x20class=\x22JDJRV-click-text\x22>' + a['i18nParams']['default-click'] + '</div></div>';
                this['clickWarp']['innerHTML'] = B;
                if (!this['clickWarp']['getElementsByClassName'])
                    this['initGetElementsByName'](this['clickWarp']);
                this['clickContent'] = this['clickWarp']['getElementsByClassName']('JDJRV-click-warp')[0x0];
                this['clickImg'] = this['clickWarp']['getElementsByClassName']('JDJRV-click-img')[0x0];
                this['clickText'] = this['clickWarp']['getElementsByClassName']('JDJRV-click-text')[0x0];
            }
        } else if (this['params']['product'] == 'click') {
            this['clickWarp'] = this['getByID'](this['params']['id']);
            var B = '<div\x20class=\x22JDJRV-click-warp\x20' + f + '\x22\x20style=\x22width:\x20' + c + '\x22><img\x20class=\x22JDJRV-click-img\x22\x20src=\x22' + g + '\x22><div\x20class=\x22JDJRV-click-text\x22>' + a['i18nParams']['default-click'] + '</div></div>';
            this['clickWarp']['innerHTML'] = B;
            if (!this['clickWarp']['getElementsByClassName'])
                this['initGetElementsByName'](this['clickWarp']);
            this['clickContent'] = this['clickWarp']['getElementsByClassName']('JDJRV-click-warp')[0x0];
            this['clickImg'] = this['clickWarp']['getElementsByClassName']('JDJRV-click-img')[0x0];
            this['clickText'] = this['clickWarp']['getElementsByClassName']('JDJRV-click-text')[0x0];
        } else if (this['params']['product'] == 'click-bind' || this['params']['product'] == 'bind-suspend') {
            this['clickWarp'] = this['getByID'](this['params']['id']);
            if (!this['clickWarp']['getElementsByClassName'])
                this['initGetElementsByName'](this['clickWarp']);
        } else if (this['params']['product'] == 'suspend') {
            this['warp'] = this['getByID'](this['params']['id']);
            if (!this['warp']['getElementsByClassName'])
                this['initGetElementsByName'](this['warp']);
            var C = this['params']['height'] || '40px';
            var B = '<div\x20class=\x22JDJRV-suspend-warp\x20' + f + '\x22\x20style=\x22width:\x20' + c + '\x22><div\x20class=\x22JDJRV-suspend-slide\x22></div><div\x20class=\x22JDJRV-suspend-click\x22\x20style=\x22;height:' + C + ';line-height:' + C + '\x22>' + a['i18nParams']['default-click'] + '</div></div>';
            this['warp']['innerHTML'] = B;
            this['clickWarp'] = this['warp']['getElementsByClassName']('JDJRV-suspend-click')[0x0];
            this['clickContent'] = this['warp']['getElementsByClassName']('JDJRV-suspend-click')[0x0];
            this['clickText'] = this['warp']['getElementsByClassName']('JDJRV-suspend-click')[0x0];
            this['suspendSlideWarp'] = this['warp']['getElementsByClassName']('JDJRV-suspend-slide')[0x0];
            this['suspendSlideWarp']['style']['bottom'] = this['clickWarp']['offsetHeight'] + 0x6 + 'px';
        } else if (this['params']['product'] == 'click-suspend') {
            j += '</div></div>';
            this['suspendSlideWarp']['innerHTML'] = j;
            this['suspendSlideWarp']['style']['display'] = 'block';
            this['closeBtn'] = this['warp']['getElementsByClassName']('JDJRV-close')[0x0];
        } else if (this['params']['product'] == 'click-bind-suspend' || this['params']['product'] == 'i-dsc' || this['params']['product'] == 'i-pic-click') {
            j += '</div></div></div></div>';
            var s = document['createElement']('div');
            s['innerHTML'] = j;
            var u = document['createDocumentFragment']();
            while (s['firstChild']) {
                u['appendChild'](s['firstChild']);
            }
            var w = this['getByID']('JDJRV-wrap-' + this['params']['id']);
            if (w) {
                document['body']['removeChild'](w);
            }
            document['body']['appendChild'](u);
            this['warp'] = this['getByID']('JDJRV-wrap-' + this['params']['id']);
            if (!this['warp']['getElementsByClassName'])
                this['initGetElementsByName'](this['warp']);
            this['closeBtn'] = this['warp']['getElementsByClassName']('JDJRV-close')[0x0];
            if (this['params']['product'] == 'click-bind-suspend' || this['params']['product'] == 'i-dsc') {
                this['suspendSlideWarp'] = this['warp']['getElementsByClassName']('JDJRV-suspend-slide')[0x0];
            } else if (this['params']['product'] == 'i-pic-click') {
                this['suspendPicClickWarp'] = this['warp']['getElementsByClassName']('JDJRV-suspend-pic-click')[0x0];
            }
        } else {
            this['warp']['innerHTML'] = j;
        }
        if (this['params']['product'] != 'click' && this['params']['product'] != 'click-bind' && this['params']['product'] != 'suspend' && this['params']['product'] != 'bind-suspend' && this['params']['product'] != 'dsc' && this['params']['product'] != 'i-dsc' && this['params']['product'] != 'pic-click' && this['params']['product'] != 'i-pic-click' && this['params']['product'] != 'e-pic-popup') {
            if (this['params']['product'] == 'click-popup' || this['params']['product'] == 'click-suspend' || this['params']['product'] == 'click-bind-suspend') {
                a['initSlideWrap']();
            } else {
                setTimeout(function() {
                    a['initSlideWrap']();
                }, 0x32);
            }
        } else if (this['params']['product'] == 'dsc' || this['params']['product'] == 'i-dsc') {
            setTimeout(function() {
                a['initDscWrap']();
            }, 0x32);
        } else if (this['params']['product'] == 'pic-click' || this['params']['product'] == 'i-pic-click' || this['params']['product'] == 'e-pic-popup') {
            setTimeout(function() {
                a['initPicClickWrap']();
            }, 0x32);
        } else {
            setTimeout(function() {
                a['initClickWrap']();
            }, 0x32);
        }
    },
    'initSlideWrap': function() {
        if (!this['warp']['getElementsByClassName'])
            this['initGetElementsByName'](this['warp']);
        this['slideWrap'] = this['warp']['getElementsByClassName']('JDJRV-slide')[0x0];
        this['width'] = this['slideWrap']['offsetWidth'];
        this['imgRatio'] = this['slideWrap']['offsetWidth'] ? 0x168 / this['slideWrap']['offsetWidth'] : 0x1;
        this['slideBar'] = this['warp']['getElementsByClassName']('JDJRV-slide-bg')[0x0];
        this['slideBtn'] = this['warp']['getElementsByClassName']('JDJRV-slide-btn')[0x0];
        this['slideGreenBar'] = this['warp']['getElementsByClassName']('JDJRV-slide-bar')[0x0];
        this['slideGreenBarCenter'] = this['warp']['getElementsByClassName']('JDJRV-slide-bar-center')[0x0];
        this['slideSmallImg'] = this['warp']['getElementsByClassName']('JDJRV-smallimg')[0x0];
        this['slideBigImg'] = this['warp']['getElementsByClassName']('JDJRV-bigimg')[0x0];
        this['slideImgWrap'] = this['warp']['getElementsByClassName']('JDJRV-img-panel')[0x0];
        this['slideCenter'] = this['warp']['getElementsByClassName']('JDJRV-slide-center')[0x0];
        if (!this['slideImgWrap']['getElementsByClassName'])
            this['initGetElementsByName'](this['slideImgWrap']);
        this['refreshBtn'] = this['slideImgWrap']['getElementsByClassName']('JDJRV-img-refresh')[0x0];
        this['slideText'] = this['warp']['getElementsByClassName']('JDJRV-slide-text')[0x0];
        this['slideBigImg']['style']['height'] = 0x8c / (0x168 / this['slideWrap']['offsetWidth']) + 'px';
        this['getValidateImage']();
        this['bindEvent']();
    },
    'initClickWrap': function() {
        var a = this;
        a['getValidateImage']();
        if (a['params']['eventListener'] == ![] || a['params']['eventListener'] == 'false') {
            a['verify'] = c;
        } else {
            a['clickWarp']['onclick'] = c;
            if (a['params']['formId']) {
                document['getElementById'](a['params']['formId'])['onsubmit'] = function() {
                    c();
                    return ![];
                }
                ;
            }
        }
        document['onmousemove'] = b;
        document['ontouchmove'] = b;
        function b(d) {
            if (a['params']['product'] == 'click' || a['params']['product'] == 'click-bind' || a['params']['product'] == 'suspend' || a['params']['product'] == 'bind-suspend') {
                var e = d || event;
                if (e['touches'])
                    e = e['touches'][0x0];
                a['clickProductData']['push']([e['clientX']['toFixed'](0x0), e['clientY']['toFixed'](0x0), new Date()['getTime']()]);
            }
        }
        function c() {
            if (!a['clickResult']) {
                if (a['params']['product'] == 'click-popup' || a['params']['product'] == 'e-pic-popup') {
                    a['warp']['style']['display'] = 'block';
                    a['resetSize']();
                } else if (a['params']['product'] == 'click-suspend') {
                    a['suspendSlideWarp']['style']['display'] = 'block';
                    a['resetSize']();
                } else if (a['params']['product'] == 'click-bind-suspend') {
                    a['warp']['style']['display'] = 'block';
                    a['resetSize']();
                } else if (a['params']['product'] == 'i-dsc') {
                    a['warp']['style']['display'] = 'block';
                } else if (a['params']['product'] == 'i-pic-click') {
                    a['warp']['style']['display'] = 'block';
                } else {
                    if (a['validateID']) {
                        a['submit']();
                    }
                }
            }
        }
    },
    'initDscWrap': function() {
        if (!this['warp']['getElementsByClassName'])
            this['initGetElementsByName'](this['warp']);
        this['dscWrap'] = this['warp']['getElementsByClassName']('JDJRV-dsc')[0x0];
        this['width'] = this['dscWrap']['offsetWidth'];
        this['imgRatio'] = this['dscWrap']['offsetWidth'] ? 0x168 / this['dscWrap']['offsetWidth'] : 0x1;
        this['dscBigImg'] = this['warp']['getElementsByClassName']('JDJRV-bigimg')[0x0];
        this['dscResult'] = this['warp']['getElementsByClassName']('JDJRV-dsc-result')[0x0];
        this['dscWrapImgWrap'] = this['warp']['getElementsByClassName']('JDJRV-img-panel')[0x0];
        if (!this['dscWrapImgWrap']['getElementsByClassName'])
            this['initGetElementsByName'](this['dscWrapImgWrap']);
        this['refreshBtn'] = this['dscWrapImgWrap']['getElementsByClassName']('JDJRV-question-refresh')[0x0];
        this['dscBigImg']['style']['height'] = 0xbe / (0x168 / this['dscWrap']['offsetWidth']) + 'px';
        this['questionLable'] = this['warp']['getElementsByClassName']('JDJRV-question-lable')[0x0];
        this['getValidateImage']();
        this['bindDscEvent']();
    },
    'initPicClickWrap': function() {
        if (!this['warp']['getElementsByClassName'])
            this['initGetElementsByName'](this['warp']);
        this['picClickWrap'] = this['warp']['getElementsByClassName']('JDJRV-pic-click')[0x0];
        this['width'] = this['picClickWrap']['offsetWidth'];
        this['imgRatio'] = this['picClickWrap']['offsetWidth'] ? 0x280 / this['picClickWrap']['offsetWidth'] : 0x1;
        this['picClickBigImg'] = this['warp']['getElementsByClassName']('JDJRV-bigimg')[0x0];
        this['picClickSmallImg'] = this['warp']['getElementsByClassName']('JDJRV-smallimg')[0x0];
        this['picClickResult'] = this['warp']['getElementsByClassName']('JDJRV-pic-click-result')[0x0];
        this['picClickImgWrap'] = this['warp']['getElementsByClassName']('JDJRV-img-panel')[0x0];
        if (!this['picClickImgWrap']['getElementsByClassName'])
            this['initGetElementsByName'](this['picClickImgWrap']);
        this['refreshBtn'] = this['picClickImgWrap']['getElementsByClassName']('JDJRV-question-refresh')[0x0];
        this['picClickBigImg']['style']['height'] = 0x14d / (0x280 / this['picClickWrap']['offsetWidth']) + 'px';
        this['questionLable'] = this['warp']['getElementsByClassName']('JDJRV-question-lable')[0x0];
        this['operWrap'] = this['warp']['getElementsByClassName']('JDJRV-oper')[0x0];
        this['operSeqs'] = this['warp']['getElementsByClassName']('JDJRV-seq');
        this['getValidateImage']();
        this['bindPicClickEvent']();
    },
    'bindEvent': function() {
        var a = this;
        if (a['params']['product'] == 'click-popup') {
            a['closeBtn']['onclick'] = function() {
                a['warp']['style']['display'] = 'none';
            }
            ;
        }
        if (a['params']['product'] == 'click-suspend') {
            a['closeBtn']['onclick'] = function() {
                a['suspendSlideWarp']['style']['display'] = 'none';
            }
            ;
        }
        if (a['params']['product'] == 'click-bind-suspend') {
            a['closeBtn']['onclick'] = function() {
                a['warp']['style']['display'] = 'none';
            }
            ;
        }
        if (a['params']['product'] == 'popup') {
            a['clickWarp']['onclick'] = function() {
                a['warp']['style']['display'] = 'block';
                a['resetSize']();
            }
            ;
            a['closeBtn']['onclick'] = function() {
                a['warp']['style']['display'] = 'none';
            }
            ;
        }
        if (a['params']['product'] == 'bind') {
            if (a['params']['eventListener'] == ![] || a['params']['eventListener'] == 'false') {
                a['verify'] = function() {
                    a['warp']['style']['display'] = 'block';
                    a['resetSize']();
                }
                ;
            } else {
                document['getElementById'](a['params']['id'])['onclick'] = function() {
                    a['warp']['style']['display'] = 'block';
                    a['resetSize']();
                }
                ;
            }
            a['closeBtn']['onclick'] = function() {
                a['warp']['style']['display'] = 'none';
            }
            ;
        }
        a['slideBtn']['onmousedown'] = b;
        a['slideBtn']['ontouchstart'] = b;
        a['slideSmallImg']['onmousedown'] = b;
        a['slideSmallImg']['ontouchstart'] = b;
        function b(f) {
            if (a['passValidate'])
                return;
            a['isDraging'] = !![];
            var g = f || event;
            if (document['all']) {
                window['event']['returnValue'] = ![];
                window['event']['cancelBubble'] = !![];
            } else {
                g['preventDefault']();
                g['stopPropagation']();
                g['returnValue'] = ![];
            }
            ;if (g['touches'])
                g = g['touches'][0x0];
            a['disX'] = g['clientX'];
            a['slideGreenBar']['style']['display'] = 'block';
            a['mousePos'] = [];
            a['mousePos']['push']([a['getLeft'](a['slideBtn'])['toFixed'](0x0), a['getTop'](a['slideBtn'])['toFixed'](0x0), new Date()['getTime']()]);
            a['mousePos']['push']([g['clientX']['toFixed'](0x0), g['clientY']['toFixed'](0x0), new Date()['getTime']()]);
            document['onmousemove'] = h;
            document['ontouchmove'] = h;
            document['onmouseup'] = j;
            document['ontouchend'] = j;
            function h(k) {
                var l = k || event;
                if (document['all']) {
                    window['event']['returnValue'] = ![];
                    window['event']['cancelBubble'] = !![];
                } else {
                    l['preventDefault']();
                    l['stopPropagation']();
                    l['returnValue'] = ![];
                }
                ;if (l['touches'])
                    l = l['touches'][0x0];
                var m = l['clientX'] - a['disX'] + 0x28;
                var n = l['clientX'] - a['disX'];
                var o = l['clientX'] - a['disX'];
                if (o < 0x0) {
                    o = 0x0;
                } else if (o > a['width'] - 0x32 / a['imgRatio']) {
                    o = a['width'] - 0x32 / a['imgRatio'];
                }
                if (n < 0x0) {
                    n = 0x0;
                } else if (n > a['width'] - 0x28) {
                    n = a['width'] - 0x28;
                }
                if (m < 0x2c) {
                    m = 0x2c;
                } else if (m > a['width']) {
                    m = a['width'];
                }
                a['mousePos']['push']([l['clientX']['toFixed'](0x0), l['clientY']['toFixed'](0x0), new Date()['getTime']()]);
                a['slideBtn']['style']['left'] = n + 'px';
                a['slideSmallImg']['style']['left'] = o + 'px';
                a['slideGreenBar']['style']['width'] = m + 'px';
                return ![];
            }
            ;function j(k) {
                var l = k || event;
                if (l['changedTouches'])
                    l = l['changedTouches'][0x0];
                a['isDraging'] = ![];
                a['mousePos']['push']([l['clientX']['toFixed'](0x0), l['clientY']['toFixed'](0x0), new Date()['getTime']()]);
                document['onmousemove'] = null;
                document['ontouchmove'] = null;
                document['onmouseup'] = null;
                document['ontouchend'] = null;
                if (a['mousePos']['length'] <= 0x3) {
                    a['slideGreenBar']['style']['display'] = 'none';
                    a['slideText']['setAttribute']('class', 'JDJRV-slide-inner\x20JDJRV-slide-text');
                    a['slideText']['setAttribute']('className', 'JDJRV-slide-inner\x20JDJRV-slide-text');
                    return;
                }
                a['submit']();
            }
        }
        ;if (this['params']['product'] == 'float') {
            var c = ![];
            var d = ![];
            this['slideImgWrap']['onmouseover'] = function() {
                c = !![];
            }
            ;
            this['slideImgWrap']['onmouseout'] = function() {
                c = ![];
                a['slideTimer'] = setTimeout(function() {
                    if (c || d)
                        return;
                    a['slideImgWrap']['setAttribute']('class', 'JDJRV-img-panel\x20JDJRV-float');
                    a['slideImgWrap']['setAttribute']('className', 'JDJRV-img-panel\x20JDJRV-float\x20');
                }, 0x12c);
            }
            ;
            this['slideBar']['onmouseover'] = function() {
                d = !![];
                if (a['passValidate'] || a['isDraging'])
                    return;
                clearTimeout(a['slideTimer']);
                a['slideImgWrap']['setAttribute']('class', 'JDJRV-img-panel\x20JDJRV-float\x20JDJRV-float-hover');
                a['slideImgWrap']['setAttribute']('className', 'JDJRV-img-panel\x20JDJRV-float\x20JDJRV-float-hover');
            }
            ;
            this['slideBar']['onmouseout'] = function() {
                d = ![];
                if (a['isDraging'])
                    return;
                a['slideTimer'] = setTimeout(function() {
                    if (c)
                        return;
                    a['slideImgWrap']['setAttribute']('class', 'JDJRV-img-panel\x20JDJRV-float');
                    a['slideImgWrap']['setAttribute']('className', 'JDJRV-img-panel\x20JDJRV-float\x20');
                }, 0x12c);
            }
            ;
        }
        this['refreshBtn']['onclick'] = function() {
            if (a['passValidate'] || a['isDraging'])
                return;
            a['getValidateImage']();
            if (a['params']['refreshCallback']) {
                a['callback']({
                    'getSuccess': function() {
                        return '2';
                    },
                    'getMessage': function() {
                        return 'refresh';
                    },
                    'getValidate': function() {
                        return '';
                    }
                });
            }
        }
        ;
        var e = 0x0;
        window['onresize'] = function() {
            a['resetSize']();
        }
        ;
    },
    'bindDscEvent': function() {
        var a = this;
        if (a['params']['product'] == 'i-dsc') {
            a['closeBtn']['onclick'] = function() {
                a['warp']['style']['display'] = 'none';
            }
            ;
        }
        document['onmousemove'] = b;
        document['ontouchmove'] = b;
        a['dscBigImg']['onmousedown'] = c;
        function b(d) {
            var e = d || event;
            if (document['all']) {
                window['event']['returnValue'] = ![];
                window['event']['cancelBubble'] = !![];
            } else {
                e['preventDefault']();
                e['stopPropagation']();
                e['returnValue'] = ![];
            }
            ;if (e['touches'])
                e = e['touches'][0x0];
            a['mousePos']['push']([e['clientX']['toFixed'](0x0), e['clientY']['toFixed'](0x0), new Date()['getTime']()]);
            return ![];
        }
        ;function c(d) {
            var e = d || event;
            if (e['changedTouches'])
                e = e['changedTouches'][0x0];
            a['isDraging'] = ![];
            a['mousePos']['push']([e['clientX']['toFixed'](0x0), e['clientY']['toFixed'](0x0), new Date()['getTime']()]);
            a['mousePos']['push']([a['getLeft'](a['dscBigImg'])['toFixed'](0x0), a['getTop'](a['dscBigImg'])['toFixed'](0x0), new Date()['getTime']()]);
            var f = e['offsetX'] || e['clientX'] - a['dscBigImg']['getBoundingClientRect']()['left'];
            var g = e['offsetY'] || e['clientY'] - a['dscBigImg']['getBoundingClientRect']()['top'];
            a['mousePos']['push']([f['toFixed'](0x0), g['toFixed'](0x0), new Date()['getTime']()]);
            a['mousePos']['push']([0x0, 0x0, new Date()['getTime']()]);
            document['onmousemove'] = null;
            document['ontouchmove'] = null;
            a['dscBigImg']['onmousedown'] = null;
            a['submit']();
        }
        this['refreshBtn']['onclick'] = function() {
            if (a['passValidate'] || a['isDraging'])
                return;
            a['getValidateImage']();
            if (a['params']['refreshCallback']) {
                a['callback']({
                    'getSuccess': function() {
                        return '2';
                    },
                    'getMessage': function() {
                        return 'refresh';
                    },
                    'getValidate': function() {
                        return '';
                    }
                });
            }
        }
        ;
        window['onresize'] = function() {
            a['resetSize']();
        }
        ;
    },
    'bindPicClickEvent': function() {
        var a = this;
        if (a['params']['product'] == 'i-pic-click') {
            a['closeBtn']['onclick'] = function() {
                a['warp']['style']['display'] = 'none';
            }
            ;
        }
        if (a['params']['product'] == 'e-pic-popup') {
            if (a['params']['eventListener'] == ![] || a['params']['eventListener'] == 'false') {
                a['verify'] = function() {
                    a['warp']['style']['display'] = 'block';
                    a['resetSize']();
                }
                ;
            } else {
                document['getElementById'](a['params']['id'])['onclick'] = function() {
                    a['warp']['style']['display'] = 'block';
                    a['resetSize']();
                }
                ;
            }
            a['closeBtn']['onclick'] = function() {
                a['warp']['style']['display'] = 'none';
            }
            ;
        }
        a['picClickBigImg']['onmousedown'] = b;
        function b(e) {
            var f = e || event;
            if (f['changedTouches'])
                f = f['changedTouches'][0x0];
            a['isDraging'] = ![];
            var g = f['offsetX'] || f['clientX'] - a['dscBigImg']['getBoundingClientRect']()['left'];
            var h = f['offsetY'] || f['clientY'] - a['dscBigImg']['getBoundingClientRect']()['top'];
            a['mousePos']['push']([g['toFixed'](0x0), h['toFixed'](0x0), new Date()['getTime']()]);
            var j = a['operSeqs'][a['mousePos']['length'] - 0x1];
            j['style']['top'] = h - 0xd + 'px';
            j['style']['left'] = g - 0xd + 'px';
            j['style']['display'] = 'block';
            if (a['mousePos']['length'] == (a['operLimit'] || 0x4)) {
                a['picClickBigImg']['onmousedown'] = null;
                a['submit']();
            }
        }
        for (var c = 0x0; c < a['operSeqs']['length']; c++) {
            var d = a['operSeqs'][c];
            d['onmousedown'] = function() {
                var e = this['getAttribute']('data-i') * 0x1;
                a['mousePos'] = a['mousePos']['slice'](0x0, e - 0x1);
                for (var f = a['operSeqs']['length']; f > e - 0x1; f--) {
                    a['operSeqs'][f - 0x1]['style']['display'] = 'none';
                }
            }
            ;
        }
        this['refreshBtn']['onclick'] = function() {
            if (a['passValidate'] || a['isDraging'])
                return;
            a['mousePos'] = new Array();
            for (var e = 0x0; e < a['operSeqs']['length']; e++) {
                a['operSeqs'][e]['style']['display'] = 'none';
            }
            a['getValidateImage']();
            if (a['params']['refreshCallback']) {
                a['callback']({
                    'getSuccess': function() {
                        return '2';
                    },
                    'getMessage': function() {
                        return 'refresh';
                    },
                    'getValidate': function() {
                        return '';
                    }
                });
            }
        }
        ;
        window['onresize'] = function() {
            a['resetSize']();
        }
        ;
    },
    'getInstance': function() {
        var a = this;
        if (a['params']['getInstance']) {
            a['params']['getInstance'](a);
        }
    },
    'resetSize': function() {
        var a = this;
        if (a['y']) {
            a['width'] = a['slideWrap']['offsetWidth'];
            var b = a['imgRatio'];
            a['imgRatio'] = a['slideWrap']['offsetWidth'] ? 0x168 / a['slideWrap']['offsetWidth'] : 0x0;
            a['slideSmallImg']['style']['top'] = a['y'] / a['imgRatio'] + 'px';
            a['slideSmallImg']['style']['width'] = 0x32 / a['imgRatio'] + 'px';
            a['slideBigImg']['style']['height'] = 0x8c / (0x168 / a['slideWrap']['offsetWidth']) + 'px';
            a['slideSmallImg']['style']['left'] = a['slideSmallImg']['offsetLeft'] * b / a['imgRatio'] + 'px';
        }
        if (a['params']['product'] == 'bind' || a['params']['product'] == 'popup' || a['params']['product'] == 'click-popup' || a['params']['product'] == 'e-pic-popup') {
            a['popContent']['style']['marginLeft'] = a['popContent']['offsetWidth'] < 0x168 ? document['body']['clientWidth'] * -0.432 + 'px' : a['popContent']['offsetWidth'] / 0x2 * -0x1 + 'px';
        }
        if (a['params']['product'] == 'click-bind-suspend' && a['slideWrap']) {
            var e = a['clickWarp']['getBoundingClientRect']()['left'] + document['documentElement']['scrollLeft'];
            var h = a['clickWarp']['getBoundingClientRect']()['top'] + document['documentElement']['scrollTop'];
            h -= 0x8c / (0x168 / a['slideWrap']['offsetWidth']) + 0x78;
            a['warp']['style']['top'] = typeof a['params']['top'] != 'undefined' ? a['params']['top'] : h + 'px';
            a['warp']['style']['left'] = e + 'px';
        }
        if (a['params']['product'] == 'i-dsc' && a['dscWrap']) {
            var e = a['clickWarp']['getBoundingClientRect']()['left'] + document['documentElement']['scrollLeft'];
            var h = a['clickWarp']['getBoundingClientRect']()['top'] + document['documentElement']['scrollTop'];
            h -= 0xbe / (0x168 / a['dscWrap']['offsetWidth']) + 0x46;
            a['warp']['style']['top'] = typeof a['params']['top'] != 'undefined' ? a['params']['top'] : h + 'px';
            a['warp']['style']['left'] = e + 'px';
            a['width'] = a['dscWrap']['offsetWidth'];
        }
        if (a['params']['product'] == 'i-pic-click' && a['picClickWrap']) {
            var e = a['clickWarp']['getBoundingClientRect']()['left'] + document['documentElement']['scrollLeft'];
            var h = a['clickWarp']['getBoundingClientRect']()['top'] + document['documentElement']['scrollTop'];
            h -= 0x14d / (0x280 / a['picClickWrap']['offsetWidth']) + 0x46;
            a['warp']['style']['top'] = typeof a['params']['top'] != 'undefined' ? a['params']['top'] : h + 'px';
            a['warp']['style']['left'] = e + 'px';
            a['width'] = a['picClickWrap']['offsetWidth'];
        }
        if (a['params']['product'] == 'e-pic-popup' && a['picClickWrap']) {
            this['width'] = this['picClickWrap']['offsetWidth'];
            this['picClickBigImg']['style']['height'] = 0x14d / (0x280 / this['picClickWrap']['offsetWidth']) + 'px';
        }
    },
    'resetValidate': function() {
        var a = this;
        setTimeout(function() {
            a['slideBtn']['setAttribute']('class', 'JDJRV-slide-inner\x20JDJRV-slide-btn\x20JRJRV-animate-el');
            a['slideBtn']['setAttribute']('className', 'JDJRV-slide-inner\x20JDJRV-slide-btn\x20JRJRV-animate-el');
            a['slideGreenBar']['setAttribute']('class', 'JDJRV-slide-inner\x20JDJRV-slide-bar\x20JRJRV-animate-el');
            a['slideGreenBar']['setAttribute']('className', 'JDJRV-slide-inner\x20JDJRV-slide-bar\x20JRJRV-animate-el');
            a['slideWrap']['setAttribute']('class', 'JDJRV-slide');
            a['slideWrap']['setAttribute']('className', 'JDJRV-slide');
            a['slideBtn']['style']['left'] = '0px';
            a['slideGreenBar']['style']['width'] = '0';
            a['slideText']['setAttribute']('class', 'JDJRV-slide-inner\x20JDJRV-slide-text');
            a['slideText']['setAttribute']('className', 'JDJRV-slide-inner\x20JDJRV-slide-text');
            setTimeout(function() {
                a['slideBtn']['setAttribute']('class', 'JDJRV-slide-inner\x20JDJRV-slide-btn');
                a['slideBtn']['setAttribute']('className', 'JDJRV-slide-inner\x20JDJRV-slide-btn');
                a['slideGreenBar']['setAttribute']('class', 'JDJRV-slide-inner\x20JDJRV-slide-bar');
                a['slideGreenBar']['setAttribute']('className', 'JDJRV-slide-inner\x20JDJRV-slide-bar');
            }, 0x190);
        }, 0x258);
    },
    'getValidateImage': function() {
        var a = this;
        a['jsonp'](a['apiServer'] + '/slide/g.html', {
            'appId': a['params']['appId'],
            'scene': a['params']['scene'],
            'product': a['params']['product'],
            'e': a['getEid'](),
            'j': a['getJsTk'](),
            'lang': a['lang'] ? a['lang'] : 'zh_CN'
        }, 'callback', function(b) {
            if (a['params']['product'] != 'click' && a['params']['product'] != 'click-bind' && a['params']['product'] != 'suspend' && a['params']['product'] != 'bind-suspend' && a['params']['product'] != 'dsc' && a['params']['product'] != 'i-dsc' && a['params']['product'] != 'pic-click' && a['params']['product'] != 'i-pic-click' && a['params']['product'] != 'e-pic-popup') {
                a['slideBigImg']['innerHTML'] = '<img\x20src=\x22' + a['getImgSrc'](b['static_servers'], b['bg']) + '\x22>';
                a['slideSmallImg']['innerHTML'] = '<img\x20src=\x22' + a['getImgSrc'](b['static_servers'], b['patch']) + '\x22>';
                a['y'] = b['y'];
                a['slideSmallImg']['style']['top'] = b['y'] / a['imgRatio'] + 'px';
                a['slideSmallImg']['style']['width'] = 0x32 / a['imgRatio'] + 'px';
                a['slideSmallImg']['style']['left'] = 0x0 + 'px';
            } else if (a['params']['product'] == 'dsc' || a['params']['product'] == 'i-dsc') {
                a['dscBigImg']['innerHTML'] = '<img\x20src=\x22' + a['getImgSrc'](b['static_servers'], b['bg']) + '\x22>';
                a['questionLable']['innerHTML'] = b['desc'];
            } else if (a['params']['product'] == 'pic-click' || a['params']['product'] == 'i-pic-click' || a['params']['product'] == 'e-pic-popup') {
                a['picClickBigImg']['innerHTML'] = '<img\x20src=\x22' + a['getImgSrc'](b['static_servers'], b['bg']) + '\x22>';
                a['questionLable']['innerHTML'] = b['desc'] + '<img\x20src=\x22' + a['getImgSrc'](b['static_servers'], b['cp']) + '\x22>';
                a['operLimit'] = b['n'];
                a['picClickResult']['style']['bottom'] = '-30px';
            }
            a['validateID'] = b['challenge'];
            a['o'] = b['o'];
            setTimeout(function() {
                a['resetSize']();
            }, 0x3c);
            setTimeout(function() {
                a['resetSize']();
            }, 0x3e8);
        });
    },
    'submit': function() {
        var a = this;
        var b;
        if (a['params']['product'] == 'click' || a['params']['product'] == 'click-bind' || a['params']['product'] == 'suspend' || a['params']['product'] == 'bind-suspend') {
            b = a['clickProductData'];
            var f = b['length'];
            if (f > 0x12c) {
                b = a['clickProductData']['slice'](f - 0x12c, f);
            }
        } else if (a['params']['product'] == 'dsc' || a['params']['product'] == 'i-dsc') {
            b = a['mousePos'];
            var f = b['length'];
            if (f > 0x12c) {
                b = a['mousePos']['slice'](f - 0x12c, f);
            }
        } else {
            b = a['mousePos'];
        }
        var g = '';
        if (a['o']) {
            try {
                var h = a['getByID'](a['o']);
                if (h) {
                    g = encodeURIComponent(h['value']);
                }
            } catch (i) {}
        }
        a['jsonp'](a['apiServer'] + '/slide/s.html', {
            'd': a['getCoordinate'](b),
            'c': a['validateID'],
            'w': a['width'] ? a['width']['toFixed'](0x0) : 0x0,
            'appId': a['params']['appId'],
            'scene': a['params']['scene'],
            'product': a['params']['product'],
            'e': a['getEid'](),
            'j': a['getJsTk'](),
            's': a['getSessionId'](),
            'o': g,
            'o1': a['getSelenium'](),
            'u': a['getUrl'](),
            'lang': a['lang'] ? a['lang'] : 'zh_CN'
        }, 'callback', function(j) {
            if (a['params']['product'] == 'click' || a['params']['product'] == 'click-bind' || a['params']['product'] == 'suspend' || a['params']['product'] == 'bind-suspend') {
                if (j['success'] == 0x0) {
                    if (a['params']['product'] == 'suspend') {
                        a['params']['product'] = 'click-suspend';
                    } else if (a['params']['product'] == 'bind-suspend') {
                        if (j['nextVerify'] == 'DSC_VERIFY') {
                            a['params']['product'] = 'i-dsc';
                        } else if (j['nextVerify'] == 'PIC_CLICK_VERIFY') {
                            a['params']['product'] = 'i-pic-click';
                        } else {
                            a['params']['product'] = 'click-bind-suspend';
                        }
                    } else {
                        a['params']['product'] = 'click-popup';
                    }
                    a['initHtml']();
                    a['warp']['style']['display'] = 'block';
                    setTimeout(function() {
                        a['resetSize']();
                    }, 0x3c);
                    setTimeout(function() {
                        a['resetSize']();
                    }, 0x3e8);
                } else {
                    a['clickSuccess']();
                }
            } else if (a['params']['product'] == 'dsc' || a['params']['product'] == 'i-dsc') {
                var k = a['mousePos'][a['mousePos']['length'] - 0x1];
                var m = a['mousePos'][a['mousePos']['length'] - 0x2];
                a['dscResult']['style']['top'] = m[0x1] - k[0x1] - 0x14 + 'px';
                a['dscResult']['style']['left'] = m[0x0] - k[0x0] - 0x14 + 'px';
                a['dscResult']['style']['display'] = 'block';
                if (j['success'] == 0x0) {
                    a['dscResult']['setAttribute']('class', 'JDJRV-dsc-result\x20JDJRV-dsc-result-err');
                    a['dscResult']['setAttribute']('className', 'JDJRV-dsc-result\x20JDJRV-dsc-result-err');
                    if (a['params']['product'] == 'i-dsc') {
                        a['params']['product'] = j['nextVerify'] == 'SLIDE_VERIFY' ? 'click-bind-suspend' : 'i-dsc';
                    }
                    setTimeout(function() {
                        if (a['params']['product'] == 'i-dsc') {
                            a['dscResult']['style']['display'] = 'none';
                            a['getValidateImage']();
                            a['bindDscEvent']();
                            a['resetSize']();
                        } else {
                            a['initHtml']();
                            a['warp']['style']['display'] = 'block';
                            a['resetSize']();
                        }
                    }, 0x1f4);
                } else {
                    a['dscResult']['setAttribute']('class', 'JDJRV-dsc-result\x20JDJRV-dsc-result-succ');
                    a['dscResult']['setAttribute']('className', 'JDJRV-dsc-result\x20JDJRV-dsc-result-succ');
                    a['refreshBtn']['style']['display'] = 'none';
                    if (a['params']['product'] == 'i-dsc') {
                        setTimeout(function() {
                            a['warp']['style']['display'] = 'none';
                        }, 0x320);
                    }
                }
            } else if (a['params']['product'] == 'pic-click' || a['params']['product'] == 'i-pic-click' || a['params']['product'] == 'e-pic-popup') {
                a['picClickResult']['style']['display'] = 'block';
                if (j['success'] == 0x0) {
                    a['picClickResult']['setAttribute']('class', 'JDJRV-pic-click-result\x20JDJRV-pic-click-result-err');
                    a['picClickResult']['setAttribute']('className', 'JDJRV-pic-click-result\x20JDJRV-pic-click-result-err');
                    a['picClickResult']['innerHTML'] = '验证失败，请重试';
                    setTimeout(function() {
                        a['picClickResult']['style']['bottom'] = '0px';
                    }, 0xa);
                    a['mousePos'] = new Array();
                    for (var p = 0x0; p < a['operSeqs']['length']; p++) {
                        a['operSeqs'][p]['style']['display'] = 'none';
                    }
                    if (a['params']['product'] == 'i-pic-click') {
                        a['params']['product'] = j['nextVerify'] == 'SLIDE_VERIFY' ? 'click-bind-suspend' : 'i-pic-click';
                    }
                    setTimeout(function() {
                        if (a['params']['product'] == 'i-pic-click' || a['params']['product'] == 'e-pic-popup') {
                            a['picClickResult']['style']['display'] = 'none';
                            a['getValidateImage']();
                            a['bindPicClickEvent']();
                            a['resetSize']();
                        } else {
                            a['initHtml']();
                            a['warp']['style']['display'] = 'block';
                            a['resetSize']();
                        }
                    }, 0x3e8);
                } else {
                    a['picClickResult']['setAttribute']('class', 'JDJRV-pic-click-result\x20JDJRV-pic-click-result-succ');
                    a['picClickResult']['setAttribute']('className', 'JDJRV-pic-click-result\x20JDJRV-pic-click-result-succ');
                    a['picClickResult']['innerHTML'] = '验证成功';
                    a['picClickResult']['style']['bottom'] = '0px';
                    a['refreshBtn']['style']['display'] = 'none';
                    for (var p = 0x0; p < a['operSeqs']['length']; p++) {
                        a['operSeqs'][p]['onmousedown'] = null;
                    }
                    if (a['params']['product'] == 'i-pic-click' || a['params']['product'] == 'e-pic-popup') {
                        setTimeout(function() {
                            a['warp']['style']['display'] = 'none';
                        }, 0x320);
                    }
                }
            } else {
                if (j['success'] == 0x0) {
                    a['slideWrap']['setAttribute']('class', 'JDJRV-slide\x20JDJRV-slide-err');
                    a['slideWrap']['setAttribute']('className', 'JDJRV-slide\x20JDJRV-slide-err');
                    if (a['params']['product'] == 'click-bind-suspend' && j['nextVerify'] == 'DSC_VERIFY') {
                        a['params']['product'] = j['nextVerify'] == 'DSC_VERIFY' ? 'i-dsc' : 'click-bind-suspend';
                        setTimeout(function() {
                            a['initHtml']();
                            a['warp']['style']['display'] = 'block';
                        }, 0x1f4);
                    } else {
                        setTimeout(function() {
                            a['getValidateImage']();
                        }, 0x1f4);
                        a['resetValidate']();
                    }
                } else {
                    a['passValidate'] = !![];
                    a['slideWrap']['setAttribute']('class', 'JDJRV-slide\x20JDJRV-slide-succ');
                    a['slideWrap']['setAttribute']('className', 'JDJRV-slide\x20JDJRV-slide-succ');
                    a['slideGreenBar']['style']['width'] = '100%';
                    a['slideGreenBarCenter']['innerHTML'] = a['params']['successMess'] ? a['params']['successMess'] : a['i18nParams']['default-slide-success'];
                    a['refreshBtn']['style']['display'] = 'none';
                    if (a['params']['product'] == 'float') {
                        a['slideTimer'] = setTimeout(function() {
                            a['slideImgWrap']['setAttribute']('class', 'JDJRV-img-panel\x20JDJRV-float');
                            a['slideImgWrap']['setAttribute']('className', 'JDJRV-img-panel\x20JDJRV-float');
                        }, 0x12c);
                    }
                    if (a['params']['product'] == 'bind' || a['params']['product'] == 'popup' || a['params']['product'] == 'click-popup' || a['params']['product'] == 'click-bind-suspend') {
                        setTimeout(function() {
                            a['warp']['style']['display'] = 'none';
                        }, 0x320);
                    }
                    if (a['params']['product'] == 'popup' || a['params']['product'] == 'click-popup' || a['params']['product'] == 'click-suspend') {
                        a['clickSuccess']();
                    }
                }
            }
            a['submitCallback'](j);
        }, function() {
            if (a['params']['product'] == 'click' || a['params']['product'] == 'click-bind') {
                a['params']['product'] = 'click-popup';
                a['initHtml']();
                a['warp']['style']['display'] = 'block';
                setTimeout(function() {
                    a['resetSize']();
                }, 0x32);
            } else if (a['params']['product'] == 'dsc') {
                a['dscResult']['setAttribute']('class', 'JDJRV-dsc-result\x20JDJRV-dsc-result-err');
                a['dscResult']['setAttribute']('className', 'JDJRV-dsc-result\x20JDJRV-dsc-result-err');
                setTimeout(function() {
                    a['initHtml']();
                }, 0x1f4);
            } else if (a['params']['product'] == 'pic-click' || a['params']['product'] == 'i-pic-click' || a['params']['product'] == 'e-pic-popup') {
                a['picClickResult']['setAttribute']('class', 'JDJRV-pic-click-result\x20JDJRV-pic-click-result-err');
                a['picClickResult']['setAttribute']('className', 'JDJRV-pic-click-result\x20JDJRV-pic-click-result-err');
                a['picClickResult']['innerHTML'] = '验证失败，请重试';
                setTimeout(function() {
                    a['picClickResult']['style']['bottom'] = '0px';
                }, 0xa);
                a['mousePos'] = new Array();
                for (var j = 0x0; j < a['operSeqs']['length']; j++) {
                    a['operSeqs'][j]['style']['display'] = 'none';
                }
                if (a['params']['product'] == 'i-pic-click') {
                    a['params']['product'] = data['nextVerify'] == 'SLIDE_VERIFY' ? 'click-bind-suspend' : 'i-pic-click';
                }
                setTimeout(function() {
                    if (a['params']['product'] == 'i-pic-click' || a['params']['product'] == 'e-pic-popup') {
                        a['picClickResult']['style']['display'] = 'none';
                        a['getValidateImage']();
                        a['bindPicClickEvent']();
                        a['resetSize']();
                    } else {
                        a['initHtml']();
                        a['warp']['style']['display'] = 'block';
                        a['resetSize']();
                    }
                }, 0x3e8);
            } else {
                a['slideWrap']['setAttribute']('class', 'JDJRV-slide\x20JDJRV-slide-err');
                a['slideWrap']['setAttribute']('className', 'JDJRV-slide\x20JDJRV-slide-err');
                setTimeout(function() {
                    a['getValidateImage']();
                }, 0x1f4);
                a['resetValidate']();
            }
        });
    },
    'submitCallback': function(a) {
        var b = this;
        var c = {};
        c['getSuccess'] = function() {
            return a['success'];
        }
        ;
        c['getMessage'] = function() {
            return a['message'];
        }
        ;
        c['getValidate'] = function() {
            return '';
        }
        ;
        if (a['success'] == 0x0) {
            if (b['params']['failCallback']) {
                b['callback'](c);
            }
        } else {
            c['getValidate'] = function() {
                return a['validate'];
            }
            ;
            b['callback'](c);
        }
    },
    'clickSuccess': function() {
        var a = this;
        if (a['clickContent']) {
            if (a['params']['product'] == 'suspend') {
                a['clickContent']['setAttribute']('class', 'JDJRV-suspend-click\x20JDJRV-suspend-click-success');
                a['clickContent']['setAttribute']('className', 'JDJRV-suspend-click\x20JDJRV-suspend-click-success');
                a['clickText']['innerHTML'] = a['params']['successMess'] ? a['params']['successMess'] : a['i18nParams']['default-suspend-success'];
            } else if (a['params']['product'] == 'click-suspend') {
                a['clickContent']['setAttribute']('class', 'JDJRV-suspend-click\x20JDJRV-suspend-click-success');
                a['clickContent']['setAttribute']('className', 'JDJRV-suspend-click\x20JDJRV-suspend-click-success');
                a['clickText']['innerHTML'] = a['params']['successMess'] ? a['params']['successMess'] : a['i18nParams']['default-suspend-success'];
                a['suspendSlideWarp']['style']['display'] = 'none';
            } else {
                a['clickContent']['setAttribute']('class', 'JDJRV-click-warp\x20JDJRV-click-success');
                a['clickContent']['setAttribute']('className', 'JDJRV-click-warp\x20JDJRV-click-success');
                a['clickImg']['src'] = this['protocol'] + (a['lang'] && a['lang'] != 'zh_CN' ? '//static.joybuy.com/risk-cdn/iv/images/slide-succ.png' : '//ivs.jd.com/slide/i/slide-succ.png');
                a['clickText']['innerHTML'] = a['params']['successMess'] ? a['params']['successMess'] : a['i18nParams']['default-suspend-success'];
            }
        }
        a['clickResult'] = !![];
    },
    'getImgSrc': function(a, b) {
        return (b['lastIndexOf']('.png') > 0x0 || b['lastIndexOf']('.jpg') > 0x0 || b['lastIndexOf']('.webp') > 0x0 ? this['protocol'] + a : 'data:image/png;base64,') + b;
    },
    'jsonp': function(a, b, c, d, e) {
        var f = 'jsonp_' + Math['random']();
        f = f['replace']('.', '');
        window[f] = function(n) {
            clearTimeout(g);
            window[f] = null;
            m['removeChild'](l);
            d(n);
        }
        ;
        var g = setTimeout(function() {
            window[f] = null;
            m['removeChild'](l);
            e && e();
        }, 0x1388);
        b[c] = f;
        var h = [];
        for (var j in b) {
            h['push'](j + '=' + b[j]);
        }
        var k = a + '?' + h['join']('&');
        var l = document['createElement']('script');
        l['src'] = k;
        l['type'] = 'text/javascript';
        l['setAttribute']('ignore', 'true');
        var m = document['getElementsByTagName']('head')[0x0];
        m['appendChild'](l);
    },
    'ajax': function(a) {
        a = a || {};
        a['type'] = (a['type'] || 'GET')['toUpperCase']();
        a['dataType'] = a['dataType'] || 'json';
        var b = this['formatParams'](a['data']);
        if (window['XMLHttpRequest']) {
            var d = new XMLHttpRequest();
        } else {
            var d = new ActiveXObject('Microsoft.XMLHTTP');
        }
        d['onreadystatechange'] = function() {
            if (d['readyState'] == 0x4) {
                var e = d['status'];
                if (e >= 0xc8 && e < 0x12c) {
                    a['success'] && a['success'](d['responseText'], d['responseXML']);
                } else {
                    a['fail'] && a['fail'](e);
                }
            }
        }
        ;
        if (a['type'] == 'GET') {
            d['open']('GET', a['url'] + '?' + b, !![]);
            d['send'](null);
        } else if (a['type'] == 'POST') {
            d['open']('POST', a['url'], !![]);
            d['setRequestHeader']('Content-Type', 'application/x-www-form-urlencoded');
            d['send'](b);
        }
    },
    'formatParams': function(a) {
        var b = [];
        for (var c in a) {
            b['push'](encodeURIComponent(c) + '=' + encodeURIComponent(a[c]));
        }
        b['push'](('v=' + Math['random']())['replace']('.', ''));
        return b['join']('&');
    },
    'string10to64': function(a) {
        var b = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-~'['split']('')
          , c = b['length']
          , d = +a
          , e = [];
        do {
            mod = d % c;
            d = (d - mod) / c;
            e['unshift'](b[mod]);
        } while (d);
        return e['join']('');
    },
    'prefixInteger': function(a, b) {
        return (Array(b)['join'](0x0) + a)['slice'](-b);
    },
    'pretreatment': function(a, b, c) {
        var d = this;
        var e = d['string10to64'](Math['abs'](a));
        var f = '';
        if (!c) {
            f += a > 0x0 ? '1' : '0';
        }
        f += d['prefixInteger'](e, b);
        return f;
    },
    'getCoordinate': function(a) {
        var b = this;
        var c = new Array();
        for (var d = 0x0; d < a['length']; d++) {
            if (d == 0x0) {
                c['push'](b['pretreatment'](a[d][0x0] < 0x3ffff ? a[d][0x0] : 0x3ffff, 0x3, !![]));
                c['push'](b['pretreatment'](a[d][0x1] < 0xffffff ? a[d][0x1] : 0xffffff, 0x4, !![]));
                c['push'](b['pretreatment'](a[d][0x2] < 0x3ffffffffff ? a[d][0x2] : 0x3ffffffffff, 0x7, !![]));
            } else {
                var e = a[d][0x0] - a[d - 0x1][0x0];
                var f = a[d][0x1] - a[d - 0x1][0x1];
                var g = a[d][0x2] - a[d - 0x1][0x2];
                c['push'](b['pretreatment'](e < 0xfff ? e : 0xfff, 0x2, ![]));
                c['push'](b['pretreatment'](f < 0xfff ? f : 0xfff, 0x2, ![]));
                c['push'](b['pretreatment'](g < 0xffffff ? g : 0xffffff, 0x4, !![]));
            }
        }
        return c['join']('');
    },
    'getEid': function() {
        var a = '';
        try {
            a = getJdEid()['eid'];
        } catch (b) {}
        try {
            if (a == '') {
                if (typeof eval('getJdEid;') == 'function') {
                    getJdEid(function(c, d, f) {
                        a = c;
                    });
                }
            }
        } catch (c) {}
        return a;
    },
    'getJsTk': function() {
        var a = '';
        try {
            if (typeof eval('getJsToken;') == 'function') {
                getJsToken(function(b) {
                    a = b['jsToken'];
                }, 0xbb8);
            }
        } catch (b) {}
        return a;
    },
    'getSessionId': function() {
        var a = '';
        try {
            if ('undefined' != typeof _jdtdmap_sessionId)
                a = _jdtdmap_sessionId;
        } catch (b) {
            console['error']('sessionId\x20err;');
        }
        return a;
    },
    'getSelenium': function() {
        var a = '0';
        try {
            if (window['navigator']['webdriver'])
                a = '1';
        } catch (b) {}
        return a;
    },
    'getUrl': function() {
        var a = 'NULL';
        try {
            a = encodeURIComponent(window['location']['href']);
        } catch (b) {
            a = 'ERROR';
        }
        return a;
    },
    'getLeft': function(a) {
        var b = a;
        var c = 0x0;
        var d = 0x0;
        if (document['getElementById'] || document['all']) {
            do {
                d += a['offsetLeft'] - a['scrollLeft'];
                c += a['offsetTop'] - a['scrollTop'];
                a = a['offsetParent'];
                b = b['parentNode'];
                while (b != a) {
                    d -= b['scrollLeft'];
                    c -= b['scrollTop'];
                    b = b['parentNode'];
                }
            } while (a['offsetParent']);
        } else if (document['layers']) {
            c += a['y'];
            d += a['x'];
        }
        if (document['compatMode'] == 'BackCompat') {
            var g = document['body']['scrollLeft'];
        } else {
            var g = document['documentElement']['scrollLeft'];
        }
        return d - g;
    },
    'getTop': function(a) {
        var b = a;
        var c = 0x0;
        var d = 0x0;
        if (document['getElementById'] || document['all']) {
            do {
                d += a['offsetLeft'] - a['scrollLeft'];
                c += a['offsetTop'] - a['scrollTop'];
                a = a['offsetParent'];
                b = b['parentNode'];
                while (b != a) {
                    d -= b['scrollLeft'];
                    c -= b['scrollTop'];
                    b = b['parentNode'];
                }
            } while (a['offsetParent']);
        } else if (document['layers']) {
            c += a['y'];
            d += a['x'];
        }
        if (document['compatMode'] == 'BackCompat') {
            var g = document['body']['scrollTop'];
        } else {
            var g = document['documentElement']['scrollTop'];
        }
        return c - g;
    }
};

// JDJRValidate['prototype'].getCoordinate([["672", "377", 1690277910969], ["705", "395", 1690277910969], ["707", "395", 1690277911078], ["708", "395", 1690277911086], ["711", "395", 1690277911094], ["713", "395", 1690277911102], ["715", "395", 1690277911110], ["716", "395", 1690277911118], ["718", "395", 1690277911126], ["719", "395", 1690277911134], ["719", "395", 1690277911398]])
