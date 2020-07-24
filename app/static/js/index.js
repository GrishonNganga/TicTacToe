$(document).ready(()=>{
    
    
    socket.on('my response', (data)=>{
        console.log(data)
    })
    
    socket.on('show message', (message)=>{
        $('.chat').append(message)
    })

    $('.send').click(()=>{
        alert('Works')
        game_id = make_id()
        window.location.href = `/${game_id}`
       
    })
})

function make_id() {
    return '_' + Math.random().toString(36).substr(2, 9);
  };