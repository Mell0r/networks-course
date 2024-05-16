"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const child_process_1 = require("child_process");
const net_1 = require("net");
const PORT = 8080;
const server = (0, net_1.createServer)((socket) => {
    console.log("Client connected.");
    socket.on("data", (data) => {
        const command = data.toString().trim();
        console.log(`Accepted command to run: ${command}`);
        // Execute the command and send the output back to the client
        (0, child_process_1.exec)('hostname', (error, stdout, stderr) => {
            if (error) {
                console.log(`exception: ${error.message}`);
                socket.write(`Exception executing command: ${error.message}`);
            }
            if (stderr) {
                console.log(`Stderr: ${stderr}`);
                socket.write(`Stderr:\n${stderr}`);
            }
            if (stdout) {
                console.log(`Stdout: ${stdout}`);
                socket.write(`Stdout:\n${stdout}`);
            }
        });
    });
    socket.on("end", () => {
        console.log("Client disconnected.");
    });
});
server.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}`);
});
