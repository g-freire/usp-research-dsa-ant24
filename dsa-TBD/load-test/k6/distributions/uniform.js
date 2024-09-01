import { sleep } from 'k6';
import http from 'k6/http';
import { check } from 'k6';

// Uniform distribution
function uniformDistribution(min, max) {
    return min + Math.random() * (max - min);
}

export const options = {
    vus: 100,
    duration: '1m',
};

export default function () {
    const wait = uniformDistribution(0.5, 1.5); // min = 0.5, max = 1.5
    sleep(wait);
    
    const res = http.get('http://localhost:8080/iot');
    check(res, {
        'status is 200': (r) => r.status === 200,
    });
}
