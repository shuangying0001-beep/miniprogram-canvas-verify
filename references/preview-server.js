/*
 * preview-server.js — 小程序 Canvas 本地静态预览服务（教备神器 · 工具模块）
 * 移植自项目 preview-server.js，支持命令行指定根目录与端口。
 * 用法：node preview-server.js [rootDir] [port]
 *   默认 rootDir=__dirname, port=9099
 * 浏览器打开 http://127.0.0.1:9099/<你的preview.html> 即可预览（Canvas 效果 = 小程序效果）。
 */
const http = require('http');
const fs = require('fs');
const path = require('path');

const ROOT = process.argv[2] ? path.resolve(process.argv[2]) : __dirname;
const PORT = parseInt(process.argv[3] || '9099', 10);

const mime = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css',
  '.js': 'application/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.ttf': 'font/ttf',
  '.woff2': 'font/woff2'
};

http.createServer(function (req, res) {
  let filePath = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
  if (filePath === ROOT || filePath === path.join(ROOT, '/')) {
    filePath = path.join(ROOT, 'index.html');
  }
  const ext = path.extname(filePath).toLowerCase();
  const type = mime[ext] || 'application/octet-stream';
  fs.readFile(filePath, function (err, data) {
    if (err) {
      res.writeHead(404);
      res.end('404 Not Found');
      return;
    }
    res.writeHead(200, { 'Content-Type': type });
    res.end(data);
  });
}).listen(PORT, '127.0.0.1', function () {
  console.log('Server running at http://127.0.0.1:' + PORT + '/  (root: ' + ROOT + ')');
});
