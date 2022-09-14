
var canvas = document.getElementById("paint");
var ctx = canvas.getContext("2d");
var width = canvas.width, height = canvas.height;
var curX, curY, prevX, prevY, iniX, iniY;
var hold = false;

var img

var pencil_data_x = [];
var pencil_data_y = [];
var rectangle_data =[];

var wid_c=  document.getElementById('canvas_paint').getBoundingClientRect();  
var wid_n=  document.getElementById('navigation_bar').getBoundingClientRect();  

if   (wid_n>0){
    var offsetvaleft = wid_c.left+wid_n.right; 
}else{
    var offsetvaleft = wid_c.left; 
};        
var offsetvartop = wid_c.top; 


function color (color_value){
    ctx.strokeStyle = color_value;    
}    

        
// pencil tool
function reset (){
    window.location.reload()
}


function pencil (){    
        
    canvas.onmousedown = function (e){
        wid_c=  document.getElementById('canvas_paint').getBoundingClientRect();  
        wid_n=  document.getElementById('navigation_bar').getBoundingClientRect();  

        if   (wid_n>0){
            offsetvaleft = wid_c.left+wid_n.right; 
        }else{
            offsetvaleft = wid_c.left; 
        };  
    

        var canvas = document.getElementById("paint");
        var ctx = canvas.getContext("2d");       
        var width = canvas.width, height = canvas.height;
        img = ctx.getImageData(0, 0, width, height);        
        
        curX = e.clientX - canvas.offsetLeft-offsetvaleft;
        curY = e.clientY - canvas.offsetTop-offsetvartop;
        hold = true;
            
        prevX = curX;
        prevY = curY;

        pencil_x=[width];
        pencil_y=[height];
    };
        
    canvas.onmousemove = function (e){
        if (hold){
            ctx.putImageData(img, 0, 0);

            curX = e.clientX - canvas.offsetLeft - offsetvaleft;
            curY = e.clientY - canvas.offsetTop-offsetvartop;

            pencil_x.push(curX);
            pencil_y.push(curY);

          
            ctx.beginPath();
            ctx.moveTo(pencil_x[1], pencil_y[1]);  

            for (var j = 1; j < pencil_x.length; j++) {
                ctx.lineTo(pencil_x[j], pencil_y[j]);
                ctx.stroke(); 
            };
            ctx.lineTo(pencil_x[1], pencil_y[1]);
            ctx.stroke(); 
          
        };    
        
    };
        
    canvas.onmouseup = function (e){
        hold = false;    
        pencil_x.push(pencil_x[1])
        pencil_y.push(pencil_y[1])  
        
        pencil_data_x.push(pencil_x)
        pencil_data_y.push(pencil_y)  
        
        
    };
        
    canvas.onmouseout = function (e){
        hold = false;
    };
        
    function draw (){
        ctx.lineTo(curX, curY);
        ctx.stroke();

        pencil_x.push(curX);
        pencil_y.push(curY);

        
        for (var pencil_x = 1; j < pencil_x.length; j++) {
            ctx.lineTo(pencil_x[j], pencil_y[j]);
            ctx.stroke(); 
        } 
        ctx.lineTo(iniX, iniY);
        ctx.stroke(); 
        
    }
}
     
        
// rectangle tool
function rectangle (){
            
    canvas.onmousedown = function (e){ 
        var wid_c=  document.getElementById('canvas_paint').getBoundingClientRect();  
        var wid_n=  document.getElementById('navigation_bar').getBoundingClientRect();  

        if   (wid_n>0){
            var offsetvaleft = wid_c.left+wid_n.right; 
        }else{
            var offsetvaleft = wid_c.left; 
        };  
    
        var canvas = document.getElementById("paint");
        var ctx = canvas.getContext("2d");       
        var width = canvas.width, height = canvas.height;
        img = ctx.getImageData(0, 0, width, height);        
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
        }
    };
            
    canvas.onmouseup = function (e){
        ctx.strokeRect(prevX, prevY, curX, curY);       
        hold = false;
        var canvas1 = document.getElementById("paint");
        var width = canvas1.width, height = canvas1.height;

        rectangle_data.push([width,height,prevX, prevY,curX+ prevX, curY+ prevY])
    };
            
    canvas.onmouseout = function (e){
        hold = false;
    };
}
    