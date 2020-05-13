import { minioClient } from './minio-client'

export async function initialiseAppEnvironment() {
    const buckets = await minioClient.listBuckets();

    const bucketName = process.env.INPUT_BUCKET_NAME;
    if (!buckets.map(bucket => bucket.name).includes(bucketName)) {
        return minioClient.makeBucket(bucketName, 'eu-west-1');
    }

    return 'already initialised';
}
