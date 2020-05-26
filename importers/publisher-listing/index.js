const https = require('https');
const fs = require('fs');
const xray = require("x-ray")();

const populateCache = async cacheFilePath => {
    return new Promise(((resolve, reject) => {
        https.get('https://en.wikipedia.org/wiki/List_of_English-language_book_publishing_companies', res => {
            console.log('Status code', res.statusCode);

            const file = fs.openSync(cacheFilePath, 'w');

            res.on('data', data => {
                fs.writeSync(file, data);
                resolve();
            });
        }).on('error', err => {
            console.error(err);
            reject(err);
        });
    }));
};

const extractPublishers = async (content) => {
    return new Promise(((resolve, reject) => {
        const selector = ['li a@title']
        xray(content, '#content', selector)((err, result) => {
            if (err) {
                console.error(err);
                reject(err);
                return;
            }

            const cleanedResult = result.filter(value => value);
            resolve(cleanedResult);
        });
    }));
};

(async () => {
    try {
        const cacheFilePath = 'cached-page.html';

        if (!fs.existsSync(cacheFilePath)) {
            console.log('Fetching page and caching it.');
            await populateCache(cacheFilePath);
        }

        const content = fs.readFileSync(cacheFilePath);
        const publishers = await extractPublishers(content.toString());

        const outFilePath = 'publishers.json';
        fs.writeFileSync(outFilePath, JSON.stringify(publishers));
    } catch (e) {
        console.error(e);
    }
})();
