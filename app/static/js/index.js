$(document).ready(()=>{
    

    $('.join').click(()=>{
        url = document.getElementById('game-id-input').value
        window.location.href = '/' + url

    })
    $('.send').click(()=>{
        $.ajax({
            url: '/',
            type: 'post',
            
        })
       
    })
})
