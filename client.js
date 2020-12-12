const http = require("http");
const net = require("net");
const url = require("url");

const { load, encode, decode } = require("./encrypt.js");

const PROXY_SERVER = "101.200.152.10";
const PROXY_PORT = 8080;

function server_options(path, body) {
    var server_options = {
        hostname: PROXY_SERVER,
        port: PROXY_PORT,
        path: path,
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Content-Length": Buffer.byteLength(body),
        },
    };
    return server_options;
}

function request(cReq, cRes) {
    var u = url.parse(cReq.url);

    load(cReq, (data) => {
        var target_options = {
            hostname: u.hostname,
            port: u.port || 80,
            path: u.path,
            method: cReq.method,
            headers: cReq.headers,
            data: data,
        };

        var body = JSON.stringify(target_options);

        encode(body, (encoded_body) => {
            var pReq = http
                .request(server_options("/", encoded_body), (pRes) => {
                    cRes.writeHead(pRes.statusCode, pRes.headers);

                    load(pRes, (ret) => {
                        decode(ret, (decoded_ret) => {
                            cRes.write(decoded_ret);
                            cRes.end();
                        });
                    });
                })
                .on("error", (e) => {
                    cRes.end();
                })
                .end(encoded_body);

            // pReq.write(encoded_body);
            // cReq.pipe(pReq);
        });
    });
}

http.createServer().on("request", request).listen(8888, "127.0.0.1");
