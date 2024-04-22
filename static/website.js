// window.onscroll = function() {
//     var scrollTop = (window.pageYOffset !== undefined) ? window.pageYOffset : (document.documentElement || document.body.parentNode || document.body).scrollTop;
//     if (scrollTop >= document.getElementById("moving_nav").offsetTop) {
//       document.getElementById("topnav").style.position = "fixed";
//     //   document.getElementById("topnav").style.marginTop = "50px";
//     //   document.getElementById("topnav").style.marginTop = "-50px";
//     } else {
//       document.getElementById("topnav").style.position = "static";
//     //   document.getElementById("topnav").style.marginTop = "0px";
//     //   document.getElementById("topnav").style.marginTop = "0px";
//         // document.getElementById("topnav").style.paddingTop = "-50px";
//         // window.location.href = 'moving_nav';
//     }
//   }

// window.onscroll = function() {
//     var scrollTop = (window.pageYOffset !== undefined) ? window.pageYOffset : (document.documentElement || document.body.parentNode || document.body).scrollTop;
//     if (scrollTop >= document.getElementById("moving_nav").offsetTop) {
//       document.getElementById("topnav").style.position = "fixed";
//       document.getElementById("moving_nav").style.marginTop = "50px";
//     //   document.getElementById("topnav").style.marginTop = "-50px";
//     } else {
//       document.getElementById("topnav").style.position = "static";
//       document.getElementById("moving_nav").style.marginTop = "0px";
//       document.getElementById("topnav").style.marginTop = "0px";
//     }
//   }

window.onscroll = function() {
    var scrollTop = (window.scrollY !== undefined) ? window.scrollY : (document.documentElement || document.body.parentNode || document.body).scrollTop;
    if (scrollTop >= document.getElementById("moving_nav").offsetTop) {
      document.getElementById("topnav").style.position = "fixed";
      document.getElementById("moving_nav").style.marginTop = "50px";
    //   document.getElementById("topnav").style.marginTop = "-50px";
    } else {
      document.getElementById("topnav").style.position = "static";
      document.getElementById("moving_nav").style.marginTop = "0px";
      document.getElementById("topnav").style.marginTop = "0px";
    }
  }