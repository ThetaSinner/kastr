import { minioClient } from './minio-client'

export async function initialiseAppEnvironment() {
    const buckets = await listBuckets();

    const bucketName = process.env.INPUT_BUCKET_NAME;
    if (!buckets.map(bucket => bucket.name).includes(bucketName)) {
        return createBucket(bucketName);
    }

    return 'already initialised';
}

function listBuckets() {
    return new Promise((resolve, reject) => {
        minioClient.listBuckets((err, buckets) => {
            if (err) return reject(err);
            resolve(buckets);
        })
    })
}

function createBucket(bucketName) {
    return new Promise((resolve, reject) => {
        minioClient.makeBucket(bucketName, 'eu-west-1', err => {
            if (err) return reject(err);
            resolve('Bucket created');
        });
    });
}
