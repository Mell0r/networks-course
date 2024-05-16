import { createConnection } from "net";

const port = 8080;
const host = "localhost";

const client = createConnection({ port, host }, () => {
  console.log("Connected to server! Sending 'hostname'.");

  client.write("hostname");
  client.on("data", (data) => {
    console.log(`Received data from server: ${data}`);
    client.end();
  });
});

client.on("end", () => {
  console.log("Connection closed.");
});
