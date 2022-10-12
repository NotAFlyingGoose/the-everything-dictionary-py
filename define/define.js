const input = $('#search')[0];
const word_div = $('#word')[0];

function search(ele) {
    if (event.key === 'Enter' && ele.value != '') {
        let word = ele.value;
        ele.value = '';
        ele.blur();

        // set state
        document.title = word + ' | The Everything Dictionary';
        let nextURL = window.location.protocol + "//" + window.location.host + '/define/?word=' + word;
        let nextTitle = word + ' | The Everything Dictionary';
        let nextState = { additionalInformation: 'Searched for word ' + word };
        window.history.pushState(nextState, nextTitle, nextURL);

        lookup(word).catch(console.error);
    }
}

async function lookup(word) {
    console.log('finding word ' + word);

    let page = await getVocabComDefinition(word);
    console.log(page);

    word_div.innerHTML = '';
    word_div.appendChild(id(element('h1', word), 'title'));
    let word_area = document.createElement('div');

    word_div.appendChild(word_area);
}

function element(tag, text) {
    const el = document.createElement(tag);
    const textNode = document.createTextNode(text);
    el.appendChild(textNode);
    return el;
}

function class_(el, str) {
    el.setAttribute('class', str);
    return el;
}

function id(el, str) {
    el.setAttribute('id', str);
    return el;
}

document.onkeydown = function (evt) {
    evt = evt || window.event;
    if (input !== document.activeElement) {
        window.scrollTo(0, 0);
        input.focus();
        input.select();
    }
};

const params = new Proxy(new URLSearchParams(window.location.search), {
    get: (searchParams, prop) => searchParams.get(prop),
});
const word = params.word;
document.title = word + ' | The Everything Dictionary';
lookup(word).catch(console.error);