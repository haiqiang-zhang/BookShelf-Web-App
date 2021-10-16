function read_book(book_id){
    fetch(`/read_a_book?read_book_id=${book_id}`)
        .then(response =>{
            if (response.redirected){
                window.location.href = response.url;
            }
            else {
                response.text().then(message => alert(message))
            }
    })
}

function favourite_book(book_id){
    fetch(`/favourite_a_book?fav_book_id=${book_id}`)
        .then(response =>{
            if (response.redirected){
                window.location.href = response.url;
            }
            else {
                response.text().then(message => alert(message))
            }
    })
}