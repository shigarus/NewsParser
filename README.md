# NewsParser
Parse usefull info from default news site to *.txt

Задача:

Создать инструмент для извлечения текстов статей из новостных сайтов. Под новостными сайтами понимаются любые сайты, которые содержат обьемные статьи на любые темы, т.е. непосредственно новостные сайты, блоги и т.п.

Формат инструмента: скрипт с консольным интерфейсом.

Формат вывода: *.txt файлы, соответствующие url, вида http://default.ru/news/2013/03/dtp/index.html => [CUR_DIR]/default.ru/news/2013/03/dtp/index.txt.

Формат *.txt файла: ширина строки 80 символов, перенос по словам, абзацы и заголовки отделяются пустой строкой. Url, имеющий текстовое представление, записывается в виде \<текстовое представление \[url]>

Подробное описание в файле description.txt
