window.addEventListener('keydown', onKeyPress, false);
window.addEventListener('keyup', onKeyRelease, false);

let api_url = 'http://192.168.88.76:8080/api/v1';

let current_speed = 0.001;
let max_speed = 1;
let multiplier = 1.5;

let current_angle = 0.125;
let min_angle = 0.04;
let max_angle = 0.21;
let turn_angle = 0.007;

function onKeyPress(e) {
  let keyCode = e.keyCode;

  switch (keyCode) {
    case 87:
      console.log('w pressed');
      current_speed *= multiplier;
      break;

    case 83:
      console.log('s pressed');
      current_speed /= multiplier;
      break;

    case 65:
      console.log('a pressed');
      current_angle += turn_angle;
      break;

    case 68:
      console.log('d pressed');
      current_angle -= turn_angle;
      break;

    case 16:
      console.log('shift pressed');
      current_speed = 0.2;
      current_angle = 0.125;
      break;

    default:
      break;
  }

  if (current_speed > max_speed) current_speed = max_speed;

  if (current_angle < min_angle) current_angle = min_angle;
  if (current_angle > max_angle) current_angle = max_angle;

  let headers = new Headers();
  headers.append('Content-Type', 'application/x-www-form-urlencoded');

  let mUrlencoded = new URLSearchParams();
  mUrlencoded.append('power', current_speed);

  fetch(api_url + '/motor', {
    method: 'POST',
    body: mUrlencoded,
    headers,
  });

  let rUrlencoded = new URLSearchParams();
  rUrlencoded.append('angle', current_angle);

  fetch(api_url + '/servo', {
    method: 'POST',
    body: rUrlencoded,
    headers,
  });
  console.log('angle=' + current_angle);
}

function onKeyRelease(e) {}
