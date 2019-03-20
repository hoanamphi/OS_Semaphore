from threading import *
from random import randrange


class Buffer:

    def __init__(self, maxi):
        self.maximum = maxi
        self.queue = []

    def push(self, objet):
        if len(self.queue) == self.maximum:
            raise IndexError("The buffer is already full")
        self.queue.append(objet)

    def pop(self):
        return self.queue.pop()


MAX = 100
buffer = Buffer(MAX)
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
        buffer.push(objet)

    def run(self):
        while True:
            objet = self.produire()
            places.acquire()
            mutex.acquire()
            self.deposer(objet)
            mutex.release()
            articles.release()


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


if __name__ == "__main__":
    Consommateur().start()
    Producteur().start()
