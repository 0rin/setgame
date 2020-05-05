var selected_cards = [];
function myFunction(card_id) {
    console.log(card_id)
    // console.log(document.getElementById(card_id))
    if (selected_cards.includes(card_id)) {
        var card_index = selected_cards.indexOf(card_id);
        document.getElementById(card_id).style.background = 'white';
        console.log(card_index)
        selected_cards.splice(card_index, 1);
    }
    else {
        document.getElementById(card_id).style.background = 'grey';
        selected_cards.push(card_id)
        if (selected_cards.length == 3) {
            console.log('Ja, 3 kaarten. Maar is het ook een set?')
            // loop over selected_cards and for each
            selected_cards.forEach(card => {
                document.getElementById(card).style.background = 'white';
            });
            selected_cards = [];
        }
    }

    console.log('selected_cards are', selected_cards);
}
