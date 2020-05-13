import * as winston from 'winston';

export const logger = winston.createLogger({
    level: 'debug',
    format: winston.format.json(),
    defaultMeta: { service: 'input-listener' },
    transports: [
        new winston.transports.Console({
            level: 'debug',
            format: winston.format.simple()
        })
    ]
});
