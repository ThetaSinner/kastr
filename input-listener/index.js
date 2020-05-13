require("@babel/register");
const app = require('./app');

try {
    (async () => {
        await app.runApp()
    })();
} catch (e) {
    console.error(e);
    process.exit(1)

}
