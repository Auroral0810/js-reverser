
# 猿人学14 题
- 大部分都扣下来了[get_m](get_m.js)，浏览器和node结果不一样，可能是因为 函数 E 运行动了 gee 也用到的全局变量（应该是少了什么环境因为用vm2运行也是相同的错误结果，说明不是node被检测），要一点点跟没耐心了，花时间肯定可以搞定但意义不大，直接用调试环境加postman拿到结果算了。
- 4、5页除了要改userAgent 外计算`m`的 `d` 和 `b64_zw`也要改,不过这边的指纹就是一个数组的toString很好伪造。
- window.n 和页数page 没有直接关系
- 环境检测还是有比较多的 比如delete window document 啥的 还用try catch 包裹 
- obfuscator混淆一般般吧，习惯了的话硬刚也可以
- fiddler autoResponse yyds
> 讲的有点乱，就当是自己学习的记录吧。  


# debugger专题汇总:

1.先格式化代码，然后在debugger的行号 上 单击右键，选择 Never pause here，然后F8运行代码；

2.置空 constructor 方法，控制台输入:
```
Function.prototype.constructor=function(){}；
```
回车即可。

3.同样使用代码置空 constructor 方法，控制台输入:
```
var _con = Function.prototype.constructor; 
Function.prototype.constructor = function(val)
{ 
  if(val == "debugger")
  {   
    return 0;
  }
 return _con(val); 
}
```
回车即可。可加入油猴脚本HooK替换。

4，改写 setInterval 方法，假设代码段中包含 eval 函数:
```
setInterval_ = setInterval
setInterval = function(x1, x2) {
   if (x1.toString().indexOf('debugger') == -1) {
       if (typeof (x1) == 'function') {
           return setInterval_(x1())
       }
       return eval(x1)
   }
}
```
使用油猴时，需要注意hook时机，设置在页面加载开始执行。

5.手动把js下载下来，修改逻辑，删除debugger相关的垃圾代码。再用 fildder 或者 ReRes 映射替换。
