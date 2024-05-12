import express, { Request, Response } from "express";
import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "fs";

const cacheDirPath = "./cache";
const blacklistPath = "./blacklist.txt";

interface cacheMetadata {
  cacheFilename: string;
  lastModified?: string;
  etag?: string;
}

function genRandomFilename() {
  return Math.floor(Math.random() * 1_000_000_000).toString() + ".txt";
}

const port = parseInt(process.argv[2]) || 8080;

if (!existsSync(cacheDirPath)) {
  rmSync(cacheDirPath, { recursive: true, force: true });
  mkdirSync(cacheDirPath);
}
const blacklist = readFileSync(blacklistPath)
  .toString()
  .split(/[\r\n]+/);
console.log(`loaded blacklist:`);
console.log(blacklist);

const cacheMetadataMap: Map<string, cacheMetadata> = new Map();

const app = express();
app.use(express.text());

function handlePath(method: "GET" | "POST") {
  return (request: Request, response: Response) => {
    const url = request.originalUrl.substring(1);
    console.log(`proxy ${method} request on: ${url}`);
    
    if (blacklist.includes(url)) {
      console.log("Blacklist reject");
      response.status(403).send("This site is in the blacklist");
      return;
    }

    const cacheMetadata = cacheMetadataMap.get(url);
    console.log(`cache metadata on this adress:`);
    console.log(cacheMetadata);
    let headers =
      cacheMetadata?.lastModified && cacheMetadata?.etag
        ? {
            "If-Modified-Since": cacheMetadata.lastModified,
            "If-None-Match": cacheMetadata.etag,
          }
        : undefined;
    let body = method === "POST" ? request.body : undefined;
    const fetchPromise = fetch(`http://${url}`, {
      method: method,
      headers: headers,
      body: body,
    });

    fetchPromise
      .then(async (fetchResponse) => {
        console.log(`fetch returned status ${fetchResponse.status}`);
        const cacheFilename =
          cacheMetadataMap.get(url)?.cacheFilename ?? genRandomFilename();

        if (fetchResponse.ok) {
          console.log(`Got new 2.. response, updating local cache`);

          const lastModified = fetchResponse.headers.get("Last-Modified");
          const etag = fetchResponse.headers.get("ETag");
          if (lastModified && etag) {
            cacheMetadataMap.set(url, {
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
  };
}

app.get("*", handlePath("GET"));

app.post("*", handlePath("POST"));

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
