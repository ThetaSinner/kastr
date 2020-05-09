import { initialiseAppEnvironment } from "./init-app-env";

export function runApp() {
    initialiseAppEnvironment().then(msg => {
        console.log('Application initialisation complete:', msg);
    }).catch(err => {
        console.error(err);
        process.exit(1)
    });
}
