        var m1 = 80;
        var m2 = 8;
        function getScrollTop(){
            var scrOfY = 0;
            if( typeof( window.pageYOffset ) == "number" ) {
                scrOfY = window.pageYOffset;
            }
            else if( document.body && (document.body.scrollLeft || document.body.scrollTop )){
                scrOfY = document.body.scrollTop;
            } else if(document.documentElement && (document.documentElement.scrollLeft || document.documentElement.scrollTop )){
                scrOfY = document.documentElement.scrollTop;
            }
            return scrOfY;
        }
        function marginMenuTop()
        {
            var top = getScrollTop();
            var s= document.getElementById("socializ");
            if (top+m2 < m1){
                s.style.top = (m1-top) + "px";
            }
            else{
                s.style.top = m2 + "px";
            }
        }
        function setMenuPosition(){
            if(typeof window.addEventListener != "undefined"){
                window.addEventListener("scroll", marginMenuTop, false);
            }
            else if(typeof window.attachEvent != "undefined"){
                window.attachEvent("onscroll", marginMenuTop);
            }
        }
        if(typeof window.addEventListener != "undefined"){
            window.addEventListener("load", setMenuPosition, false);
        } else if(typeof window.attachEvent != "undefined"){
            window. attachEvent("onload", setMenuPosition);
        }