const { spawn, spawnSync } = require("child_process");

module.exports = {
    encode: function (body, call_back) {
        var encoded_body = "";
        var en = spawn("./encrypt.py", [
            "-t",
            "encode",
            "-i",
            body,
            "-k",
            "123",
        ]);

        en.stdout.on("data", (d) => {
            encoded_body += d;
        });

        en.on("close", (code) => {
            if (code !== 0) {
                cRes.end("internal error");
                return;
            }
            console.log("encoded: " + encoded_body);
            call_back(encoded_body);
        });
    },
    decode: function (body, call_back) {
        var decoded_body = "";
        var de = spawn("./encrypt.py", [
            "-t",
            "decode",
            "-i",
            body,
            "-k",
            "123",
        ]);

        de.stdout.on("data", (d) => {
            decoded_body += d;
        });

        de.on("close", (code) => {
            if (code !== 0) {
                cRes.end("internal error");
                return;
            }
            console.log("decoded: " + decoded_body);
            call_back(decoded_body);
        });
    },
};
