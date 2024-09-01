import http from 'k6/http';
import { check, sleep } from 'k6';


export let options = {
  vus: 50, // virtual concurrent users
  duration: '30s',

  // stages: [
  //   { duration: '30s', target: 20 },
  //   { duration: '1m30s', target: 10 },
  //   { duration: '20s', target: 0 },
  // ],
};

// ADD SENSSOR ENDPOINT
const baseUrl = "http://18.228.182.12:3000" // CLOUD
// const baseUrl = "http://127.0.0.1:8080"; // LOCAL
const endpoint = '/iot/'; // READ
// const endpoint = '/iot/create?n=500' //WRITE

var params = {
  headers: {
    'Content-Type': 'application/json',
  },
//   headers: {
//     'Content-Type': 'application/json',
//     'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXJ2aWNlIjoiZG9taW5vIiwib3BlcmF0b3IiOiJUZXN0In0.ElUKEixsdiaTMuupvqPSj_SBRJyloRtxvc6oeOTFGC0'
//   },
};

export default function () {
  //Generate data
  let res = http.get(baseUrl + endpoint, params);
  check(res, { 'status was 200': (r) => r.status == 200 });
  sleep(1);
}
