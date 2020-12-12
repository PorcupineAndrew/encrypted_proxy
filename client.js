const http = require("http");
const net = require("net");
const url = require("url");

const { load, encode, decode } = require("./encrypt.js");

const PROXY_SERVER = "101.200.152.10";
const PROXY_PORT = 8080;

const C_SKEY = "3 33"; // client secret key
const S_PKEY = "3 33"; // server public key

function server_options(path, body) {
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

    load(cReq, data => {
        var target_options = {
            hostname: u.hostname,
            port: u.port || 80,
            path: u.path,
            method: cReq.method,
            headers: cReq.headers,
            data: data
        };

        var body = JSON.stringify(target_options);

        encode(body, S_PKEY, C_SKEY, (encoded_body, code) => {
            if (code != 0) {
                console.log("encoding failed: " + code);
                cRes.end("encoding failed: " + code);
                return;
            }
            var pReq = http
                .request(server_options("/", encoded_body), pRes => {
                    // cRes.writeHead(pRes.statusCode, pRes.headers);
                    load(pRes, ret => {
                        console.log(ret.length);
                        // decode(ret, S_PKEY, C_SKEY, (decoded_ret, code) => {
                        //     cRes.writeHead(pRes.statusCode, pRes.headers);
                        //     if (code != 0) {
                        //         console.log(
                        //             "here auth failed in decoding: " + code
                        //         );
                        //         return;
                        //     }
                        //     cRes.writeHead(pRes.statusCode, {
                        //         "Content-Type": "application/json",
                        //         "Content-Length": decoded_ret.length
                        //     });
                        //     cRes.write(JSON.stringfy({ data: decoded_ret }));
                        //     cRes.end();
                        // });
                        cRes.write(ret);
                        cRes.end();
                    });
                })
                .on("error", e => {
                    cRes.end();
                })
                .end(encoded_body);
        });
    });
}

http.createServer()
    .on("request", request)
    .listen(8888, "127.0.0.1");
