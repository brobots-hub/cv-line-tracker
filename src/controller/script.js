window.addEventListener('keydown', onKeyPress, false);
window.addEventListener('keyup', onKeyRelease, false);

let api_url = 'xyz.xyz/api/v1';

let current_speed = 1;
let max_speed = 255;
let multiplier = 1.5;

let current_angle = 90;
let min_angle = 30;
let max_angle = 120;
let turn_angle = 10;

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
      current_angle -= turn_angle;
      break;

    case 68:
      console.log('d pressed');
      current_angle += turn_angle;
      break;

    case 16:
      console.log('ctrl pressed');
      current_speed = 1;
      current_angle = 90;
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

  fetch('/motor', {
    method: 'POST',
    body: mUrlencoded,
    headers,
  });

  let rUrlencoded = new URLSearchParams();
  rUrlencoded.append('angle', current_angle);

  fetch('/servo', {
    method: 'POST',
    body: rUrlencoded,
    headers,
  });
}

function onKeyRelease(e) {}
