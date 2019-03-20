from threading import *
from random import randrange
# from time import sleep

MAX = 100
buffer = []
mutex = Semaphore(1)
places = Semaphore(MAX)
articles = Semaphore(0)


class Producteur(Thread):

    @staticmethod
    def produire():
        objet = randrange(0, 100)
        print("Producteur1 : ", objet)
        return objet

    @staticmethod
    def deposer(objet):
        print("Producteur2 : ", objet)
        buffer.append(objet)

    def run(self):
        while True:
            objet = self.produire()
            places.acquire()
            mutex.acquire()
            self.deposer(objet)
            mutex.release()
            articles.release()
            # sleep(2)


class Consommateur(Thread):

    @staticmethod
    def extraire():
        objet = buffer.pop()
        print("Consommateur1 : ", objet)
        return objet

    @staticmethod
    def consommer(objet):
        print("Consommateur2 : ", objet)

    def run(self):
        while True:
            articles.acquire()
            mutex.acquire()
            objet = self.extraire()
            mutex.release()
            places.release()
            self.consommer(objet)
            # sleep(4)


if __name__ == "__main__":
    Consommateur().start()
    Producteur().start()
