import { createTransport } from 'nodemailer';

const fromAccount = 'jazzman0303@gmail.com';

const transporter = createTransport({
  host: 'smtp.gmail.com',
  port: 587,
  secure: false, // Use `true` for port 465, `false` for all other ports
  auth: {
    user: fromAccount,
    pass: 'ypscejyuondrbmub',
  },
});

export function sendGreetings(email: string) {
  transporter
    .sendMail({
      from: fromAccount,
      to: email,
      subject: 'Greetings!',
      text: 'Рады видеть вас в нашем сервисе вновь!',
    })
    .then((info) => console.log('Message sent: %s', info.messageId))
    .catch(console.error);
}
