var selected_cards = [];
var colors = []
var numbers = []
var shadings = []
var shapes = []

function cardClicked(card_id, color, number, shading, shape) {
    if (selected_cards.includes(card_id)) {
        var card_index = selected_cards.indexOf(card_id);
        document.getElementById(card_id).style.background = 'white';
        removeFromArrays(card_index, color, number, shading, shape);
    }
    else {
        document.getElementById(card_id).style.background = 'grey';
        addToArrays(card_id, color, number, shading, shape);
        if (selected_cards.length == 3) {
            validateSet([colors, numbers, shadings, shapes]);
            selected_cards.forEach(card => {
                document.getElementById(card).style.background = 'white';
            });
            resetArrays();
        }
    }
}


function validateSet(properties) {
    for (i = 0; i < properties.length   ; i++) {
        uniq = [...new Set(properties[i])];
        if (uniq.length == 2) {
            alert('Sorry, this was not a set.');
            return
        }
    };
    alert('SET!')
}

function addToArrays(card_id, color, number, shading, shape) {
    selected_cards.push(card_id);
    colors.push(color);
    numbers.push(number);
    shadings.push(shading);
    shapes.push(shape);
}

function removeFromArrays(card_index, color, number, shading, shape) {
    selected_cards.splice(card_index, 1);
    colors.splice(card_index, 1);
    numbers.splice(card_index, 1);
    shadings.splice(card_index, 1);
    shapes.splice(card_index, 1);
}

function resetArrays() {
    selected_cards = [];
    colors = [];
    numbers = [];
    shadings = [];
    shapes = [];
}
