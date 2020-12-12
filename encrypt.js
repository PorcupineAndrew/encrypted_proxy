const { spawn, spawnSync } = require("child_process");

module.exports = {
    encode: function (body, pkey, skey, call_back) {
        var encoded_body = "";
        var en = spawn("./encrypt.py", [
            "-t",
            "encode",
            "-i",
            body,
            "-p",
            pkey,
            "-s",
            skey,
        ]);

        en.stdout.on("data", (d) => {
            encoded_body += d;
        });

        en.stderr.on("data", (d) => {
            console.log(d.toString());
        });

        en.on("close", (code) => {
            call_back(encoded_body, code);
        });
    },

    decode: function (body, pkey, skey, call_back) {
        var decoded_body = "";
        var de = spawn("./encrypt.py", [
            "-t",
            "decode",
            "-i",
            body,
            "-p",
            pkey,
            "-s",
            skey,
        ]);

        de.stdout.on("data", (d) => {
            decoded_body += d;
        });

        de.stderr.on("data", (d) => {
            console.log(d.toString());
        });

        de.on("close", (code) => {
            call_back(decoded_body, code);
        });
    },

    load: function (ctx, callback) {
        var data = "";
        ctx.on("data", (d) => {
            data += d;
            if (data.length > 1e7) {
                ctx.end("Error 413");
            }
        });
        ctx.on("end", () => {
            callback(data);
        });
    },
};
