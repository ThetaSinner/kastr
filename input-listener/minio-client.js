import * as minio from 'minio'

export const minioClient = new minio.Client({
    endPoint: process.env.MINIO_HOST,
    port: 9000,
    useSSL: false,
    accessKey: process.env.MINIO_ACCESS_KEY,
    secretKey: process.env.MINIO_SECRET_KEY
});
