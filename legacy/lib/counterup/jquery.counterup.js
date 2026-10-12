/*!
 * jquery.counterup.js 2.1.0
 *
 * Copyright 2013, Benjamin Intal http://gambit.ph @bfintal
 * Released under the GPL v2 License
 *
 * Amended by Jeremy Paris, Ciro Mattia Gonano and others
 *
 * Date: Feb 24, 2017
 */
!function(t){"use strict";t.fn.counterUp=function(e){var a,n=t.extend({time:400,delay:10,offset:100,beginAt:0,formatter:!1,context:"window",callback:function(){}},e);return this.each(function(){var e=t(this),u={time:t(this).data("counterup-time")||n.time,delay:t(this).data("counterup-delay")||n.delay,offset:t(this).data("counterup-offset")||n.offset,beginAt:t(this).data("counterup-beginat")||n.beginAt,context:t(this).data("counterup-context")||n.context},o=function(){var t=[],o=u.time/u.delay,r=e.attr("data-num")?e.attr("data-num"):e.text(),i=/[0-9]+,[0-9]+/.test(r),c=((r=r.replace(/,/g,"")).split(".")[1]||[]).length;u.beginAt>r&&(u.beginAt=r);var s=/[0-9]+:[0-9]+:[0-9]+/.test(r);if(s){var f=r.split(":"),l=1;for(a=0;f.length>0;)a+=l*parseInt(f.pop(),10),l*=60}for(var d=o;d>=u.beginAt/r*o;d--){var p=parseFloat(r/o*d).toFixed(c);if(s){p=parseInt(a/o*d);var h=parseInt(p/3600)%24,m=parseInt(p/60)%60,g=parseInt(p%60,10);p=(h<10?"0"+h:h)+":"+(m<10?"0"+m:m)+":"+(g<10?"0"+g:g)}if(i)for(;/(\d+)(\d{3})/.test(p.toString());)p=p.toString().replace(/(\d+)(\d{3})/,"$1,$2");n.formatter&&(p=n.formatter.call(this,p)),t.unshift(p)}e.data("counterup-nums",t),e.text(u.beginAt);var b=function(){e.data("counterup-nums")?(e.html(e.data("counterup-nums").shift()),e.data("counterup-nums").length?setTimeout(e.data("counterup-func"),u.delay):(e.data("counterup-nums",null),e.data("counterup-func",null),n.callback.call(this))):n.callback.call(this)};e.data("counterup-func",b),setTimeout(e.data("counterup-func"),u.delay)};e.waypoint(function(){o(),this.destroy()},{offset:u.offset+"%",context:u.context})})}}(jQuery);