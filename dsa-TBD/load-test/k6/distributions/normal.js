import { sleep } from 'k6';
import http from 'k6/http';
import { check } from 'k6';

// Simple normal distribution approximation using Box-Muller transform
function normalDistribution(mean, stddev) {
    let u1 = Math.random();
    let u2 = Math.random();
    let z1 = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
    return mean + stddev * z1;
}

export const options = {
    vus: 500,
    duration: '3m',
};

export default function () {
    const wait = Math.abs(normalDistribution(1, 0.2)); // mean = 1, stddev = 0.2
    sleep(wait);
    
    const res = http.get('http://localhost:8080/iot');
    check(res, {
        'status is 200': (r) => r.status === 200,
    });
}
