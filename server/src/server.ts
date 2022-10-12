import express from 'express'
import router from './routes'

/*
Mude isso para seu IP local
*/

export const myIp = '192.168.1.2';

const app = express();

app.use(router);

app.use(express.json());