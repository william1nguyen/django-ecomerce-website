# Ecompera
![Uploading Screenshot 2024-04-22 at 22.03.43.png…]()

## Introduction

- A fullstack open-source ecommerce website.

## Architechture

- We use `Django` framework for the **Backend Server** and host `HTML, CSS, JS` for **Clients**.

## Install and Setup on local

### Install

> **Optional** Fork this project for customization development.

- Thanks to the publication of the repo, you can clone it.
  ```
  $ git clone https://github.com/natalieconan/ecompera.git
  ```

### Setup project on local

- Setup virtual environment (For this project, I use `pipenv`) and install required packages.

  ```
  $ pipenv shell
  $ pipenv install
  ```

- Create file `.env` from `.env.example`.

  ```
  $ cp .env.example .env
  ```

  > **Optional** Change `SECRET_KEY` inorder to enhance security.

- Create **SuperUser**.

  ```
  $ python manage.py createsuperuser
  ```

- Apply **Migration**.

  ```
  $ python manage.py migrate
  ```

- Finally, run this application.
  ```
  $ python manage.py runserver
  ```
