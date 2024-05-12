import express, { Request, Response } from "express";
import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "fs";

interface cacheMetadata {
  cacheFilename: string;
  lastModified?: string;
  etag?: string;
}

function genRandomFilename() {
  return Math.floor(Math.random() * 1_000_000_000).toString() + ".txt";
}

const port = parseInt(process.argv[2]) || 8080;
const cacheDirPath = "./cache";

if (!existsSync(cacheDirPath)) {
  rmSync(cacheDirPath, { recursive: true, force: true });
  mkdirSync(cacheDirPath);
}

const cacheMetadataMap: Map<string, cacheMetadata> = new Map();

const app = express();

app.get("*", (request: Request, response: Response) => {
  console.log(`proxy request on: ${request.originalUrl}`);

  const cacheMetadata = cacheMetadataMap.get(request.originalUrl);
  console.log(`cache metadata on this adress:`);
  console.log(cacheMetadata);
  const fetchPromise =
    cacheMetadata?.lastModified && cacheMetadata?.etag
      ? fetch(`http://${request.originalUrl}`, {
          headers: {
            "If-Modified-Since": cacheMetadata.lastModified,
            "If-None-Match": cacheMetadata.etag,
          },
        })
      : fetch(`http://${request.originalUrl}`);

  fetchPromise
    .then(async (fetchResponse) => {
      console.log(`fetch returned status ${fetchResponse.status}`);
      const cacheFilename =
        cacheMetadataMap.get(request.originalUrl)?.cacheFilename ??
        genRandomFilename();

      if (fetchResponse.ok) {
        console.log(`Got new 2.. response, updating local cache`);

        const lastModified = fetchResponse.headers.get("Last-Modified");
        const etag = fetchResponse.headers.get("ETag");
        if (lastModified && etag) {
          cacheMetadataMap.set(request.originalUrl, {
            cacheFilename: cacheFilename,
            lastModified: lastModified,
            etag: etag,
          });
        }

        const content = await fetchResponse.text();

        writeFileSync(`${cacheDirPath}/${cacheFilename}`, content);
      }

      if (fetchResponse.status === 304)
        console.log("Got 304 response, sending data from cache.");

      if (fetchResponse.ok || fetchResponse.status === 304) {
        const content = readFileSync(`${cacheDirPath}/${cacheFilename}`);
        response.status(200).send(content.toString());
      } else {
        response
          .status(fetchResponse.status)
          .send(`Error returned on fetch: ${fetchResponse.statusText}`);
      }
    })
    .catch((err) => {
      console.error(err);
      response.status(500).send(`Internal server error on fetch: ${err}`);
    });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
