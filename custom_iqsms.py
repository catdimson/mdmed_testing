import urllib.request as urllib2
import urllib


class Gate:
    """class for using iqsms.ru service via GET requests"""

    __host = 'gate.iqsms.ru'

    def __init__(self, api_login, api_password):
        self.login = api_login
        self.password = api_password

    def __sendRequest(self, uri, params=None):
        url = self.__getUrl(uri, params)
        request = urllib2.Request(url)
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, url, self.login, self.password)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        try:
            opener = urllib2.build_opener(authhandler)
            data = opener.open(request).read()
            return data
        except Exception as e:
            return e.code

    def __getUrl(self, uri, params=None):
        url = "https://%s/%s/" % (self.getHost(), uri)
        paramStr = ''
        clear_params = {}
        if params is not None:
            for k, v in params.items():
                if v is not None:
                    clear_params[k] = params[k]
            paramStr = urllib.parse.urlencode(clear_params)
        return "%s?%s" % (url, paramStr)

    def getHost(self):
        """Return current requests host """
        return self.__host

    def setHost(self, host):
        """Changing default requests host """
        self.__host = host

    def send(self, phone, text, sender='iqsms',
             statusQueueName=None, scheduleTime=None, wapurl=None):
        """Sending sms """
        params = {'phone': phone,
                  'text': text,
                  'sender': sender,
                  'statusQueueName': statusQueueName,
                  'scheduleTime': scheduleTime,
                  'wapurl': wapurl
                  }
        return self.__sendRequest('send', params)

    def status(self, id):
        """Retrieve sms status by it's id """
        params = {'id': id}
        return self.__sendRequest('status', params)

    def statusQueue(self, statusQueueName, limit=5):
        """Retrieve latest statuses from queue """
        params = {'statusQueueName': statusQueueName, 'limit': limit}
        return self.__sendRequest('statusQueue', params)

    def credits(self):
        """Retrieve current credit balance """
        return self.__sendRequest('credits')

    def senders(self):
        """Retrieve available signs """
        return self.__sendRequest('senders')


if __name__ == "__main__":
    print(Gate.__doc__)
    print('***' * 5)
    login, password = input('Введите login: '), input('Введите пароль: ')
    text, phone = input('Введите текст сообщения: '), input('Введите номер получателя (в формате 79998886655: ')
    iqsms = Gate(login, password)
    senders = str(iqsms.senders()).replace("b", "").replace("\'", "").split("\\n")
    print("Доступные подписи отправителя: ")
    for i in range(len(senders)):
        print(f"{i+1}: {senders[i]}")
    sender = senders[int(input(f"Выберите номер доступной подписи отправителя: ")) - 1]

    iqsms.send(phone, text, sender=sender)  # отправляем sms
    print(iqsms.status(sender))

