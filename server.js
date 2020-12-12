const http = require("http");
const net = require("net");
const url = require("url");

const { load, encode, decode } = require("./encrypt.js");

const C_PKEY = "7 33"; // client public key
const S_SKEY = "7 33"; // server secret key

function request(cReq, cRes) {
    if (cReq.method === "GET") {
        cRes.writeHead(404);
        cRes.end("Error");
        return;
    }

    var u = url.parse(cReq.url);

    if (u.path === "/") {
        load(cReq, (body) => {
            decode(body, C_PKEY, S_SKEY, (decoded_body, code) => {
                if (code != 0) {
                    console.log("auth failed in decoding: " + code);
                    cRes.end("auth failed in decoding: " + code);
                    return;
                }
                var options = JSON.parse(decoded_body);
                var data = options.data;
                delete options.data;

                var pReq = http
                    .request(options, (pRes) => {
                        cRes.writeHead(pRes.statusCode, pRes.headers);

                        load(pRes, (ret) => {
                            encode(ret, C_PKEY, S_SKEY, (encoded_ret, code) => {
                                if (code != 0) {
                                    console.log("encoding failed: " + code);
                                    cRes.end("encoding failed: " + code);
                                    return;
                                }
                                cRes.write(encoded_ret);
                                cRes.end();
                            });
                        });
                    })
                    .on("error", (e) => {
                        cRes.end();
                    })
                    .end(data);
            });
        });
    }
}

http.createServer().on("request", request).listen(8080, "0.0.0.0");
