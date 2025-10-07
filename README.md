[EN](#English-version)

-----

# Fragment API ☄️

> [\!WARNING]
> **Демонстрационный код**: Данный проект является демонстрацией работы больше с блокчейном, чем с фрагментом и был написан в образовательных целях. Он требует доработок для стабильного использования в реальных условиях (продакшене).

Этот скрипт автоматизирует процесс покупки **Telegram Stars** на платформе **Fragment**. Он включает в себя функции для создания и инициализации кошелька TON, а также для выполнения самих транзакций.

Подробный разбор процесса [статье на Lolzteam](https://lolz.live/threads/8785274/).

-----

## 🚀 Возможности

  * **Создание кошелька**: Генерация нового кошелька TON любой поддерживаемой версии (например, `v3r1`, `v3r2`, `v4r2`) с сохранением данных (адрес, мнемоника, ключи) в файл.
  * **Инициализация кошелька**: Развертывание контракта кошелька в сети TON, что необходимо для его активации.
  * **Автоматическая покупка**: Скрипт самостоятельно получает все необходимые данные для платежа (адрес, сумму, payload) и отправляет транзакцию.
  * **Гибкая настройка**: Возможность работы как в основной сети (mainnet), так и в тестовой (testnet).

-----

## ⚙️ Принцип работы

1.  **Получение данных для платежа** (`PaymentGet.py`):
      * Скрипт использует ваши `cookies` для аутентификации на Fragment.
      * Отправляется запрос для получения ID получателя по его `@username`.
      * Инициируется запрос на покупку, в результате которого Fragment предоставляет временный адрес кошелька, точную сумму в TON и специальную полезную нагрузку (`payload`).
2.  **Отправка транзакции** (`Transactions.py`):
      * Используя данные вашего кошелька (из `wallets_data.txt`), скрипт формирует транзакцию.
      * На полученный от Fragment временный адрес отправляется нужная сумма TON с обязательным указанием `payload`.
      * После успешной обработки этой транзакцией сетью TON, Fragment зачисляет "звезды" указанному получателю.

-----

## 🛠️ Установка и настройка

### Шаг 1: Клонирование и установка зависимостей

Сначала скопируйте репозиторий на свой компьютер и установите необходимые библиотеки.

```bash
git clone <URL репозитория>
cd <папка репозитория>
pip install -r requirements.txt
```

### Шаг 2: Создание и настройка кошелька

Скрипт включает утилиты для работы с кошельками.

1.  **Создайте кошелек**. Вы можете использовать встроенную функцию `create_wallet`. Для этого создайте временный файл, например, `generate_wallet.py`, со следующим кодом и запустите его:

    ```python
    # generate_wallet.py
    from wallet.WalletUtils import WalletUtils

    wallet_utils = WalletUtils()
    # Вы можете указать любую версию, например "v3r2" или "v4r2"
    wallet_utils.create_wallet(version="v4r2", save_to_file=True, save_dir="created_wallets/wallets_data.txt")

    print("Кошелек успешно создан! Данные сохранены в created_wallets/wallets_data.txt")
    ```

    После запуска в файле `created_wallets/wallets_data.txt` появятся все данные вашего нового кошелька, включая **мнемоническую фразу**.

2.  **Пополните кошелек**. Скопируйте `wallet_address` из файла и отправьте на него немного TON (например, 1-2 TON) для оплаты комиссий и будущих покупок. **Это обязательный шаг перед инициализацией\!**

### Шаг 3: Инициализация кошелька

Новый кошелек нужно активировать (развернуть его контракт в сети).

1.  **Убедитесь, что кошелек пополнен**.

2.  Создайте еще один временный файл, например `init_wallet.py`, со следующим кодом:

    ```python
    # init_wallet.py
    import json
    from wallet.WalletUtils import WalletUtils

    with open("created_wallets/wallets_data.txt", "r") as f:
        mnemonics = json.load(f)['mnemonics']

    wallet_utils = WalletUtils()
    wallet_utils.init_wallet(mnemonics=mnemonics)
    ```

3.  Запустите его. Если все пройдет успешно, в консоли появится сообщение `Wallet inited!`.

### Шаг 4: Настройка `cookies.json`

Для взаимодействия с API Fragment скрипту нужны ваши сессионные cookie.

1.  Установите в браузер расширение для управления cookie, например, **EditThisCookie**.
2.  Откройте сайт [Fragment](https://fragment.com) и авторизуйтесь через Telegram.
3.  Нажмите на иконку расширения, найдите и скопируйте значения для `stel_dt`, `stel_ssid`, `stel_token` и `stel_ton_token`.
4.  Вставьте эти значения в соответствующие поля в файле `cookies.json`.

-----

## ▶️ Использование

После выполнения всех шагов настройки вы готовы к покупке.

1.  Запустите главный файл:
    ```bash
    python main.py
    ```
2.  Введите имя пользователя получателя (например, `durov`).
3.  Введите желаемое количество "звезд".

Скрипт выведет в консоль информацию о процессе и результат выполнения.

-----

## ⚠️ Важно

  * **Безопасность**: Никогда не делитесь файлами `cookies.json` и `wallets_data.txt` с посторонними. Они содержат данные для доступа к вашему аккаунту и кошельку.
  * **Комиссии**: Убедитесь, что на вашем кошельке достаточно средств для покрытия не только стоимости "звезд", но и сетевой комиссии TON.

-----

# English version

# Fragment API ☄️

> [\!WARNING]
> **Demonstration Code**: This project is more of a demonstration of working with the blockchain than with Fragment itself, and it was created for educational purposes. It requires further refinement for stable use in a real production environment.

This script automates the process of purchasing **Telegram Stars** on the **Fragment** platform. It includes functions for creating and initializing a TON wallet, as well as for executing the transactions themselves.

A detailed breakdown of the code-writing process and its logic can be found in the [article on Lolzteam](https://lolz.live/threads/8785274/) (in Russian).

-----

## 🚀 Features

  * **Wallet Creation**: Generate a new TON wallet of any supported version (e.g., `v3r1`, `v3r2`, `v4r2`) and save its data (address, mnemonics, keys) to a file.
  * **Wallet Initialization**: Deploy the wallet's contract to the TON network, which is necessary for its activation.
  * **Automated Purchase**: The script automatically retrieves all necessary payment data (address, amount, payload) and sends the transaction.
  * **Flexible Configuration**: Ability to operate on both the mainnet and testnet.

-----

## ⚙️ How It Works

1.  **Get Payment Data** (`PaymentGet.py`):
      * The script uses your `cookies` to authenticate on Fragment.
      * A request is sent to get the recipient's ID based on their `@username`.
      * A purchase request is initiated, from which Fragment provides a temporary wallet address, the exact amount in TON, and a special payload.
2.  **Send Transaction** (`Transactions.py`):
      * Using your wallet data (from `wallets_data.txt`), the script creates a transaction.
      * The required amount of TON is sent to the temporary address received from Fragment, with the mandatory `payload` included.
      * After the TON network successfully processes this transaction, Fragment credits the Stars to the specified recipient.

-----

## 🛠️ Installation and Setup

### Step 1: Clone and Install Dependencies

First, clone the repository to your computer and install the necessary libraries.

```bash
git clone <repository URL>
cd <repository folder>
pip install -r requirements.txt
```

### Step 2: Create and Set Up Wallet

The script includes utilities for wallet management.

1.  **Create a wallet**. You can use the built-in `create_wallet` function. Create a temporary file, e.g., `generate_wallet.py`, with the following code and run it:

    ```python
    # generate_wallet.py
    from wallet.WalletUtils import WalletUtils

    wallet_utils = WalletUtils()
    # You can specify any version, e.g., "v3r2" or "v4r2"
    wallet_utils.create_wallet(version="v4r2", save_to_file=True, save_dir="created_wallets/wallets_data.txt")

    print("Wallet created successfully! Data saved to created_wallets/wallets_data.txt")
    ```

    After running, the `created_wallets/wallets_data.txt` file will contain all your new wallet's data, including the **mnemonic phrase**.

2.  **Fund your wallet**. Copy the `wallet_address` from the file and send some TON to it (e.g., 1-2 TON) to cover fees and future purchases. **This is a mandatory step before initialization\!**

### Step 3: Initialize Wallet

A new wallet needs to be activated (its contract deployed on the network).

1.  **Ensure the wallet is funded**.

2.  Create another temporary file, e.g., `init_wallet.py`, with the following code:

    ```python
    # init_wallet.py
    import json
    from wallet.WalletUtils import WalletUtils

    with open("created_wallets/wallets_data.txt", "r") as f:
        mnemonics = json.load(f)['mnemonics']

    wallet_utils = WalletUtils()
    wallet_utils.init_wallet(mnemonics=mnemonics)
    ```

3.  Run it. If successful, you will see the message `Wallet inited!` in the console.

### Step 4: Configure `cookies.json`

The script needs your session cookies to interact with the Fragment API.

1.  Install a cookie management extension in your browser, such as **EditThisCookie**.
2.  Go to the [Fragment](https://fragment.com) website and log in via Telegram.
3.  Click the extension's icon, find and copy the values for `stel_dt`, `stel_ssid`, `stel_token`, and `stel_ton_token`.
4.  Paste these values into the corresponding fields in the `cookies.json` file.

-----

## ▶️ Usage

After completing all setup steps, you are ready to make a purchase.

1.  Run the main file:
    ```bash
    python main.py
    ```
2.  Enter the recipient's username (e.g., `durov`).
3.  Enter the desired amount of Stars.

The script will output information about the process and the result to the console.

-----

## ⚠️ Important

  * **Security**: Never share your `cookies.json` and `wallets_data.txt` files with anyone. They contain access credentials to your account and wallet.
  * **Fees**: Ensure you have enough funds in your wallet to cover not only the cost of the Stars but also the TON network fees.
