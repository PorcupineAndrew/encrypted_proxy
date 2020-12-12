const http = require("http");
const net = require("net");
const url = require("url");

const { load, encode, decode } = require("./encrypt.js");

function request(cReq, cRes) {
    if (cReq.method === "GET") {
        cRes.writeHead(404);
        cRes.end("Error");
        return;
    }

    var u = url.parse(cReq.url);

    if (u.path === "/") {
        load(cReq, (body) => {
            decode(body, (decoded_body) => {
                var options = JSON.parse(decoded_body);
                var data = options.data;
                delete options.data;

                var pReq = http
                    .request(options, (pRes) => {
                        cRes.writeHead(pRes.statusCode, pRes.headers);

                        load(pRes, (ret) => {
                            encode(ret, (encoded_ret) => {
                                cRes.write(encoded_ret);
                                cRes.end();
                            });
                        });
                    })
                    .on("error", (e) => {
                        cRes.end();
                    });

                pReq.write(data);
                // cReq.pipe(pReq);
            });
        });
    }
}

http.createServer().on("request", request).listen(8080, "0.0.0.0");
