const canvas_map = document.querySelector('canvas');
const canvas = canvas_map.getContext('2d');

const collisionMap = []
for(let i=0; i< collisions.length;i+95){
    collisionMap.push(collisions.slice(i,i+95))
}

class Boundry {
    constructor({position}){
        this.position = position
        this.width = 64
        this.height = 64
    }

    draw(){
        canvas.fillStyle='red'
        canvas.fillRect(this.position.x,this.position.y,this.width,this.height)
    }
}

const offset = {
    x: -150,
    y: -200
}

const boundaries = []
collisionMap.forEach((row,i) => {
    row.forEach((point,j) => {
        if(point > 1000)
            console.log("ich")
            boundaries.push(
                new Boundry({
                    position: {
                        x: i * Boundry.width + offset.x,
                        y: j * Boundry.height + offset.y
                    }
                })
            )
    })
})

const town = new Image();
town.src = "/static/images/townmap.png";

const playerWalk = new Image();
playerWalk.src = "/static/images/right-walk.png";

class Sprite {
    constructor(position, image) {
        this.position = position;
        this.image = image;
    }

    draw() {
        if (this.image && this.image.complete) {
            canvas.drawImage(this.image, this.position.x, this.position.y);
        }
    }
}

let background = null;

const keys = {
    w: { pressed: false },
    a: { pressed: false },
    s: { pressed: false },
    d: { pressed: false }
};

function resizeCanvas() {
    canvas_map.width = window.innerWidth - 20;
    canvas_map.height = window.innerHeight - 20;

    canvas.fillStyle = 'white';
    canvas.fillRect(0, 0, canvas_map.width, canvas_map.height);

    if (background) background.draw();

    if (playerWalk.complete) {
        canvas.drawImage(
            playerWalk,
            0, 0,
            playerWalk.width / 8, playerWalk.height,
            window.innerWidth / 2 - playerWalk.width / 8 / 2,
            window.innerHeight / 2 - playerWalk.height / 2,
            playerWalk.width / 8, playerWalk.height
        );
    }

    if (background) background.draw();
    boundaries.forEach((boundry) => {
        boundry.draw()
    })
}

function animate() {
    window.requestAnimationFrame(animate);

    if (background) background.draw();
    boundaries.forEach((boundry) => {
        boundry.draw()
    })

    if (playerWalk.complete) {
        canvas.drawImage(
            playerWalk,
            0, 0,
            playerWalk.width / 8, playerWalk.height,
            window.innerWidth / 2 - playerWalk.width / 8 / 2,
            window.innerHeight / 2 - playerWalk.height / 2,
            playerWalk.width / 8, playerWalk.height
        );
    }

    if (keys.w.pressed) background.position.y += 3;
    if (keys.a.pressed) background.position.x += 3;
    if (keys.s.pressed) background.position.y -= 3;
    if (keys.d.pressed) background.position.x -= 3;
}

// Wait for both images to load
let imagesLoaded = 0;
function tryStartGame() {
    imagesLoaded++;
    if (imagesLoaded === 2) {
        background = new Sprite(
            { x: -150, y: -200 },
            town
        );
        resizeCanvas();
        animate();
    }
}

town.onload = tryStartGame;
playerWalk.onload = tryStartGame;

// Handle window resize
window.addEventListener('resize', resizeCanvas);

// Movement input
window.addEventListener('keydown', (e) => {
    if (keys[e.key]) keys[e.key].pressed = true;
});

window.addEventListener('keyup', (e) => {
    if (keys[e.key]) keys[e.key].pressed = false;
});
