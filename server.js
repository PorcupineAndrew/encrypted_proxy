var http = require("http");
var net = require("net");
var url = require("url");

function request(cReq, cRes) {
    if (cReq.method === "GET") {
        cRes.writeHead(404);
        cRes.end("Error");
        return;
    }

    var u = url.parse(cReq.url);

    if (u.path === "/") {
        var reqbody = "";
        cReq.on("data", (d) => {
            reqbody += d;
            if (reqbody.length > 1500) {
                cRes.writeHead(413, "Request Entity Too Large", {
                    "Content-Type": "text/html",
                });
                cRes.end("Error 413");
            }
        });

        cReq.on("end", () => {
            var options = JSON.parse(reqbody);
            console.log("request to: " + options["hostname"]);

            var pReq = http
                .request(options, (pRes) => {
                    cRes.writeHead(pRes.statusCode, pRes.headers);
                    pRes.pipe(cRes);
                })
                .on("error", (e) => {
                    cRes.end();
                });

            cReq.pipe(pReq);
        });
    }
}

http.createServer().on("request", request).listen(8080, "0.0.0.0");
