
const proxy = 'http://www.whateverorigin.org/get?url='

const protocol = 'https';
const vocab_com_url_base = protocol + '://vocabulary.com';
const slang_url_base = protocol + '://urbandictionary.com';
const wiki_url_base = protocol + '://wiktionary.org';

async function getRawData(url) {
    let start = new Date();
    console.log('fetching');
    let response = await fetch(proxy + encodeURIComponent(url));
    console.log('fetched in ' + (Math.abs(new Date() - start)) / 1000.0 + ' seconds');
    return await response.json().catch(console.error);
}

async function getVocabComDefinition(word) {
    let data = await getRawData(vocab_com_url_base + '/dictionary/definition.ajax?search=' + word);
    console.log(data.contents);
    //console.log(data.contents);
}