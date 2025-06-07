const canvas = document.querySelector('canvas')

const city = canvas.getContext('2d')

canvas.width = 1024
canvas.height = 576

city.fillStyle = 'blue'
city.fillRect(0,0,canvas.width,canvas.height)

const img = new Image()
img.src='../static/images/trialcitymap.png'

const playerImg = new Image()
playerImg.src='../static/images/playerRight.png'

class Sprite {
    constructor({position,velocity,image}){
        this.position = position
        this.image = image
    }

    draw(){
        city.drawImage(this.image,this.position.x,this.position.y)
    }
}

class Boundary  {
    static width = 48;
    static height = 48;
    constructor({position}){
        this.position = position
        this.width = 48
        this.height = 48
    }

    draw(){
        city.fillStyle = 'red'
        city.fillRect(this.position.x,this.position.y,this.width,this.height)
    }
}

const boundaries =[]     

const offset ={
    x : -750,
    y : -700
}

const background = new Sprite({
    position:{
        x : offset.x,
        y : offset.y
    },
    image : img
})

const keys={
    w: {
        pressed : false
    },
    a: {
        pressed : false
    },
    s: {
        pressed : false
    },
    d: {
        pressed : false
    },
}

const collisionMap = []
for(let i=0;i<collisions.length ; i+=70){
    collisionMap.push(collisions.slice(i,i+70))
}
// console.log(collisionMap)

collisionMap.forEach((row,i) => {
    row.forEach((value,j) => {
        if(value==340){
            boundaries.push(
                new Boundary({
                    position:{
                        x: j*Boundary.width + offset.x,
                        y: i*Boundary.height + offset.y
                    }
                })
            )
        }
    })
    
});

// console.log(boundaries)

window.addEventListener('keydown',(e) => {
    switch(e.key){
        case 'w':
            keys.w.pressed = true
            break
        case 'a':
            keys.a.pressed = true
            break
        case 's':
            keys.s.pressed = true
            break
        case 'd':
            keys.d.pressed = true
            break
    }
})

window.addEventListener('keyup',(e) => {
    switch(e.key){
        case 'w':
            keys.w.pressed = false
            break
        case 'a':
            keys.a.pressed = false
            break
        case 's':
            keys.s.pressed = false
            break
        case 'd':
            keys.d.pressed = false
            break
    }
})

function animate(){
    window.requestAnimationFrame(animate)
    background.draw()
    boundaries.forEach(boundary => {
        boundary.draw()
    })
    city.drawImage(
        playerImg, 
        0,
        0,
        playerImg.width/4,
        playerImg.height,
        canvas.width/2 - playerImg.width/4 /2 , 
        canvas.height/2 - playerImg.height/2,
        playerImg.width/4,
        playerImg.height
    )

    if(keys.w.pressed) {
        background.position.y+=3
    }
    else if(keys.a.pressed){
        background.position.x+=3
    } 
    else if(keys.s.pressed){ 
        background.position.y-=3
    }
    else if(keys.d.pressed){ 
        background.position.x-=3
    }
}
animate()
