$( function () {
  var length=$(".main_lb li").length;
  var index=0;
  var timer=800;
  var intervaltimer=0;
  var isMoving=false;
  /*轮播方法*/
  function slide(slideMode){
    if(isMoving==false){
      isMoving=true;
      var prev,next,hidden;
      var curr=$("#imgCard"+index);

      if (index==0){
        prev=$("#imgCard"+(length-1));
      }else{
        prev=$("#imgCard"+(index-1));
      }

      if (index==(length-1)){
        next=$("#imgCard0");
      }else{
        next=$("#imgCard"+(index+1));
      }

      if (slideMode){
        if (index-2>=0){
          hidden=$("#imgCard"+(index-2));
        }else{
          hidden=$("#imgCard"+(length+index-2));
        }

        prev.css("z-index","5");
        next.css("z-index","1");
        curr.css("z-index","2");
        hidden.css("z-index","1");
        /* 当index自减时，图片往右动 */
        hidden.css({width:"450px",height:"180px",top:"60px",left:"0px","opacity":0});
        hidden.stop(true,true).animate({width:"580px",height:"240px",top:"20px",left:"0px",opacity:1},timer);
        curr.stop(true,true).animate({width:"580px",height:"240px",top:"20px",left:"600px",opacity:1},timer);
        next.stop(true,true).animate({width:"450px",height:"180px",top:"60px","left":"730px","opacity":0},timer,
              function(){
                next.find("span").css("opacity",0); isMoving = false;
              });
        prev.find("span").css("opacity",0);
        $(".main_lb_box li").find("p").css({"bottom":"-50px"});//视频图片介绍标题隐藏
        prev.stop(true,true).animate({width:"670px",height:"280px",left:"255px",top:0,opacity:1},timer,
            function(){
              $(this).find("p").animate({"bottom":"0px"});	//当前视频图片介绍的标题运动出来
            });
        index--;
      }else{
        if (index+2>=length){
          hidden=$("#imgCard"+(index+2-length));
        }else{
          hidden=$("#imgCard"+(index+2));
        }
        prev.css("z-index","1");
        next.css("z-index","5");
        curr.css("z-index","2");
        hidden.css("z-index","1");
        /* 当index自增时，图片往左动 */
        hidden.css({width:"450px",height:"180px",top:"60px",left:"730px","opacity":0});
        hidden.stop(true,true).animate({width:"580px",height:"240px",top:"20px",left:"600px",opacity:1},timer);
        curr.stop(true,true).animate({width:"580px",height:"240px",top:"20px",left:"0px",opacity:1},timer);
        next.find("span").css("opacity",0);
        $(".main_banner_box li").find("p").css({"bottom":"-50px"});//视频图片介绍标题隐藏
        next.stop(true,true).animate({width:"670px",height:"280px",top:"60px","left":"255px",top:0,opacity:1},timer,
              function(){
                $(this).find("p").animate({"bottom":"0px"});	//当前视频图片介绍的标题运动出来
              });
        prev.stop(true,true).animate({width:"450px",height:"180px",left:"0px",top:"60px",opacity:0},timer,
            function(){
              isMoving = false;
            });
        index++;
      }
      hidden.find("span").css("opacity",0.5);
      curr.find("span").css("opacity",0.5);

      if (index==length){
        index=0;
      }
      if (index<0){
        index+=length;
      }
      $(".btn_list span").removeClass('curr').eq(index).addClass('curr');//给序列号按钮添加、移除样式
    }
  }

  
  if(length>3){
		//序列号按钮 跳序切换 方法
		$(".btn_list span").click(function(event){

			if (isMoving ) return;
			var oIndex=$(this).index();

			if(oIndex==index) return;//点击按钮的序列号与当前图片的序列号一致，return
			clearInterval(intervaltimer)
			intervaltimer=null;

			var flag=false;
			//当前显示图片的序列号  和  被点击按钮的序列号  间隔超过1且不是首尾两个的时候
			if(Math.abs(index-oIndex)>1&&Math.abs(length-Math.abs(index-oIndex))!=1){
				//统一样式
				$(".main_lb_box li").css({width:"300px",height:"120px",left:"600px",top:"60px",opacity:0});
				//如果当前的序列号   比    被点击按钮序列号     大     而且     不相邻、不是首尾
				if(index>oIndex&&length-Math.abs(index-oIndex)!=1){
					flag=true;
					index=oIndex+1;		//oIndex+1    通过slide()  运动回上一张    oIndex
				}else{//比   小     而且     不相邻、不是首尾
					index=oIndex-1;		//oIndex-1     通过slide()  运动到下一张    oIndex
					if(index<0) index=length-1;
				}
			}else{//当前 比 被点击  大	且   相邻									//从0    跳到     4		要执行上一张方法
				if((index>oIndex&&length-(index-oIndex)!=1)||(index<oIndex&&length+(index-oIndex)==1)){
					flag=true;			//执行上一张
				}
			}
			slide(flag);
			intervaltimer=setInterval(slide,3000);//自动轮播

		});

        $(".js_pre").click(function(event){//上一张
			if (isMoving ) return;
			clearInterval(intervaltimer);
			intervaltimer=null;
			slide(1);
			intervaltimer=setInterval(slide,3000);
		});

		$(".js_next").click(function(event){//下一张
			if (isMoving ) return;
			clearInterval(intervaltimer);
			intervaltimer=null;
			slide();
			intervaltimer=setInterval(slide,3000);
		});

		intervaltimer=setInterval(slide,3000);

	}else{

		$(".js_pre").hide();
		$(".js_next").hide();

	}//if else

});