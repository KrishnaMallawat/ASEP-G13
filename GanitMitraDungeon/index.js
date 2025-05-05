const canvas = document.querySelector('canvas')

const c=canvas.getContext('2d')

canvas.width=1024
canvas.height=576

c.fillStyle='white'
c.fillRect(0,0,canvas.width,canvas.height)

const image = new Image()
image.src='ASEP 22.png' 

const playerImg= new Image()
playerImg.src='playerDown.png'

class Sprite{
    constructor(position,image){
        this.position=position
        this.image=image
    }

    draw(){
        c.drawImage(this.image,this.position.x,this.position.y)
    }
}

const bacground= new Sprite({x:-2030,y:-432},image)

window.addEventListener('keydown',(e)=>{
    // console.log(e.key)
    key_handling(e.key)
})

function animate(movement){
    window.requestAnimationFrame(animate)
    bacground.draw()
    c.drawImage(playerImg,
        0,
        0,
        playerImg.width/4,
        playerImg.height,
        175,
        canvas.height/2,
        playerImg.width/4,
        playerImg.height
    )
}
animate()

let lastKey=''

function key_handling(key){
    if(key ==="w" || key ==="ArrowUp"){
        if(lastKey==='w'|| lastKey===''){
            bacground.position.y=bacground.position.y+6;
            lastKey='up'
            console.log("Moving up\nThe new  Y  position is :",bacground.position.y)
        }
        else
        lastKey='w'
    }
    if(key ==="a" || key==="ArrowLeft"){
        if(lastKey==='a'|| lastKey===''){
            bacground.position.x=bacground.position.x+6;
            lastKey='left'
            console.log("Moving Left\nThe new  X  position is :",bacground.position.x)
        }
        else
        lastKey='a'
    }
    if(key ==="s" || key ==="ArrowDown"){
        if(lastKey==='s'|| lastKey===''){
            bacground.position.y=bacground.position.y-6;
            lastKey='down'
            console.log("Moving Down\nThe new  Y  position is :",bacground.position.y)
        }
        else
        lastKey='s'
    }
    if(key ==="d" || key==="ArrowRight"){
        if(lastKey==='d'|| lastKey===''){
            lastKey='right'
            console.log("Moving Right\nThe new  X  position is :",bacground.position.x)
            bacground.position.x=bacground.position.x-6;
        }
        else
        lastKey='d'
    }
}