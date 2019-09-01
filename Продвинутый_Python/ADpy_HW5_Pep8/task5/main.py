from task5.MailWorker import MailWorker

yandexMailWorker = MailWorker('python-tst@yandex.ru', 'A!b2c3D4', 'smtp.yandex.ru', 465, 'imap.yandex.ru', 993)
yandexMailWorker.send_mail(['ivan.v.konstantinov@gmail.com'], 'Проверка работы программы', 'Тут тело письма')
