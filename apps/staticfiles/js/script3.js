var canvas = document.getElementById("paint");
var ctx = canvas.getContext("2d");
var width = canvas.width, height = canvas.height;
var curX, curY, prevX, prevY;
var hold = false;
var stroke_value = false;
var canvas_data = { "pencil": [], "line": [], "rectangle": [], "circle": []};


var canvas_annotation = document.getElementById("annotation");
var ctx_annotation = canvas_annotation.getContext("2d");



var img = document.getElementById("image"); 
var w = img.width;     
var h = img.height; 

var wid=  document.getElementById('canvas_paint').getBoundingClientRect();  
var offsetvaleft = wid.left; 
var offsetvartop = wid.top;


function color (color_value){
    ctx.strokeStyle = color_value;    
    ctx_annotation.strokeStyle = color_value;
}    

        
// pencil tool
function reset (){
    window.location.reload()
}


function pencil (){        
    canvas.onmousedown = function (e){
        curX = e.clientX - canvas.offsetLeft-offsetvaleft;
        curY = e.clientY - canvas.offsetTop-offsetvartop;
        hold = true;
            
        prevX = curX;
        prevY = curY;
        ctx.beginPath();
        ctx.moveTo(prevX, prevY);

        
        ctx_annotation.beginPath();
        ctx_annotation.moveTo(prevX, prevY);
    };
        
    canvas.onmousemove = function (e){
        if(hold){
            curX = e.clientX - canvas.offsetLeft-offsetvaleft;
            curY = e.clientY - canvas.offsetTop-offsetvartop;
            draw();
        }
    };
        
    canvas.onmouseup = function (e){
        hold = false;        
    };
        
    canvas.onmouseout = function (e){
        hold = false;
    };
        
    function draw (){
        ctx.lineTo(curX, curY);
        ctx.stroke();

        
        ctx_annotation.lineTo(curX, curY);
        ctx_annotation.stroke();

        canvas_data.pencil.push({ "startx": prevX, "starty": prevY, "endx": curX, "endy": curY, 
            "thick": ctx.lineWidth, "color": ctx.strokeStyle });
        

    }
}
        
// line tool
        
function line (){
           
    canvas.onmousedown = function (e){
        img = ctx.getImageData(0, 0, width, height);
        img_ann = ctx_annotation.getImageData(0, 0, width, height);
        prevX = e.clientX - canvas.offsetLeft-offsetvaleft;
        prevY = e.clientY - canvas.offsetTop-offsetvartop;
        hold = true;
    };
            
    canvas.onmousemove = function (e){
        if (hold){
            ctx.putImageData(img, 0, 0);
            curX = e.clientX - canvas.offsetLeft-offsetvaleft;
            curY = e.clientY - canvas.offsetTop-offsetvartop;
            ctx.beginPath();
            ctx.moveTo(prevX, prevY);
            ctx.lineTo(curX, curY);
            ctx.stroke();
            canvas_data.line.push({ "starx": prevX, "starty": prevY, "endx": curX, "endY": curY,
                 "thick": ctx.lineWidth, "color": ctx.strokeStyle });
            ctx.closePath();

            ctx_annotation.putImageData(img_ann, 0, 0);
            ctx_annotation.beginPath();
            ctx_annotation.moveTo(prevX, prevY);
            ctx_annotation.lineTo(curX, curY);
            ctx_annotation.stroke();
            ctx_annotation.closePath();
        }
    };
            
    canvas.onmouseup = function (e){
         hold = false;
    };
            
    canvas.onmouseout = function (e){
         hold = false;
    };
}
        
// rectangle tool
        
function rectangle (){
            
    canvas.onmousedown = function (e){
        img = ctx.getImageData(0, 0, width, height);        
        img_ann = ctx_annotation.getImageData(0, 0, width, height);
        prevX = e.clientX - canvas.offsetLeft-offsetvaleft;
        prevY = e.clientY - canvas.offsetTop-offsetvartop;
        hold = true;
    };
            
    canvas.onmousemove = function (e){
        if (hold){
            ctx.putImageData(img, 0, 0);
            curX = e.clientX - canvas.offsetLeft-offsetvaleft - prevX;
            curY = e.clientY - canvas.offsetTop-offsetvartop - prevY;
            ctx.strokeRect(prevX, prevY, curX, curY);
            canvas_data.rectangle.push({ "starx": prevX, "stary": prevY, "width": curX, "height": curY, 
                "thick": ctx.lineWidth, "stroke": stroke_value, "stroke_color": ctx.strokeStyle });

            ctx_annotation.putImageData(img_ann, 0, 0);
            ctx_annotation.strokeRect(prevX, prevY, curX, curY);
            
        }
    };
            
    canvas.onmouseup = function (e){
        hold = false;
    };
            
    canvas.onmouseout = function (e){
        hold = false;
    };
}
        
// circle tool
        
function circle (){
            
    canvas.onmousedown = function (e){
        img = ctx.getImageData(0, 0, width, height);        
        img_ann = ctx_annotation.getImageData(0, 0, width, height);
        prevX = e.clientX - canvas.offsetLeft-offsetvaleft;
        prevY = e.clientY - canvas.offsetTop-offsetvartop;
        hold = true;
    };
            
    canvas.onmousemove = function (e){
        if (hold){
            ctx.putImageData(img, 0, 0);
            curX = e.clientX - canvas.offsetLeft-offsetvaleft;
            curY = e.clientY - canvas.offsetTop-offsetvartop;
            ctx.beginPath();
            ctx.arc(Math.abs(curX + prevX)/2, Math.abs(curY + prevY)/2, 
                Math.sqrt(Math.pow(curX - prevX, 2) + Math.pow(curY - prevY, 2))/2, 0, Math.PI * 2, true);
            ctx.closePath();
            ctx.stroke();
            
            ctx_annotation.putImageData(img_ann, 0, 0);
            ctx_annotation.beginPath();
            ctx_annotation.arc(Math.abs(curX + prevX)/2, Math.abs(curY + prevY)/2, 
                Math.sqrt(Math.pow(curX - prevX, 2) + Math.pow(curY - prevY, 2))/2, 0, Math.PI * 2, true);
            ctx_annotation.closePath();
            ctx_annotation.stroke();

            canvas_data.circle.push({ "starx": prevX, "stary": prevY, "radius": curX - prevX, "thick": ctx.lineWidth,
                "stroke": stroke_value, "stroke_color": ctx.strokeStyle});
        }
    };
            
    canvas.onmouseup = function (e){
        hold = false;
    };
            
    canvas.onmouseout = function (e){
        hold = false;
    };
}
  
