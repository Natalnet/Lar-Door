import mqtt from 'mqtt'

import { myIp } from '../server'

const client = mqtt.connect(`mqtt://${myIp}`);

const channels = ['door/logs', 'door/nomes', 'door/heartbeat']

client.on('connect', () => {
    client.subscribe(channels);
})

client.on('message', function(topic, message) {
    const context = message.toString()

    console.log(context);
})