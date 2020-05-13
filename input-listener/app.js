import { initialiseAppEnvironment } from "./init-app-env";
import { logger } from './logger';
import {startPdfListener} from "./pdf-listener";

export async function runApp() {
    const message = await initialiseAppEnvironment();
    logger.info('Application initialisation complete:', message);

    startPdfListener();
}
