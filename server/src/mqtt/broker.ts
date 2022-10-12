import mosca from 'mosca'

import { myIp } from '../server'

const defaultPort = 1883;

const server = new mosca.Server({
    port: defaultPort
})

server.on('ready', function() {
    console.log(`MQTT habilitado com sucesso, URL: mqtt://${myIp}:${defaultPort}`)
})