const http = require("http");
const net = require("net");
const url = require("url");

const { encode, decode } = require("./encrypt.js");

function request(cReq, cRes) {
    if (cReq.method === "GET") {
        cRes.writeHead(404);
        cRes.end("Error");
        return;
    }

    var u = url.parse(cReq.url);

    if (u.path === "/") {
        var body = "";
        cReq.on("data", (d) => {
            body += d;
            if (body.length > 1500) {
                cRes.writeHead(413, "Request Entity Too Large", {
                    "Content-Type": "text/html",
                });
                cRes.end("Error 413");
            }
        });

        cReq.on("end", () => {
            decode(body, (decoded_body) => {
                var options = JSON.parse(decoded_body);
                console.log("request to: " + options["hostname"]);

                var pReq = http
                    .request(options, (pRes) => {
                        cRes.writeHead(pRes.statusCode, pRes.headers);
                        // pRes.pipe(cRes);
                        let ret = "";

                        pRes.on("data", (d) => {
                            ret += d;
                        });

                        pRes.on("end", () => {
                            encode(ret, (encoded_ret) => {
                                cRes.write(encoded_ret);
                                cRes.end();
                            });
                        });
                    })
                    .on("error", (e) => {
                        cRes.end();
                    });

                cReq.pipe(pReq);
            });
        });
    }
}

http.createServer().on("request", request).listen(8080, "0.0.0.0");
