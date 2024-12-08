# Задание №2 Индивидуальный вариант №19
## Постановка задачи

Разработать инструмент командной строки для визуализации графа
зависимостей, включая транзитивные зависимости. Сторонние средства для
получения зависимостей использовать нельзя.
Зависимости определяются для git-репозитория. Для описания графа
зависимостей используется представление Mermaid. Визуализатор должен
выводить результат на экран в виде графического изображения графа.
Построить граф зависимостей для коммитов, в узлах которого находятся
списки файлов и папок. Граф необходимо строить только для коммитов ранее
заданной даты.

Ключами командной строки задаются:

• Путь к программе для визуализации графов.

• Путь к анализируемому репозиторию.

• Дата коммитов в репозитории.

## Описание функций, используемых для моделирования работы строки

• Функция get_commit_history принимает путь к репозиторию и дату в виде объекта datetime, после чего извлекает историю коммитов, выполненных до указанной даты, с помощью команды Git. Она возвращает список кортежей, где каждый элемент содержит хэш коммита, сообщение коммита и список затронутых файлов. Если возникают ошибки при выполнении команды, выводится соответствующее сообщение, а функция возвращает пустой список.

• Функция build_mermaid_graph строит текстовое представление графа зависимостей коммитов в формате Mermaid. Она принимает список коммитов и создает вершины для каждого коммита с указанием сообщения и связей между последовательными коммитами. Результат возвращается в виде строки, которая может быть сохранена в файл для визуализации.

• Функция save_mermaid_file сохраняет текстовое представление графа в формате Mermaid в указанный файл. Она принимает текст графа и путь к файлу, после чего записывает данные в файл с использованием кодировки UTF-8.

• Функция display_graph отвечает за отображение графа в виде изображения. Она принимает путь к файлу Mermaid и путь к инструменту для генерации графа (Mermaid CLI). Функция запускает процесс генерации изображения, сохраняет его в файл формата PNG и открывает его с помощью стандартного просмотрщика. Если возникают ошибки при генерации, выводится сообщение об ошибке.

• Функция main организует основной поток выполнения программы. Она обрабатывает аргументы командной строки, проверяет корректность введённых путей к инструменту визуализации и репозиторию, парсит указанную дату, извлекает историю коммитов, создает граф в формате Mermaid, сохраняет его в файл и вызывает функцию отображения графа.

## Запуск программы
 
py Graph.py --viz <путь_к_mermaid_cli> --repo <путь_к_репозиторию> --date <дата_в_формате_YYYY-MM-DD>

## Тестики

Обычный

![image](https://github.com/user-attachments/assets/3315d697-0966-45dd-8fb2-d962951584fb)

С датой

![image](https://github.com/user-attachments/assets/288c39c6-335f-4f5d-af99-454a604d9913)

С не очень датой

![image](https://github.com/user-attachments/assets/a330cc48-b862-404c-bd82-5034cc9866e5)

дата +-

![image](https://github.com/user-attachments/assets/ad13a174-7aec-43a5-9888-85ceae0f9452)






