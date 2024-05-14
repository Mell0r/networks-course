import { createTransport } from "nodemailer";
import { exit } from "process";

const fromAccount = process.argv[2];
const toAccount = process.argv[3];
const appAccessCode = process.argv[4];
const subject = process.argv[5];
const messageType = process.argv[6];
if (messageType !== "html" && messageType !== "text") {
  console.error(`Message type (5th argument) should be html or text.`);
  exit(1);
}
const message = process.argv[7];

const transporter = createTransport({
  host: "smtp.gmail.com",
  port: 587,
  secure: false, // Use `true` for port 465, `false` for all other ports
  auth: {
    user: fromAccount,
    pass: appAccessCode,
  },
});

// send mail with defined transport object
transporter
  .sendMail({
    from: fromAccount, // sender address
    to: toAccount, // list of receivers
    subject: subject, // Subject line
    text: messageType === "text" ? message : undefined, // plain text body
    html: messageType === "html" ? message : undefined, // html body
  })
  .then((info) => console.log("Message sent: %s", info.messageId))
  .catch(console.error);
