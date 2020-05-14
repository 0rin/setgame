var selected_ids = [];

function cardClicked(card_id) {
    var this_card = document.getElementById(card_id);
    if (selected_ids.includes(card_id)) {
        this_card.style.background = 'white';
        var card_index = selected_ids.indexOf(card_id);
        selected_ids.splice(card_index, 1);
    }
    else {
        this_card.style.background = 'grey';
        selected_ids.push(card_id);
        if (selected_ids.length == 3) {
            submitSelectedCards();
            selected_ids.forEach(card => {
                document.getElementById(card).style.background = 'white';
            });
            selected_ids = [];
        }
    }
}

function submitSelectedCards() {
    var last_clicked_card =
        document.getElementById(selected_ids[selected_ids.length - 1])
    last_clicked_card.value = selected_ids;
    last_clicked_card.type = "submit";
}

function confirmSetExistence(card_id) {
    if (confirm('There is a set. Want a hint?')) {
        document.getElementById(card_id).style.background = "lightGrey";
    }
}

function incorrectSet() {
    alert('That is not a set.');
}

