var input = $('#search')[0];

function search(ele) {
    if (event.key === 'Enter' && ele.value != '') {
        let new_word = ele.value;
        ele.value = '';
        ele.blur();
        window.location.href = 'define/?word=' + new_word;
    }
}

document.onkeydown = function (evt) {
    evt = evt || window.event;
    if (input !== document.activeElement) {
        window.scrollTo(0, 0);
        input.focus();
        input.select();
    }
};