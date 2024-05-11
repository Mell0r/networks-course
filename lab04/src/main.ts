import express, { Request, Response } from "express";

const port = parseInt(process.argv[2]) || 8080;

const app = express();
// app.use(express.json());

app.get("*", (request: Request, response: Response) => {
  console.log(`proxy request on: ${request.originalUrl}`);
  fetch(`http://${request.originalUrl}`)
    .then(
      // async (fetchResponse) => {
      // if (!fetchResponse.ok) {
      //   response
      //     .status(fetchResponse.status)
      //     .send(`GET returned an error: ${fetchResponse.statusText}`);
      // } else {
      //   const contentReader = fetchResponse.body?.getReader();
      //   if (!contentReader) {
      //     console.log("there is no body reader in fetch response");
      //     response.status(200);
      //     return;
      //   }
      //   let part = await contentReader.read();
      //   response.status(200);
      //   console.log("proxied chunks: ");
      //   while (!part.done) {
      //     console.log(part);
      //     response.write(part?.value);
      //     part = await contentReader.read();
      //   }
      //   response.end();
      // }}

      (fetchResponse) => {
        fetchResponse.text().then((content) => {
          console.log(content);
          response.status(200).send(content);
        });
      }
    )
    .catch((err) => {
      console.error(err);
      response.status(500).send(`Internal server error on fetch: ${err}`);
    });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
