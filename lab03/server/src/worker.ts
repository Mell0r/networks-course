import { readFileSync } from "fs";
import { resolve } from "path";
import { parentPort, workerData } from "worker_threads";

function readResource(filename: string): string {
  return readFileSync(`./resources/${filename}`, { encoding: "utf8" });
}

parentPort!.postMessage(readResource(workerData.filename));