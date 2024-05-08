if (process.argv.length < 5) {
  console.error("Expected at least three argument!");
  process.exit(1);
}

const serverHost = process.argv[2];
const serverPort = process.argv[3];
const filename = process.argv[4];

fetch(`http://${serverHost}:${serverPort}/${filename}`)
  .then((response) =>
    response
      .text()
      .catch((err) => console.error(`error on request: ${err}`))
      .then((content) => console.log(content))
  )
  .catch((err) => console.error(err));
