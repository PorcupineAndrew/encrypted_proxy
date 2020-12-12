var http = require("http");
var net = require("net");
var url = require("url");

var PROXY_SERVER = "101.200.152.10";
var PROXY_PORT = 8080;

function server_options(path, body) {
    // TODO: encode body
    var server_options = {
        hostname: PROXY_SERVER,
        port: PROXY_PORT,
        path: path,
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Content-Length": Buffer.byteLength(body)
        }
    };
    return server_options;
}

function request(cReq, cRes) {
    var u = url.parse(cReq.url);

    var target_options = {
        hostname: u.hostname,
        port: u.port || 80,
        path: u.path,
        method: cReq.method,
        headers: cReq.headers
    };

    var body = JSON.stringify(target_options);
    console.log("request to proxy server: " + body);

    var pReq = http
        .request(server_options("/", body), pRes => {
            cRes.writeHead(pRes.statusCode, pRes.headers);
            pRes.pipe(cRes);
        })
        .on("error", e => {
            cRes.end();
        })
        .end(body);

    cReq.pipe(pReq);
}

http.createServer()
    .on("request", request)
    .listen(8888, "127.0.0.1");
