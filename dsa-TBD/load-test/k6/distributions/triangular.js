import { sleep } from 'k6';
import http from 'k6/http';
import { check } from 'k6';

// Triangular distribution approximation
function triangularDistribution(min, mode, max) {
    let F = (mode - min) / (max - min);
    let u = Math.random();
    if (u < F) {
        return min + Math.sqrt(u * (max - min) * (mode - min));
    } else {
        return max - Math.sqrt((1 - u) * (max - min) * (max - mode));
    }
}

export const options = {
    vus: 100,
    duration: '1m',
};

export default function () {
    const wait = triangularDistribution(0.5, 1, 1.5); // min = 0.5, mode = 1, max = 1.5
    sleep(wait);
    
    const res = http.get('http://localhost:8080/iot');
    check(res, {
        'status is 200': (r) => r.status === 200,
    });
}