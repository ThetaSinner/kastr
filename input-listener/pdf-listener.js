import { minioClient } from "./minio-client";
import {logger} from "./logger";

export function startPdfListener() {
    const listener = minioClient.listenBucketNotification(process.env.INPUT_BUCKET_NAME, '', '.pdf', ['s3:ObjectCreated:*'])

    logger.debug('Starting listener');
    listener.on('notification', record => {
        logger.info(JSON.stringify(record));
    });
}
