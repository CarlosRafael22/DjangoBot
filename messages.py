

class ModelsComposite:

    def __init__(self):
        self.models = []

    def add_model(self, model):
        self.models.append(model)

    def save_all(self):

        for model in self.models:
            model.save()


class MessageBase(object):

    def __init__(self, text, contents=ModelsComposite()):
        self._text = text
        self.contents = contents

    def get_text(self):
        return self._text


class MessageHelloName(MessageBase):

    def __init__(self, first_name):
        text = 'Oi,{0}! Tudo bem?'
        self._first_name = first_name
        MessageBase.__init__(self, text)

    def get_text(self):
        return self._text.format(self._first_name)


class MessageSayHi(MessageBase):

    def __init__(self):
        text = 'Diga "Oi" para registrar informações no seu diário.'
        MessageBase.__init__(self, text)


class MessageSorry(MessageBase):

    def __init__(self):
        text = 'Desculpa, ainda sou limitado =/. Qualquer dúvida fale com seu coach.'
        MessageBase.__init__(self, text)


class MessageWhatRegister(MessageBase):

    def __init__(self):
        text = 'O que você deseja registrar?'

        MessageBase.__init__(self, text)






