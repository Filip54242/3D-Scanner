rgb_image = document.getElementById('rgb_image');
depth_raw = document.getElementById('depth_raw');
depth_colorized = document.getElementById('depth_colorized');
rotate_clockwise = document.getElementById('rotate_clockwise');
rotate_counterclockwise = document.getElementById('rotate_counterclockwise');

rgb_image.onclick = function (_) { fetch('/rgb_image') };
depth_raw.onclick = function (_) { fetch('/depth_raw') };
depth_colorized.onclick = function (_) { fetch('/depth_colorized') };
rotate_clockwise.onclick = function (_) { fetch('/clockwise') };
rotate_counterclockwise.onclick = function (_) { fetch('/counterclockwise') };
