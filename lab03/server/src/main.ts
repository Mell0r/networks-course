import express, { Request, Response } from "express";
import { Worker } from "worker_threads";

if (process.argv.length < 4) {
  console.error("Expected at least two arguments!");
  process.exit(1);
}

const port = parseInt(process.argv[2]);
let threadCount = parseInt(process.argv[3]);

const app = express();

app.get("/:filename", (req: Request, res: Response) => {
  console.log(`get file request with name: ${req.params.filename}`);

  while (threadCount === 0) {}
  threadCount--;
  const resultPromise: Promise<string> = new Promise((resolve, reject) => {
    const worker = new Worker("./src/worker/worker.ts", {
      workerData: { filename: req.params.filename },
    });
    worker.on("message", (fileContent) => resolve(fileContent));
    worker.on("error", (err) => reject(err));
    worker.on("exit", (_) => threadCount++);
  });

  resultPromise
    .catch((err) => {
      console.log(err);
      res.status(404).send("File not found");
    })
    .then((content) => res.status(200).send(content));
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
