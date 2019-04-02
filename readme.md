[TOC]

## 项目介绍

因为刷题没题库，搜索看瞎了，比较窝火。

正好又找到了个试题库网站漏洞（权限问题）`预计5月和官方反馈=-=` 所以做了个题库，希望能够有所帮助。

### 技术栈

1. python 3
2. selenium 库
3. pymysql 库

### 项目协议 

项目遵循MIT 

你有权利使用、复制、修改、合并、出版发行、散布、再授权及贩售软件及软件的副本。

你可根据程序的需要修改授权条款为适当的内容。

但是你在软件和软件的所有副本中都必须包含版权声明和许可声明。

## 项目使用

### 试题库表格文件下载

试题库的表格文件就在data文件夹下，请自取使用[请使用另存为本链接保存文件](https://github.com/uasier/xszc/blob/master/data/qa.xlsx)

### 试题库不能复制破解教程

1. fq使用谷歌浏览器安装浏览器插件`[tampermonkey](https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo?hl=zh-CN)

2. 使用插件新建脚本(脚本代码如下，脚本有个人修改=-=)

   ```js
   // ==UserScript==
   // @namespace         https://www.github.com/Cat7373/
   
   // @name              网页限制解除
   // @name:en           Remove web limits
   // @name:zh           网页限制解除
   // @name:zh-CN        网页限制解除
   // @name:zh-TW        網頁限制解除
   // @name:ja           ウェブの規制緩和
   
   // @description       通杀大部分网站，可以解除禁止复制、剪切、选择文本、右键菜单的限制。
   // @description:en    Pass to kill most of the site, you can lift the restrictions prohibited to copy, cut, select the text, right-click menu.
   // @description:zh    通杀大部分网站，可以解除禁止复制、剪切、选择文本、右键菜单的限制。
   // @description:zh-CN 通杀大部分网站，可以解除禁止复制、剪切、选择文本、右键菜单的限制。
   // @description:zh-TW 通殺大部分網站，可以解除禁止復制、剪切、選擇文本、右鍵菜單的限制。
   // @description:ja    サイトのほとんどを殺すために渡し、あなたは、コピー切り取り、テキスト、右クリックメニューを選択することは禁止の制限を解除することができます。
   
   // @homepageURL       https://cat7373.github.io/remove-web-limits/
   // @supportURL        https://github.com/Cat7373/remove-web-limits/issues/
   
   // @author            Cat73
   // @version           1.3
   // @license           LGPLv3
   
   // @compatible        chrome Chrome_46.0.2490.86 + TamperMonkey + 脚本_1.3 测试通过
   // @compatible        firefox Firefox_42.0 + GreaseMonkey + 脚本_1.2.1 测试通过
   // @compatible        opera Opera_33.0.1990.115 + TamperMonkey + 脚本_1.1.3 测试通过
   // @compatible        safari 未测试
   
   // @match             *://*/*
   // @grant             none
   // @run-at            document-start
   // ==/UserScript==
   (function() {
     'use strict';
   
     // 域名规则列表
     var rules = {
       black_rule: {
         name: "black",
         hook_eventNames: "",
         unhook_eventNames: ""
       },
       default_rule: {
         name: "default",
         hook_eventNames: "contextmenu|select|selectstart|copy|cut|dragstart",
         unhook_eventNames: "mousedown|mouseup|keydown|keyup|copy",
         dom0: true,
         hook_addEventListener: true,
         hook_preventDefault: true,
         hook_set_returnValue: true,
         add_css: true
       }
     };
     // 域名列表
     var lists = {
       // 黑名单
       black_list: [
         /.*\.youtube\.com.*/,
         /.*\.wikipedia\.org.*/,
         /mail\.qq\.com.*/,
         /translate\.google\..*/
       ]
     };
   
     // 要处理的 event 列表
     var hook_eventNames, unhook_eventNames, eventNames;
     // 储存名称
     var storageName = getRandStr('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM', parseInt(Math.random() * 12 + 8));
     // 储存被 Hook 的函数
     var EventTarget_addEventListener = EventTarget.prototype.addEventListener;
     var document_addEventListener = document.addEventListener;
     var Event_preventDefault = Event.prototype.preventDefault;
   
     // Hook addEventListener proc
     function addEventListener(type, func, useCapture) {
       var _addEventListener = this === document ? document_addEventListener : EventTarget_addEventListener;
       if(hook_eventNames.indexOf(type) >= 0) {
         _addEventListener.apply(this, [type, returnTrue, useCapture]);
       } else if(unhook_eventNames.indexOf(type) >= 0) {
         var funcsName = storageName + type + (useCapture ? 't' : 'f');
   
         if(this[funcsName] === undefined) {
           this[funcsName] = [];
           _addEventListener.apply(this, [type, useCapture ? unhook_t : unhook_f, useCapture]);
         }
   
         this[funcsName].push(func);
       } else {
         _addEventListener.apply(this, arguments);
       }
     }
   
     // 清理循环
     function clearLoop() {
       var elements = getElements();
   
       for(var i in elements) {
         for(var j in eventNames) {
           var name = 'on' + eventNames[j];
           if(elements[i][name] !== null && elements[i][name] !== onxxx) {
             if(unhook_eventNames.indexOf(eventNames[j]) >= 0) {
               elements[i][storageName + name] = elements[i][name];
               elements[i][name] = onxxx;
             } else {
               elements[i][name] = null;
             }
           }
         }
       }
     }
   
     // 返回true的函数
     function returnTrue(e) {
       return true;
     }
     function unhook_t(e) {
       return unhook(e, this, storageName + e.type + 't');
     }
     function unhook_f(e) {
       return unhook(e, this, storageName + e.type + 'f');
     }
     function unhook(e, self, funcsName) {
       var list = self[funcsName];
       for(var i in list) {
         list[i](e);
       }
   
       e.returnValue = true;
       return true;
     }
     function onxxx(e) {
       var name = storageName + 'on' + e.type;
       this[name](e);
   
       e.returnValue = true;
       return true;
     }
   
     // 获取随机字符串
     function getRandStr(chs, len) {
       var str = '';
   
       while(len--) {
         str += chs[parseInt(Math.random() * chs.length)];
       }
   
       return str;
     }
   
     // 获取所有元素 包括document
     function getElements() {
       var elements = Array.prototype.slice.call(document.getElementsByTagName('*'));
       elements.push(document);
   
       return elements;
     }
   
     // 添加css
     function addStyle(css) {
       var style = document.createElement('style');
       style.innerHTML = css;
       document.head.appendChild(style);
     }
   
     // 获取目标域名应该使用的规则
     function getRule(url) {
       function testUrl(list, url) {
         for(var i in list) {
           if(list[i].test(url)) {
             return true;
           }
         }
   
         return false;
       }
   
       if(testUrl(lists.black_list, url)) {
         return rules.black_rule;
       }
   
       return rules.default_rule;
     }
   
     // 初始化
     function init() {
       // 获取当前域名的规则
       var url = window.location.host + window.location.pathname;
       var rule = getRule(url);
   
       // 设置 event 列表
       hook_eventNames = rule.hook_eventNames.split("|");
       // TODO Allowed to return value
       unhook_eventNames = rule.unhook_eventNames.split("|");
       eventNames = hook_eventNames.concat(unhook_eventNames);
   
       // 调用清理 DOM0 event 方法的循环
       if(rule.dom0) {
         setInterval(clearLoop, 30 * 1000);
         setTimeout(clearLoop, 2500);
         window.addEventListener('load', clearLoop, true);
         clearLoop();
       }
   
       // hook addEventListener
       if(rule.hook_addEventListener) {
         EventTarget.prototype.addEventListener = addEventListener;
         document.addEventListener = addEventListener;
       }
   
       // hook preventDefault
       if(rule.hook_preventDefault) {
         Event.prototype.preventDefault = function() {
           if(eventNames.indexOf(this.type) < 0) {
             Event_preventDefault.apply(this, arguments);
           }
         };
       }
   
       // Hook set returnValue
       if(rule.hook_set_returnValue) {
         Event.prototype.__defineSetter__('returnValue', function() {
           if(this.returnValue !== true && eventNames.indexOf(this.type) >= 0) {
             this.returnValue = true;
           }
         });
       }
   
       console.debug('url: ' + url, 'storageName：' + storageName, 'rule: ' + rule.name);
   
       // 添加CSS
       if(rule.add_css) {
         addStyle('html, * {-webkit-user-select:text!important; -moz-user-select:text!important;}');
       }
     }
   
     init();
   })();
   ```

   

3. 启动脚本

4. 访问自测界面，刷题时可以用CtrlCV了

