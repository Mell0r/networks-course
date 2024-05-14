"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const nodemailer_1 = require("nodemailer");
const process_1 = require("process");
const fromAccount = process.argv[2];
const toAccount = process.argv[3];
const appAccessCode = process.argv[4];
const subject = process.argv[5];
const messageType = process.argv[6];
if (messageType !== "html" && messageType !== "text") {
    console.error(`Message type (5th argument) should be html or text.`);
    (0, process_1.exit)(1);
}
const message = process.argv[7];
const transporter = (0, nodemailer_1.createTransport)({
    host: "smtp.gmail.com",
    port: 587,
    secure: false,
    auth: {
        user: fromAccount,
        pass: appAccessCode,
    },
});
// send mail with defined transport object
transporter
    .sendMail({
    from: fromAccount,
    to: toAccount,
    subject: subject,
    text: messageType === "text" ? message : undefined,
    html: messageType === "html" ? message : undefined, // html body
})
    .then((info) => console.log("Message sent: %s", info.messageId))
    .catch(console.error);
