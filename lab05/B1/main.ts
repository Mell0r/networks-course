import { exec } from "child_process";
import { createServer } from "net";

const PORT = 8080;

const server = createServer((socket) => {
  console.log("Client connected.");

  socket.on("data", (data) => {
    const command = data.toString().trim();
    console.log(`Accepted command to run: ${command}`);

    // Execute the command and send the output back to the client
    exec('hostname', (error, stdout, stderr) => {
      if (error) {
        console.log(`exception: ${error.message}`)
        socket.write(`Exception executing command: ${error.message}`);
      }
      if (stderr) {
        console.log(`Stderr: ${stderr}`)
        socket.write(`Stderr:\n${stderr}`);
      }
      if (stdout) {
        console.log(`Stdout: ${stdout}`)
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
