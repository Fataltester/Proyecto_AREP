import http from 'k6/http';
import { sleep, check } from 'k6';

// ----------------------
// CONFIGURACIÓN
// ----------------------
export let options = {
    stages: [
        { duration: '30s', target: 5 },   // sube a 5 usuarios
        { duration: '1m', target: 20 },   // sube a 20 usuarios
        { duration: '30s', target: 0 },   // baja a 0 usuarios
    ],
    thresholds: {
        http_req_duration: ['p(95)<500'], // 95% de requests < 500ms
    },
};

// ----------------------
// PARÁMETROS DE LA PRUEBA
// ----------------------
const counts = [50, 100, 200, 400, 700];

export default function () {
    for (let i = 0; i < counts.length; i++) {
        let url = `https://z5aezszkv2.execute-api.us-east-1.amazonaws.com/beta/generate?count=${counts[i]}`;
        let res = http.get(url);

        check(res, {
            'status is 200': (r) => r.status === 200
        });

        sleep(1);
    }
}
