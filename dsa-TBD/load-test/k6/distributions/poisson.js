import { sleep } from 'k6';
import http from 'k6/http';
import { check } from 'k6';

// Poisson distribution approximation using the inverse transform sampling method
function poissonDistribution(lambda) {
    let L = Math.exp(-lambda);
    let k = 0;
    let p = 1;
    do {
        k++;
        p *= Math.random();
    } while (p > L);
    return k - 1;
}

export const options = {
    vus: 500,
    duration: '3m',
};

export default function () {
    const wait = poissonDistribution(1); // Lambda = 1
    sleep(wait);
    
    const res = http.get('http://localhost:8080/iot');
    check(res, {
        'status is 200': (r) => r.status === 200,
    });
}
