const ingredients = require('./ingredients.json');
const request = require('request');
const assert = require("assert");
const promisify = require('util').promisify;
const cheerio = require('cheerio');
const fs = require("fs");


async function searchImages(word) {
    try {

        let url = `https://yandex.ru/images/search?text=${encodeURIComponent(word)}&q=123`;
        let response = await promisify(request.get)(url);
        assert.equal(response && response.statusCode, 200);
        // noinspection JSUnresolvedFunction
        let $ = cheerio.load(response.body);
        function parseUrl(index) {
            try {
                let dataBem = $('.serp-item_pos_' + index.toString()).attr('data-bem');
                dataBem = JSON.parse(dataBem);
                assert.equal(typeof dataBem['serp-item'].img_href, 'string');
                return dataBem['serp-item'].img_href;
            }
            catch (e) {
                return null;
            }
        }
        return Array(5).fill(0).map((v, i) => parseUrl(i));
    }
    catch (e) {
        console.log(e);
        return [];
    }
}
async function getImages() {
    // noinspection JSUnresolvedFunction
    let result = [];
    // noinspection JSUnresolvedVariable
    for (let i = 0; i < ingredients.length; i++) {
        // noinspection SpellCheckingInspection
        let ingr = Object.assign({}, ingredients[i]);
        ingr.urls = await searchImages(ingr.name);
        ingr.cur = 0;
        console.log(`${Number((i + 1) / ingredients.length * 100).toFixed(1)}% (${i + 1}/${ingredients.length}) "${ingr.name}":
${ingr.urls.join('\n')}`);
        result.push(ingr);
        await promisify(setTimeout)(3 * 1000);
    }
    return result;
}

async function test() {
    for (let i = 0; i < 25; i++) {
        await promisify(setTimeout)(1000);
        console.log(i);
    }
}
async function append() {
    let items = require('./updatedIngredientsMulti.json');
    for (let  i = 0; i < items.length; i++) {
        let item = items[i];
        if (item.urls && item.urls.indexOf(null) === -1) {
            continue;
        }
        item.urls = await searchImages(item.name);
        console.log(`${i}: ${item.name}
${item.urls.join('\n')}`);
        await promisify(setTimeout)(3000);
    }

    fs.writeFileSync('updatedIngredientsMulti.json', JSON.stringify(items));
}
function selectUrl() {
    let items = require('./updatedIngredientsMulti.json');
    items.forEach(item => {
        item.url = item.urls[parseInt(item.cur)];
    });

    fs.writeFileSync('updatedIngredientsMulti.json', JSON.stringify(items));
}
function run() {
    getImages()
        .then(images => {
            fs.writeFileSync('updatedIngredientsMulti.json', JSON.stringify(images));
        })
        .catch(e => {
            console.log('Error:', e);
        });
}

module.exports.search = searchImages;
module.exports.run = append;
module.exports.test = test;

selectUrl();