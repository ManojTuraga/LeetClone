// https://www.kirupa.com/canvas/creating_motion_trails.htm
// https://www.youtube.com/watch?app=desktop&v=D_BPilf_F8k&t=41s
// https://www.jeffreythompson.org/collision-detection/circle-circle.php

// canvas setup
const particle_canvas = document.getElementById("particle-canvas");
const ctx = particle_canvas.getContext("2d");

particle_canvas.style.width ='100%';
particle_canvas.style.height='100%';
particle_canvas.width  = particle_canvas.offsetWidth;
particle_canvas.height = particle_canvas.offsetHeight;

// window sizes
let width = particle_canvas.width;
let height = particle_canvas.height;
let min_size = Math.min(width, height);

// important point locations
let center_x = width / 2;
let center_y = height / 2;

// base velocity
let velocity = 1;
let acceleration = 1;
let particle_rad = 5;
let particle_amount = 150;

let mouse = 
{
    x: null,
    y: null,
    radius: (width / 120) * (height / 120)
}

window.addEventListener(
    "mousemove",
    function(event)
    {
        mouse.x = event.x;
        mouse.y = event.y;
    }
);

// what to do when the window gets resized.
window.onresize = function() 
    {
        particle_canvas.width  = particle_canvas.offsetWidth;
        particle_canvas.height = particle_canvas.offsetHeight;

        width = particle_canvas.width;
        height = particle_canvas.height;
        min_size = Math.min(width, height);

        center_x = width / 2;
        center_y = height / 2;

        //particle_canvas.clear()
    }

const particles = 
{
    // store all particles here
    points: [],

    // generating points 
    pointGen()
    {
        //let point_x = (Math.cos(direction) * circle_rad) + center_x;
        //let point_y = (Math.sin(direction) * circle_rad) + center_y;

        let point_x =  Math.random() * width;
        
        let point_y =  center_y;

        let direction = this.pointDirCalc(point_x, point_y);

        const point = 
        {
            x: point_x,
            y: point_y,
            positions: [{x: point_x, y: point_y}],
            direction: direction,
            velocity: velocity,
            alive_time: 0,
            alpha: 0
        };

        particles.points.push(point);
    },

    // drawing points
    drawPoints()
    {
        // iterating through all the particle points 
        for (let i = 0; i < particles.points.length; i++)
        {   
            point = particles.points[i];
            
            // checking if the point is  within the canvas 
            if ( (point.x > 0 && point.x < width) && (point.y > 0 && point.y < width) ) 
            {  
                for (let j = 0; j < point.positions.length; j++) {
                    let ratio = (j + 1) / point.positions.length;

                    ctx.beginPath();
                    ctx.arc(point.positions[j].x, point.positions[j].y, particle_rad, 0, 2 * Math.PI, true);
                    ctx.fillStyle = `rgba(255, 255, 255, ${(ratio / 2) * point.alpha})`;
                    ctx.fill();
                  }
                
                this.pointUpdate(point);
            }
            else 
            {
                // if the point is not within the screen, remove it from our list 
                particles.points[i] = particles.points[particles.points.length - 1];
                particles.points.pop();
            }
        }
    },

    pointUpdate(point)
    {   
        if (point.positions.length > 10)
        {
            point.positions.shift();
        }
        
        let is_collision = false;

        // Collision Detection (Comment out of if the webpage runs slow idk how to optimize this!)
        /*let dx = mouse.x - point.x;
        let dy = mouse.y - point.y;
        let col_dis = Math.sqrt((dx * dx) + (dy * dy))
        
        if (col_dis <= mouse.radius + particle_rad)
        {
            is_collision = true;
            if (mouse.x < point.x && point.x < width - (particle_rad * 3))
            {
                point.x += 2;
            }

            else if (mouse.x > point.x && point.x > (particle_rad * 3))
            {
                point.x -= 2;
            }

            if (mouse.y < point.y && point.y < height - (particle_rad * 3))
            {
                point.y += 2;
            }

            else if (mouse.y > point.y && point.y > (particle_rad * 3))
            {
                point.y -= 2;
            }
        }*/
        // END OF COLLISION DETECTION

        point.x += Math.cos(point.direction) * ( (point.velocity * point.alive_time) + (0.5 * acceleration * (point.alive_time ** 2)) );
        point.y += Math.sin(point.direction) * ( (point.velocity * point.alive_time) + (0.5 * acceleration * (point.alive_time ** 2)) );
        point.positions.push({x: point.x, y: point.y});
        
        point.velocity = !is_collision ? point.velocity + (acceleration * point.alive_time) : point.velocity;
        point.alive_time += 0.001;

        if (point.alive_time > 0.1)
        {
            point.alpha += 0.01;
        }
        
    },

    pointDirCalc(point_x, point_y)
    {
        let dir_scale = 0.4;
        let offset = ((1 - dir_scale) / 2) * width; 
        let point_x_dir = Math.abs(center_x - point_x) / ((dir_scale / 2) * width);
        point_x_dir *= offset;

        if (point_x - center_x < 0)
        {
            point_x_dir = -1 * point_x_dir;
            point_x_dir += point_x;
        }
        else
        {
            point_x_dir += point_x;
        }

        let direction = Math.random() * 2 * Math.PI;
        let random_quad = Math.random() < 0.5 ? 1 : -1;
        direction = Math.atan((random_quad * point_y)/(point_x_dir - center_x));
        
        if (point_x - center_x < 0)
        {
            direction += Math.PI;
        }

        return direction;
    }
}


// loop initalization
function init()
{
    window.requestAnimationFrame(mainLoop);
}


// main drawing loop
function mainLoop()
{
    ctx.clearRect(0, 0, width, height);
    
    if (particles.points.length < particle_amount)
    {
        particles.pointGen();
    }
    particles.drawPoints();

    window.requestAnimationFrame(mainLoop);
}

init();
