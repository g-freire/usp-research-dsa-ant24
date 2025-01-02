// k6 run load_simple_test.js
import http from 'k6/http';
import { check } from 'k6';

export let options = {
    vus: 10,        // Number of concurrent users
    iterations: 100,  // Total number of requests to make
    duration: '60s',  // Time limit (e.g., '30s', '1m', '1h')
};

export default function () {
    const res = http.get('http://iot-api.local/iot/');
    check(res, {
        'status is 200': (r) => r.status === 200,
    });
}