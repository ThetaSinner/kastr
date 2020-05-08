const winston = require('winston')

const logger = winston.createLogger({
    level: 'info',
    format: winston.format.json(),
    defaultMeta: { service: 'input-listener' },
    transports: [
        new winston.transports.Console({
            level: 'info',
            format: winston.format.simple()
        })
    ]
});

logger.info('testing')
