# Wyniki WF

Aplikacja umożliwia zarządzanie wynikami z przedmiotu wychowania fizycznego.
Pozwala na podstawowe operacje na danych (dla nauczyciela), oraz na wyświetlanie swoich wyników (dla ucznia).
Dostęp do aplikacji jest przyznawany poprzez zalogowanie

## Uruchomienie
1. Sklonuj repozytorium:
    ```shell script
    $ git clone https://github.com/marcinadd/django-wf.git
    ```
1. Przejdź do katalogu sklonowanej aplikacji:
    ```shell script
   $ cd django-wf/
   ```
1. Utwórz i aktywuj wirtualne środowisko:
   ```shell script
    $ python3 -m venv pve3
    $ source pve3/bin/activate    
   ```
1. Zainstaluj wymagane zależności:
    ```shell script
   $ pip install -r requirements.txt
    ```
1. Wykonaj migracje:
    ```shell script
   $ python manage.py migrate
   ```
1. Utwórz konto administratora:
    ```shell script
   $ python manage.py createsuperuser
   ```
1. Uruchom serwer deweloperski: 
    ```shell script
   $ python manage.py runserver
   ```
## Uruchomienie testów
Aby uruchomić testy w katalogu głównym repozytorium wywołaj polecenie: 
   ```shell script
   $ python manage.py test 
   ```
## Konfiguracja
* Dodawanie i podgląd informacji wymaga zalogowania jako superużytkownik 
 (na konto utworzone w pkt.7 instrukcji uruchomienia projektu) pod adresem:
    ```
    http://localhost:8000/admin
    ```
* Do aplikacji należy logować się przez konta Google w domenie szkolnej, lecz należy pierw uzupełnić **client_id** i **secret**
w *fixtures/allauth.json* i wydać polecenie: 
    ```shell script
    $ python manage.py loaddata fixtures/allauth.json
    ```
  Wartości te można uzyskać tworząc **Identyfikator klienta OAuth** na stronie https://console.developers.google.com

    Domyślnie każdy zalogowany użytkownik jest traktowany jako uczeń (ma możliwość oglądania tylko swoich wyników), aby
    dodać możliwość zmiany i wyświetlania wszystkich danych, należy mianować użytkownika na 
    superużytkownika w panelu administracyjnym. Teraz użytkownik (nauczyciel) może logować się ze swojego konta Google.
 
## Przykładowe dane
Aby wczytać przykładowe dane należy wydać polecenie:
```shell script
$ python manage.py loaddata fixtures/example_data.json
```

## Twórcy
* marcinadd
* marcins1
* inari6735
   
