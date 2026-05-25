import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8411682585:AAHqVyye_GW84cTR_gmpQXnCvoSAdOZFrSQ"

CHOOSE_CATEGORY, CHOOSE_MODE, ANSWERING_QUESTION, VIEW_RESULTS = range(4)

CATEGORY_NAMES = {
    "languages": "📚 Языки программирования",
    "networks": "🌐 Сети, браузеры, серверы",
    "visual": "🎨 Визуальные языки и цвета",
    "variables": "🔢 Переменные и синтаксис",
}

user_data = {}

QUESTIONS_DATABASE = {
    "languages": [
        # 1-10: JavaScript
        {"question": "В каком году был создан язык программирования JavaScript?", "options": ["1993", "1995", "1997", "2000"], "correct": 1, "explanation": "JavaScript создан в 1995 году Бренданом Айком в компании Netscape."},
        {"question": "Кто создал язык программирования JavaScript?", "options": ["Гвидо ван Россум", "Бьёрн Страуструп", "Брендан Айк", "Джеймс Гослинг"], "correct": 2, "explanation": "JavaScript создал Брендан Айк (Brendan Eich) в 1995 году."},
        {"question": "В какой компании был разработан JavaScript?", "options": ["Microsoft", "Google", "Netscape", "Sun Microsystems"], "correct": 2, "explanation": "JavaScript был разработан в компании Netscape Communications."},
        {"question": "Какой тип языка является JavaScript?", "options": ["Компилируемый статически типизированный", "Интерпретируемый динамически типизированный", "Байт-кодовый", "Ассемблерный"], "correct": 1, "explanation": "JavaScript — интерпретируемый, динамически типизированный язык программирования."},
        {"question": "Что расшифровывается аббревиатура DOM в JavaScript?", "options": ["Data Object Model", "Document Object Model", "Dynamic Object Method", "Desktop Object Manager"], "correct": 1, "explanation": "DOM — Document Object Model (объектная модель документа)."},
        {"question": "Какой метод используется для вывода сообщения в консоль в JavaScript?", "options": ["print()", "System.out.println()", "console.log()", "echo()"], "correct": 2, "explanation": "В JavaScript для вывода в консоль используется console.log()."},
        {"question": "Какой стандарт определяет современный JavaScript?", "options": ["W3C", "ECMAScript", "WHATWG", "ISO/IEC"], "correct": 1, "explanation": "JavaScript стандартизирован как ECMAScript (ECMA-262)."},
        {"question": "Какой тип данных НЕ существует в JavaScript?", "options": ["undefined", "null", "integer", "boolean"], "correct": 2, "explanation": "В JavaScript нет отдельного типа integer — числа представлены типом number."},
        {"question": "Что делает оператор === в JavaScript?", "options": ["Присваивает значение", "Сравнивает только значения", "Сравнивает значение и тип", "Логическое И"], "correct": 2, "explanation": "=== — строгое равенство, проверяет совпадение значения И типа данных."},
        {"question": "Какое ключевое слово используется для объявления переменной в современном JavaScript?", "options": ["var и только var", "let и const", "dim", "define"], "correct": 1, "explanation": "В современном JS рекомендуется использовать let (изменяемые) и const (константы)."},
        # 11-20: Python
        {"question": "В каком году был создан язык программирования Python?", "options": ["1985", "1989", "1993", "1998"], "correct": 1, "explanation": "Python создан в 1989 году Гвидо ван Россумом (первый релиз в 1991)."},
        {"question": "Кто создал язык программирования Python?", "options": ["Брендан Айк", "Гвидо ван Россум", "Ларри Уолл", "Юкихиро Мацумото"], "correct": 1, "explanation": "Python создал Гвидо ван Россум (Guido van Rossum)."},
        {"question": "Откуда произошло название языка Python?", "options": ["От змеи питон", "От британского комедийного шоу Monty Python", "От греческого слова мудрость", "От имени создателя"], "correct": 1, "explanation": "Python назван в честь британского комедийного шоу Monty Python's Flying Circus."},
        {"question": "Что используется в Python для обозначения блоков кода?", "options": ["Фигурные скобки {}", "Ключевые слова begin/end", "Отступы (indentation)", "Круглые скобки ()"], "correct": 2, "explanation": "В Python блоки кода определяются отступами (indentation), а не скобками."},
        {"question": "Как называется менеджер пакетов Python?", "options": ["npm", "pip", "gem", "cargo"], "correct": 1, "explanation": "pip — стандартный менеджер пакетов для Python."},
        {"question": "Какое расширение имеют файлы Python?", "options": [".py", ".python", ".pt", ".pyt"], "correct": 0, "explanation": "Файлы Python имеют расширение .py."},
        {"question": "Что такое PEP 8 в Python?", "options": ["Версия Python 8.0", "Руководство по стилю кода Python", "Модуль для работы с сетью", "Встроенная функция"], "correct": 1, "explanation": "PEP 8 — руководство по стилю написания кода на Python."},
        {"question": "Какая функция используется для получения длины списка в Python?", "options": ["size()", "length()", "len()", "count()"], "correct": 2, "explanation": "Функция len() возвращает длину объекта в Python."},
        {"question": "Что такое list comprehension в Python?", "options": ["Встроенная функция сортировки", "Компактный способ создания списков", "Тип данных", "Метод класса"], "correct": 1, "explanation": "List comprehension — компактный синтаксис для создания списков: [x for x in range(10)]."},
        {"question": "Какой тип данных в Python является неизменяемым (immutable)?", "options": ["list", "dict", "set", "tuple"], "correct": 3, "explanation": "tuple (кортеж) является неизменяемым типом данных в Python."},
        # 21-30: PHP
        {"question": "Как изначально расшифровывалась аббревиатура PHP?", "options": ["Professional Hypertext Processor", "Personal Home Page", "PHP: Hypertext Preprocessor", "Public Hypertext Platform"], "correct": 1, "explanation": "PHP изначально означало Personal Home Page, сейчас — рекурсивная аббревиатура PHP: Hypertext Preprocessor."},
        {"question": "Кто создал язык PHP?", "options": ["Расмус Лердорф", "Брендан Айк", "Гвидо ван Россум", "Линус Торвальдс"], "correct": 0, "explanation": "PHP создал Расмус Лердорф (Rasmus Lerdorf) в 1995 году."},
        {"question": "В каком году был создан PHP?", "options": ["1993", "1994", "1995", "1997"], "correct": 2, "explanation": "PHP был создан в 1994-1995 году Расмусом Лердорфом."},
        {"question": "С какого символа начинаются переменные в PHP?", "options": ["#", "@", "$", "%"], "correct": 2, "explanation": "В PHP все переменные начинаются с символа $."},
        {"question": "Какой из следующих вариантов является правильным тегом для начала PHP кода?", "options": ["<php>", "<?php", "<script php>", "<%php"], "correct": 1, "explanation": "Правильный открывающий тег для PHP кода — <?php."},
        {"question": "Для чего преимущественно используется PHP?", "options": ["Разработка мобильных приложений", "Серверная веб-разработка", "Системное программирование", "Машинное обучение"], "correct": 1, "explanation": "PHP — серверный язык программирования, преимущественно используется для веб-разработки."},
        {"question": "Какая функция в PHP используется для вывода текста?", "options": ["print_text()", "output()", "echo", "display()"], "correct": 2, "explanation": "В PHP для вывода используются echo и print."},
        {"question": "Что делает функция strlen() в PHP?", "options": ["Создаёт строку", "Возвращает длину строки", "Конкатенирует строки", "Удаляет строку"], "correct": 1, "explanation": "strlen() возвращает длину строки в PHP."},
        {"question": "Как называется популярная CMS, написанная на PHP?", "options": ["Django", "Rails", "WordPress", "Laravel"], "correct": 2, "explanation": "WordPress — наиболее популярная CMS, написанная на PHP."},
        {"question": "Какой оператор используется для конкатенации строк в PHP?", "options": ["+", "&", ".", "||"], "correct": 2, "explanation": "В PHP конкатенация строк выполняется с помощью оператора точки (.)."},
        # 31-40: Java
        {"question": "В каком году был создан язык Java?", "options": ["1991", "1995", "1998", "2000"], "correct": 1, "explanation": "Java был выпущен в 1995 году компанией Sun Microsystems."},
        {"question": "Кто создал язык Java?", "options": ["Бьёрн Страуструп", "Джеймс Гослинг", "Брендан Айк", "Гвидо ван Россум"], "correct": 1, "explanation": "Java создал Джеймс Гослинг (James Gosling) в Sun Microsystems."},
        {"question": "Что означает принцип Java Write Once Run Anywhere?", "options": ["Код пишется один раз и не изменяется", "Скомпилированный код запускается на любой платформе с JVM", "Один разработчик может написать всё приложение", "Код запускается без компиляции"], "correct": 1, "explanation": "WORA означает, что скомпилированный байт-код Java запускается на любой платформе, где установлена JVM."},
        {"question": "Что такое JVM?", "options": ["Java Virtual Machine", "Java Variable Method", "Java Version Manager", "Java Visual Module"], "correct": 0, "explanation": "JVM — Java Virtual Machine, виртуальная машина, исполняющая байт-код Java."},
        {"question": "Какое расширение имеют скомпилированные файлы Java?", "options": [".java", ".class", ".jar", ".jvm"], "correct": 1, "explanation": "Скомпилированные файлы Java имеют расширение .class (байт-код)."},
        {"question": "Какая компания изначально создала Java?", "options": ["Microsoft", "Oracle", "Sun Microsystems", "IBM"], "correct": 2, "explanation": "Java была создана в Sun Microsystems (впоследствии приобретена Oracle)."},
        {"question": "Какая концепция НЕ относится к ООП в Java?", "options": ["Наследование", "Инкапсуляция", "Полиморфизм", "Процедурность"], "correct": 3, "explanation": "Процедурность — не концепция ООП. ООП включает инкапсуляцию, наследование, полиморфизм, абстракцию."},
        {"question": "Что такое JDK в Java?", "options": ["Java Desktop Kit", "Java Development Kit", "Java Dynamic Kernel", "Java Data Key"], "correct": 1, "explanation": "JDK — Java Development Kit, набор инструментов разработчика Java."},
        {"question": "Как в Java называется родительский класс всех классов?", "options": ["Base", "Super", "Object", "Root"], "correct": 2, "explanation": "Класс Object является родительским для всех классов в Java."},
        {"question": "Какой фреймворк наиболее популярен для разработки на Java?", "options": ["Django", "Rails", "Spring", "Laravel"], "correct": 2, "explanation": "Spring — наиболее популярный фреймворк для Java-разработки."},
        # 41-50: TypeScript, Go, C#
        {"question": "В каком году был создан TypeScript?", "options": ["2010", "2012", "2014", "2016"], "correct": 1, "explanation": "TypeScript выпущен Microsoft в 2012 году."},
        {"question": "Кто создал TypeScript?", "options": ["Брендан Айк", "Андерс Хейлсберг", "Гвидо ван Россум", "Бьёрн Страуструп"], "correct": 1, "explanation": "TypeScript создал Андерс Хейлсберг (Anders Hejlsberg) в Microsoft."},
        {"question": "Что такое TypeScript?", "options": ["Новый язык не связанный с JS", "Надмножество JavaScript с статической типизацией", "Фреймворк для JavaScript", "Сборщик модулей"], "correct": 1, "explanation": "TypeScript — надмножество JavaScript, добавляющее статическую типизацию."},
        {"question": "В каком году был создан язык Go (Golang)?", "options": ["2007", "2009", "2011", "2013"], "correct": 1, "explanation": "Go был разработан в Google и выпущен в 2009 году."},
        {"question": "Кто создал язык Go?", "options": ["Линус Торвальдс и Ричард Столман", "Грисемер, Пайк и Томпсон", "Гвидо ван Россум", "Страуструп и Ричи"], "correct": 1, "explanation": "Go создали Роберт Гризмер, Роб Пайк и Кен Томпсон в Google."},
        {"question": "Что такое горутина (goroutine) в Go?", "options": ["Тип данных", "Легковесный поток выполнения", "Цикл для обработки ошибок", "Встроенная функция"], "correct": 1, "explanation": "Горутина — легковесный поток выполнения в Go, управляемый средой выполнения Go."},
        {"question": "В каком году был выпущен C#?", "options": ["1998", "2000", "2002", "2004"], "correct": 1, "explanation": "C# был выпущен Microsoft в 2000 году."},
        {"question": "Кто создал C#?", "options": ["Бьёрн Страуструп", "Андерс Хейлсберг", "Джеймс Гослинг", "Деннис Ричи"], "correct": 1, "explanation": "C# создал Андерс Хейлсберг (тот же, кто создал TypeScript) в Microsoft."},
        {"question": "Как расшифровывается C# в контексте языка программирования?", "options": ["C Sharp", "C Hash", "C Hashtag", "C Octothorpe"], "correct": 0, "explanation": "C# читается как C Sharp (C диез) — название музыкального знака повышения тона."},
        {"question": "На какой платформе преимущественно работает C#?", "options": ["JVM", ".NET", "Node.js", "CPython"], "correct": 1, "explanation": "C# работает на платформе .NET (ранее .NET Framework, сейчас .NET Core/.NET 5+)."},
        # 51-60: Ruby, Rust, HTML
        {"question": "Кто создал язык программирования Ruby?", "options": ["Мац Мацумото", "Брендан Айк", "Ларри Уолл", "Гвидо ван Россум"], "correct": 0, "explanation": "Ruby создал Юкихиро Мацумото (Yukihiro Matsumoto), известный как Мац."},
        {"question": "В каком году был создан Ruby?", "options": ["1991", "1993", "1995", "1997"], "correct": 2, "explanation": "Ruby создан в 1995 году Юкихиро Мацумото."},
        {"question": "Какой популярный веб-фреймворк написан на Ruby?", "options": ["Django", "Laravel", "Ruby on Rails", "Spring"], "correct": 2, "explanation": "Ruby on Rails (Rails) — популярный веб-фреймворк, написанный на Ruby."},
        {"question": "Когда был создан язык Rust?", "options": ["2008", "2010", "2012", "2014"], "correct": 1, "explanation": "Rust начал разрабатываться в 2006 году, первый стабильный релиз — 2010 год (публичный проект Mozilla)."},
        {"question": "Кто создал язык Rust?", "options": ["Линус Торвальдс", "Грейдон Хор", "Кен Томпсон", "Деннис Ричи"], "correct": 1, "explanation": "Rust создал Грейдон Хор (Graydon Hoare) при поддержке Mozilla."},
        {"question": "Какое ключевое преимущество Rust перед C/C++?", "options": ["Более медленное выполнение", "Безопасность памяти без сборщика мусора", "Проще синтаксис", "Больше библиотек"], "correct": 1, "explanation": "Rust обеспечивает безопасность памяти (memory safety) без сборщика мусора через систему владения (ownership)."},
        {"question": "Кто создал HTML?", "options": ["Линус Торвальдс", "Тим Бернерс-Ли", "Деннис Ричи", "Брендан Айк"], "correct": 1, "explanation": "HTML создал Тим Бернерс-Ли (Tim Berners-Lee) в CERN."},
        {"question": "В каком году был создан HTML?", "options": ["1985", "1989", "1993", "1995"], "correct": 1, "explanation": "HTML предложен Тимом Бернерсом-Ли в 1989 году, первая спецификация — 1991 год."},
        {"question": "Как расшифровывается HTML?", "options": ["Home Text Markup Language", "HyperText Markup Language", "High Text Making Language", "Hyperlink and Text Management Language"], "correct": 1, "explanation": "HTML — HyperText Markup Language (язык гипертекстовой разметки)."},
        {"question": "Какая последняя крупная версия HTML?", "options": ["HTML 4", "XHTML 2", "HTML5", "HTML6"], "correct": 2, "explanation": "HTML5 — текущая стандартная версия HTML, принята W3C в 2014 году."},
        # 61-70: CSS, Dart, SQL, Kotlin
        {"question": "В каком году появился CSS?", "options": ["1994", "1996", "1998", "2000"], "correct": 1, "explanation": "CSS был предложен в 1994 году, первая спецификация опубликована W3C в 1996 году."},
        {"question": "Кто предложил CSS?", "options": ["Тим Бернерс-Ли", "Хокон Виум Ли и Берт Бос", "Брендан Айк", "Расмус Лердорф"], "correct": 1, "explanation": "CSS предложили Хокон Виум Ли (Hakon Wium Lie) и Берт Бос (Bert Bos)."},
        {"question": "Как расшифровывается CSS?", "options": ["Cascading Style Sheets", "Computer Style Syntax", "Creative Style System", "Content Style Script"], "correct": 0, "explanation": "CSS — Cascading Style Sheets (каскадные таблицы стилей)."},
        {"question": "Когда был создан язык Dart?", "options": ["2009", "2011", "2013", "2015"], "correct": 1, "explanation": "Dart создан в Google в 2011 году, главным разработчиком был Ларс Бак."},
        {"question": "Для какого фреймворка преимущественно используется Dart?", "options": ["React Native", "Flutter", "Ionic", "NativeScript"], "correct": 1, "explanation": "Dart — основной язык для разработки на Flutter (Google)."},
        {"question": "Как расшифровывается SQL?", "options": ["System Query Language", "Structured Query Language", "Sequential Query Logic", "Standard Query Layer"], "correct": 1, "explanation": "SQL — Structured Query Language (язык структурированных запросов)."},
        {"question": "Где был разработан SQL?", "options": ["MIT", "IBM", "Bell Labs", "Stanford"], "correct": 1, "explanation": "SQL разработан в IBM в 1970-х годах Чемберлином и Бойсом."},
        {"question": "В каком году был создан Kotlin?", "options": ["2009", "2011", "2013", "2016"], "correct": 1, "explanation": "Kotlin создан JetBrains в 2011 году (первый стабильный релиз в 2016)."},
        {"question": "Кто создал Kotlin?", "options": ["Google", "JetBrains", "Apple", "Microsoft"], "correct": 1, "explanation": "Kotlin разработан компанией JetBrains."},
        {"question": "В честь чего назван Kotlin?", "options": ["В честь острова рядом с Санкт-Петербургом", "В честь города Котлас", "В честь кофейного напитка", "В честь персонажа игры"], "correct": 0, "explanation": "Kotlin назван в честь острова Котлин вблизи Санкт-Петербурга (Россия)."},
        # 71-80: Swift, Scala, R, Perl, Elixir
        {"question": "В каком году Apple выпустила Swift?", "options": ["2012", "2014", "2016", "2018"], "correct": 1, "explanation": "Swift представлен Apple на WWDC в 2014 году."},
        {"question": "Кто создал Swift?", "options": ["Стив Джобс", "Крис Латтнер", "Тим Кук", "Джонатан Айв"], "correct": 1, "explanation": "Swift создал Крис Латтнер (Chris Lattner) в Apple."},
        {"question": "Для каких платформ предназначен Swift?", "options": ["Android и Windows", "iOS, macOS, watchOS, tvOS", "Linux и Windows", "Только iOS"], "correct": 1, "explanation": "Swift предназначен для разработки под платформы Apple: iOS, macOS, watchOS, tvOS."},
        {"question": "В каком году создан Scala?", "options": ["1999", "2001", "2003", "2005"], "correct": 1, "explanation": "Scala создана в 2001 году Мартином Одерски в EPFL."},
        {"question": "Что значит название Scala?", "options": ["Scalable Language", "Scientific Algorithm Language", "Scripting and Lambda", "System of Classes and Actors"], "correct": 0, "explanation": "Scala — Scalable Language (масштабируемый язык)."},
        {"question": "В каком году создан язык R?", "options": ["1991", "1993", "1995", "1997"], "correct": 1, "explanation": "R создан в 1993 году Россом Ихакой и Робертом Джентлменом в Университете Окленда."},
        {"question": "Для чего преимущественно используется язык R?", "options": ["Веб-разработка", "Статистика и анализ данных", "Мобильные приложения", "Системное программирование"], "correct": 1, "explanation": "R — язык для статистических вычислений и анализа данных."},
        {"question": "Кто создал Perl?", "options": ["Ларри Уолл", "Гвидо ван Россум", "Брендан Айк", "Ричард Столман"], "correct": 0, "explanation": "Perl создал Ларри Уолл (Larry Wall) в 1987 году."},
        {"question": "Как расшифровывается Perl?", "options": ["Practical Extraction and Report Language", "Professional Extension Resource Language", "Public Extended Runtime Library", "Portable Executable Runtime Library"], "correct": 0, "explanation": "Perl — Practical Extraction and Report Language."},
        {"question": "В каком году был создан Elixir?", "options": ["2009", "2011", "2013", "2015"], "correct": 1, "explanation": "Elixir создан в 2011 году Жозе Валимом (Jose Valim)."},
        # 81-90: Julia, WebAssembly, Groovy, C++, C, Lua
        {"question": "В каком университете был создан язык Julia?", "options": ["Стэнфорд", "MIT", "Гарвард", "Беркли"], "correct": 1, "explanation": "Julia разработана в MIT и выпущена в 2012 году."},
        {"question": "Для чего предназначен Julia?", "options": ["Веб-разработка", "Системное программирование", "Научные и численные вычисления", "Мобильная разработка"], "correct": 2, "explanation": "Julia создана для высокопроизводительных научных и численных вычислений."},
        {"question": "Что такое WebAssembly (Wasm)?", "options": ["Язык разметки", "Бинарный формат инструкций для веба", "JavaScript фреймворк", "Серверный язык"], "correct": 1, "explanation": "WebAssembly — бинарный формат инструкций для стековых виртуальных машин, работает в браузере."},
        {"question": "Кто разрабатывает стандарт WebAssembly?", "options": ["Google", "Mozilla", "W3C", "ECMA"], "correct": 2, "explanation": "WebAssembly разрабатывается W3C вместе с основными производителями браузеров."},
        {"question": "В каком году был создан Groovy?", "options": ["2001", "2003", "2005", "2007"], "correct": 1, "explanation": "Groovy создан в 2003 году, разрабатывается Apache Software Foundation."},
        {"question": "На какой платформе работает Groovy?", "options": [".NET", "JVM", "CPython", "Node.js"], "correct": 1, "explanation": "Groovy — язык для JVM, полностью совместим с Java."},
        {"question": "Кто создал C++?", "options": ["Деннис Ричи", "Бьёрн Страуструп", "Кен Томпсон", "Брайан Керниган"], "correct": 1, "explanation": "C++ создал Бьёрн Страуструп (Bjarne Stroustrup) в Bell Labs в 1985 году."},
        {"question": "Что означает ++ в названии C++?", "options": ["Двойное увеличение скорости", "Оператор инкремента — улучшенный C", "Два плюса означают ООП", "Ничего конкретного"], "correct": 1, "explanation": "++ — оператор инкремента в C, т.е. C++ означает следующий C или улучшенный C."},
        {"question": "В каком году был создан язык C?", "options": ["1968", "1972", "1975", "1979"], "correct": 1, "explanation": "Язык C создан в 1972 году Деннисом Ричи в Bell Labs."},
        {"question": "Кто создал язык C?", "options": ["Бьёрн Страуструп", "Кен Томпсон", "Деннис Ричи", "Брайан Керниган"], "correct": 2, "explanation": "Язык C создал Деннис Ричи (Dennis Ritchie) в AT&T Bell Labs."},
        # 91-100: Lua и общие вопросы
        {"question": "Что означает слово Lua на языке, из которого оно происходит?", "options": ["Звезда", "Луна", "Огонь", "Вода"], "correct": 1, "explanation": "Lua в переводе с португальского означает Луна. Язык создан в Бразилии."},
        {"question": "Где был создан язык программирования Lua?", "options": ["MIT", "PUC-Rio (Бразилия)", "Стэнфорд", "CERN"], "correct": 1, "explanation": "Lua создан в Папском католическом университете Рио-де-Жанейро (PUC-Rio) в 1993 году."},
        {"question": "Для чего чаще всего используется Lua?", "options": ["Веб-разработка", "Машинное обучение", "Встраиваемый скриптинг в играх", "Системное программирование"], "correct": 2, "explanation": "Lua широко используется как встраиваемый скриптовый язык в игровых движках (Roblox, World of Warcraft)."},
        {"question": "Какой из языков является компилируемым (не интерпретируемым)?", "options": ["Python", "JavaScript", "PHP", "C"], "correct": 3, "explanation": "C — компилируемый язык. Python, JS, PHP — интерпретируемые."},
        {"question": "Какой язык программирования использует garbage collection (сборщик мусора)?", "options": ["C", "C++", "Rust", "Java"], "correct": 3, "explanation": "Java использует автоматическую сборку мусора. C и C++ управляют памятью вручную, Rust — через ownership."},
        {"question": "Какой язык создан специально для параллельного и конкурентного программирования?", "options": ["Python", "PHP", "Go", "Ruby"], "correct": 2, "explanation": "Go создавался с учётом конкурентного программирования, горутины и каналы — его ключевые особенности."},
        {"question": "Какой из языков является языком разметки, а не программирования?", "options": ["Python", "HTML", "JavaScript", "PHP"], "correct": 1, "explanation": "HTML — язык разметки гипертекста, а не язык программирования."},
        {"question": "Что такое IDE?", "options": ["Internet Data Exchange", "Integrated Development Environment", "Internal Debug Engine", "Interface Design Editor"], "correct": 1, "explanation": "IDE — Integrated Development Environment (интегрированная среда разработки)."},
        {"question": "Что такое API?", "options": ["Advanced Programming Interface", "Application Programming Interface", "Automated Process Integration", "Accessible Protocol Interface"], "correct": 1, "explanation": "API — Application Programming Interface (интерфейс программирования приложений)."},
        {"question": "Какой язык программирования был создан первым?", "options": ["C", "Fortran", "COBOL", "Pascal"], "correct": 1, "explanation": "Fortran (1957) — один из первых высокоуровневых языков программирования."},
    ],
    "networks": [
        # 1-10: Типы сетей
        {"question": "Как расшифровывается LAN?", "options": ["Large Area Network", "Local Area Network", "Linked Access Node", "Light Access Network"], "correct": 1, "explanation": "LAN — Local Area Network (локальная вычислительная сеть)."},
        {"question": "Как расшифровывается WAN?", "options": ["Wireless Access Node", "Wide Area Network", "Web Application Network", "Wired Attached Network"], "correct": 1, "explanation": "WAN — Wide Area Network (глобальная сеть)."},
        {"question": "Как расшифровывается MAN?", "options": ["Mobile Area Network", "Metropolitan Area Network", "Multiple Access Node", "Managed Access Network"], "correct": 1, "explanation": "MAN — Metropolitan Area Network (городская сеть)."},
        {"question": "Как расшифровывается PAN?", "options": ["Public Access Network", "Personal Area Network", "Protocol Access Node", "Portable Area Network"], "correct": 1, "explanation": "PAN — Personal Area Network (персональная сеть, например, Bluetooth)."},
        {"question": "Какой стандарт лежит в основе Wi-Fi?", "options": ["IEEE 802.3", "IEEE 802.11", "IEEE 802.15", "IEEE 802.16"], "correct": 1, "explanation": "Wi-Fi основан на стандарте IEEE 802.11."},
        {"question": "В каком году появился первый стандарт Wi-Fi?", "options": ["1994", "1997", "1999", "2001"], "correct": 1, "explanation": "Первый стандарт Wi-Fi (IEEE 802.11) принят в 1997 году."},
        {"question": "На каких частотах работает Wi-Fi?", "options": ["900 МГц и 1.8 ГГц", "2.4 ГГц и 5 ГГц", "3.5 ГГц и 7 ГГц", "1 ГГц и 10 ГГц"], "correct": 1, "explanation": "Wi-Fi работает на частотах 2.4 ГГц и 5 ГГц (а также 6 ГГц в новых стандартах)."},
        {"question": "Что такое топология сети?", "options": ["Физическое расположение кабелей", "Схема соединения узлов сети", "Протокол передачи данных", "Тип сетевого оборудования"], "correct": 1, "explanation": "Топология сети — схема физического или логического соединения узлов."},
        {"question": "Какая топология сети является наиболее распространённой в современных ЛВС?", "options": ["Шина", "Кольцо", "Звезда", "Ячеистая"], "correct": 2, "explanation": "Топология звезда наиболее распространена — все узлы подключены к центральному коммутатору."},
        {"question": "Что такое протокол TCP/IP?", "options": ["Язык программирования для сетей", "Набор правил для передачи данных в интернете", "Тип сетевого кабеля", "Операционная система"], "correct": 1, "explanation": "TCP/IP — набор сетевых протоколов, основа интернета."},
        # 11-20: Протоколы HTTP, HTTPS, DNS, FTP, SSH
        {"question": "Кто создал протокол HTTP?", "options": ["Винт Серф и Боб Кан", "Тим Бернерс-Ли", "Расмус Лердорф", "Деннис Ричи"], "correct": 1, "explanation": "HTTP создал Тим Бернерс-Ли в CERN в 1991 году."},
        {"question": "Какой порт по умолчанию использует HTTP?", "options": ["21", "443", "80", "8080"], "correct": 2, "explanation": "HTTP использует порт 80 по умолчанию."},
        {"question": "Какой порт по умолчанию использует HTTPS?", "options": ["80", "443", "8443", "21"], "correct": 1, "explanation": "HTTPS использует порт 443 по умолчанию."},
        {"question": "Что означает S в HTTPS?", "options": ["Speed", "Secure", "Server", "Static"], "correct": 1, "explanation": "S в HTTPS означает Secure (защищённый), шифрование обеспечивается TLS/SSL."},
        {"question": "Как расшифровывается DNS?", "options": ["Dynamic Network Service", "Domain Name System", "Data Network Server", "Distributed Node Service"], "correct": 1, "explanation": "DNS — Domain Name System (система доменных имён)."},
        {"question": "В каком году создан DNS?", "options": ["1978", "1983", "1987", "1991"], "correct": 1, "explanation": "DNS разработан Полом Мокапетрисом в 1983 году."},
        {"question": "Какой порт использует DNS?", "options": ["25", "53", "80", "443"], "correct": 1, "explanation": "DNS использует порт 53 (TCP и UDP)."},
        {"question": "Какой порт использует FTP?", "options": ["20/21", "22", "25", "80"], "correct": 0, "explanation": "FTP использует порт 21 (управление) и 20 (данные)."},
        {"question": "Что безопаснее: FTP или SFTP?", "options": ["FTP", "SFTP", "Оба одинаково безопасны", "Зависит от настроек"], "correct": 1, "explanation": "SFTP (SSH File Transfer Protocol) безопаснее, так как использует шифрование."},
        {"question": "Кто создал SSH?", "options": ["Тим Бернерс-Ли", "Тату Илёнен", "Винт Серф", "Лайнус Торвальдс"], "correct": 1, "explanation": "SSH создал Тату Илёнен (Tatu Ylonen) в 1995 году."},
        # 21-30: SSH, UDP, IPv4, IPv6, DHCP, NAT
        {"question": "Какой порт использует SSH?", "options": ["21", "22", "23", "25"], "correct": 1, "explanation": "SSH использует порт 22."},
        {"question": "Что заменил SSH?", "options": ["FTP", "HTTP", "Telnet", "SMTP"], "correct": 2, "explanation": "SSH пришёл на смену Telnet, обеспечив зашифрованный удалённый доступ."},
        {"question": "В чём главное отличие UDP от TCP?", "options": ["UDP быстрее, но не гарантирует доставку", "UDP медленнее, но надёжнее", "UDP работает только в LAN", "UDP использует шифрование"], "correct": 0, "explanation": "UDP — быстрый, но ненадёжный протокол без гарантии доставки пакетов."},
        {"question": "Для чего используется UDP?", "options": ["Передача файлов", "Потоковое видео и онлайн-игры", "Электронная почта", "Банковские транзакции"], "correct": 1, "explanation": "UDP используется там, где важна скорость: потоковое видео, VoIP, онлайн-игры."},
        {"question": "Сколько бит в IPv4 адресе?", "options": ["16", "32", "64", "128"], "correct": 1, "explanation": "IPv4 адрес — 32 бита (4 октета, например 192.168.1.1)."},
        {"question": "Сколько уникальных адресов может быть в IPv4?", "options": ["около 4.3 млрд", "около 43 млрд", "около 4.3 трлн", "бесконечно"], "correct": 0, "explanation": "IPv4 позволяет примерно 4.3 миллиарда адресов (2^32 = 4 294 967 296)."},
        {"question": "Сколько бит в IPv6 адресе?", "options": ["32", "64", "128", "256"], "correct": 2, "explanation": "IPv6 адрес — 128 бит, что даёт колоссальное количество адресов."},
        {"question": "Как расшифровывается DHCP?", "options": ["Dynamic Host Configuration Protocol", "Distributed Host Connection Protocol", "Data Host Control Protocol", "Dynamic HTTP Connection Protocol"], "correct": 0, "explanation": "DHCP — Dynamic Host Configuration Protocol (протокол динамической настройки хоста)."},
        {"question": "В каком году создан DHCP?", "options": ["1989", "1993", "1997", "2001"], "correct": 1, "explanation": "DHCP разработан в 1993 году (RFC 1531)."},
        {"question": "Что делает NAT?", "options": ["Шифрует трафик", "Транслирует приватные IP в публичные", "Фильтрует вирусы", "Маршрутизирует IPv6"], "correct": 1, "explanation": "NAT (Network Address Translation) транслирует частные IP-адреса в публичные при выходе в интернет."},
        # 31-40: Localhost, браузеры
        {"question": "Какой IP-адрес соответствует localhost?", "options": ["0.0.0.0", "127.0.0.1", "192.168.0.1", "255.255.255.255"], "correct": 1, "explanation": "localhost — это 127.0.0.1 (loopback адрес), указывающий на текущий компьютер."},
        {"question": "В каком году был выпущен Internet Explorer?", "options": ["1993", "1995", "1997", "1999"], "correct": 1, "explanation": "Internet Explorer вышел в 1995 году в составе Windows 95."},
        {"question": "В каком году Microsoft прекратила поддержку Internet Explorer?", "options": ["2019", "2020", "2022", "2023"], "correct": 2, "explanation": "Microsoft прекратила поддержку IE 11 в июне 2022 года."},
        {"question": "В каком году вышел браузер Firefox?", "options": ["2002", "2004", "2006", "2008"], "correct": 1, "explanation": "Firefox выпущен Mozilla Foundation в 2004 году."},
        {"question": "Кем разработан браузер Firefox?", "options": ["Google", "Microsoft", "Mozilla", "Apple"], "correct": 2, "explanation": "Firefox разработан Mozilla Foundation (и Mozilla Corporation)."},
        {"question": "В каком году вышел браузер Google Chrome?", "options": ["2006", "2007", "2008", "2009"], "correct": 2, "explanation": "Google Chrome выпущен в 2008 году."},
        {"question": "Какой JavaScript движок использует Chrome?", "options": ["SpiderMonkey", "V8", "JavaScriptCore", "Chakra"], "correct": 1, "explanation": "Chrome использует движок V8, разработанный Google."},
        {"question": "Какой примерно рыночной долей обладает Chrome среди браузеров?", "options": ["30%", "45%", "60%", "более 60%"], "correct": 3, "explanation": "Chrome занимает более 60% рынка браузеров (по разным данным, 65-70%)."},
        {"question": "В каком году вышел браузер Safari?", "options": ["2001", "2003", "2005", "2007"], "correct": 1, "explanation": "Safari выпущен Apple в 2003 году."},
        {"question": "Какой движок рендеринга использует Safari?", "options": ["Blink", "Gecko", "WebKit", "Trident"], "correct": 2, "explanation": "Safari использует движок WebKit, разработанный Apple."},
        # 41-50: Edge, Opera, серверы
        {"question": "В каком году Microsoft выпустила браузер Edge?", "options": ["2013", "2015", "2017", "2019"], "correct": 1, "explanation": "Microsoft Edge выпущен в 2015 году вместе с Windows 10."},
        {"question": "На какой движок перешёл Edge в 2020 году?", "options": ["Gecko", "WebKit", "Blink (Chromium)", "Trident"], "correct": 2, "explanation": "В 2020 году Edge перешёл на движок Chromium (Blink), как и Chrome."},
        {"question": "В каком году создан браузер Opera?", "options": ["1993", "1995", "1997", "1999"], "correct": 1, "explanation": "Opera создана в 1995 году норвежской компанией Opera Software."},
        {"question": "Какое нововведение приписывают браузеру Opera?", "options": ["Вкладки в браузере", "JavaScript", "Cookie", "SSL"], "correct": 0, "explanation": "Opera была первым браузером с вкладками (tabbed browsing)."},
        {"question": "Что такое XAMPP?", "options": ["Язык программирования", "Пакет локального сервера (Apache+MySQL+PHP+Perl)", "Облачный хостинг", "Система контроля версий"], "correct": 1, "explanation": "XAMPP — бесплатный пакет локального сервера: X (кросс-платформ.), Apache, MariaDB, PHP, Perl."},
        {"question": "В каком году создан XAMPP?", "options": ["1999", "2002", "2005", "2008"], "correct": 1, "explanation": "XAMPP создан в 2002 году Apache Friends."},
        {"question": "Что означает буква X в XAMPP?", "options": ["eXtended", "Кросс-платформенность", "XML", "eXtra"], "correct": 1, "explanation": "X в XAMPP означает кросс-платформенность (работает на Windows, Linux, macOS)."},
        {"question": "Где по умолчанию хранятся файлы сайтов в XAMPP?", "options": ["www/", "public/", "htdocs/", "webroot/"], "correct": 2, "explanation": "В XAMPP файлы сайтов хранятся в директории htdocs/."},
        {"question": "Какой порт по умолчанию использует MySQL?", "options": ["1433", "3306", "5432", "27017"], "correct": 1, "explanation": "MySQL использует порт 3306 по умолчанию."},
        {"question": "Какой порт по умолчанию использует PostgreSQL?", "options": ["1433", "3306", "5432", "27017"], "correct": 2, "explanation": "PostgreSQL использует порт 5432 по умолчанию."},
        # 51-60: Порты и протоколы
        {"question": "Какой порт по умолчанию использует MongoDB?", "options": ["5432", "6379", "27017", "3306"], "correct": 2, "explanation": "MongoDB использует порт 27017 по умолчанию."},
        {"question": "Какой порт по умолчанию использует Redis?", "options": ["5432", "6379", "27017", "3306"], "correct": 1, "explanation": "Redis использует порт 6379 по умолчанию."},
        {"question": "Какой порт по умолчанию использует Express.js?", "options": ["3000", "4000", "5000", "8000"], "correct": 0, "explanation": "Express.js по умолчанию запускается на порту 3000."},
        {"question": "Какой порт использует SMTP?", "options": ["25", "53", "80", "110"], "correct": 0, "explanation": "SMTP (Simple Mail Transfer Protocol) использует порт 25."},
        {"question": "Что такое SSL/TLS?", "options": ["Язык программирования", "Протоколы шифрования для защиты данных", "Тип базы данных", "Браузерный движок"], "correct": 1, "explanation": "SSL/TLS — протоколы шифрования, обеспечивающие безопасную передачу данных (HTTPS)."},
        {"question": "Что такое VPN?", "options": ["Very Private Network", "Virtual Private Network", "Virtual Public Node", "Verified Packet Network"], "correct": 1, "explanation": "VPN — Virtual Private Network (виртуальная частная сеть)."},
        {"question": "Что такое firewall (брандмауэр)?", "options": ["Антивирусная программа", "Система мониторинга сети", "Система фильтрации сетевого трафика", "Протокол шифрования"], "correct": 2, "explanation": "Firewall — система для фильтрации сетевого трафика по заданным правилам."},
        {"question": "Что такое Cookie в контексте браузеров?", "options": ["Вирус", "Небольшие данные, хранимые браузером от сайтов", "Тип шифрования", "Кэш браузера"], "correct": 1, "explanation": "Cookie — небольшие фрагменты данных, которые веб-сайты сохраняют в браузере пользователя."},
        {"question": "Что такое кэш браузера?", "options": ["История посещений", "Сохранённые пароли", "Временные файлы для ускорения загрузки страниц", "Открытые вкладки"], "correct": 2, "explanation": "Кэш браузера — временное хранилище файлов сайтов для ускорения повторной загрузки."},
        {"question": "Что такое URL?", "options": ["Universal Resource Locator", "Unique Resource Link", "Universal Remote Language", "Unified Request Locator"], "correct": 0, "explanation": "URL — Uniform Resource Locator (унифицированный указатель ресурса — адрес в интернете)."},
        # 61-70: Сетевые устройства и концепции
        {"question": "Чем роутер отличается от коммутатора (switch)?", "options": ["Роутер дороже", "Роутер маршрутизирует между сетями, switch — внутри сети", "Switch работает быстрее", "Роутер — устаревший switch"], "correct": 1, "explanation": "Роутер маршрутизирует трафик между разными сетями, switch соединяет устройства внутри одной сети."},
        {"question": "Что такое MAC-адрес?", "options": ["IP-адрес для Mac компьютеров", "Уникальный аппаратный адрес сетевого интерфейса", "Протокол шифрования", "Адрес Wi-Fi роутера"], "correct": 1, "explanation": "MAC-адрес — уникальный 48-битный аппаратный адрес сетевого интерфейса (например, AA:BB:CC:DD:EE:FF)."},
        {"question": "Что такое IP-адрес?", "options": ["Физический адрес устройства", "Логический адрес устройства в сети", "Серийный номер устройства", "Адрес веб-сайта"], "correct": 1, "explanation": "IP-адрес — логический адрес устройства в сети, используемый для маршрутизации."},
        {"question": "Что такое подсеть (subnet)?", "options": ["Тип сетевого кабеля", "Логическое разделение IP-сети", "Протокол маршрутизации", "Устройство связи"], "correct": 1, "explanation": "Подсеть — логическое разбиение IP-сети для эффективной организации адресного пространства."},
        {"question": "Что такое DNS-сервер?", "options": ["Сервер хранения файлов", "Сервер преобразования доменных имён в IP-адреса", "Почтовый сервер", "Игровой сервер"], "correct": 1, "explanation": "DNS-сервер преобразует доменные имена (google.com) в IP-адреса."},
        {"question": "Что такое HTTP-запрос GET?", "options": ["Удаляет ресурс на сервере", "Запрашивает данные с сервера", "Отправляет данные на сервер", "Обновляет данные на сервере"], "correct": 1, "explanation": "GET — метод HTTP для получения (запроса) данных с сервера."},
        {"question": "Что такое HTTP-запрос POST?", "options": ["Удаляет ресурс", "Запрашивает данные", "Отправляет данные на сервер", "Обновляет частично"], "correct": 2, "explanation": "POST — метод HTTP для отправки данных на сервер (создание ресурса)."},
        {"question": "Какой HTTP-код означает Не найдено?", "options": ["200", "301", "403", "404"], "correct": 3, "explanation": "HTTP 404 — Not Found (ресурс не найден)."},
        {"question": "Какой HTTP-код означает успешный запрос?", "options": ["200", "301", "404", "500"], "correct": 0, "explanation": "HTTP 200 — OK (запрос выполнен успешно)."},
        {"question": "Какой HTTP-код означает внутреннюю ошибку сервера?", "options": ["400", "403", "404", "500"], "correct": 3, "explanation": "HTTP 500 — Internal Server Error (внутренняя ошибка сервера)."},
        # 71-80: REST, WebSocket, CDN и др.
        {"question": "Что такое REST API?", "options": ["Протокол шифрования", "Архитектурный стиль для создания API на HTTP", "Фреймворк для Python", "Тип базы данных"], "correct": 1, "explanation": "REST (Representational State Transfer) — архитектурный стиль для создания веб-API."},
        {"question": "Что такое WebSocket?", "options": ["Тип HTTP-запроса", "Протокол постоянного двунаправленного соединения", "Физический разъём", "Браузерное расширение"], "correct": 1, "explanation": "WebSocket — протокол, обеспечивающий постоянное двунаправленное соединение между клиентом и сервером."},
        {"question": "Что такое CDN?", "options": ["Code Delivery Network", "Content Delivery Network", "Central Data Node", "Cloud DNS Network"], "correct": 1, "explanation": "CDN — Content Delivery Network (сеть доставки контента) для быстрой отдачи статики."},
        {"question": "Что такое load balancer (балансировщик нагрузки)?", "options": ["Устройство для увеличения скорости интернета", "Система распределения запросов между серверами", "Тип маршрутизатора", "Протокол синхронизации"], "correct": 1, "explanation": "Load balancer распределяет входящие запросы между несколькими серверами."},
        {"question": "Что такое proxy-сервер?", "options": ["Резервный сервер", "Посредник между клиентом и целевым сервером", "Тип файервола", "DNS-сервер"], "correct": 1, "explanation": "Proxy-сервер — промежуточный сервер, действующий как посредник между клиентом и целевым сервером."},
        {"question": "Что означает CORS?", "options": ["Cross-Origin Resource Sharing", "Content Origin Resource Server", "Cached Origin Request System", "Cross-Output Rendering Service"], "correct": 0, "explanation": "CORS — Cross-Origin Resource Sharing (совместное использование ресурсов между источниками)."},
        {"question": "Что такое API endpoint?", "options": ["Конечная точка API — конкретный URL для запроса", "Документация API", "Версия API", "Ключ аутентификации"], "correct": 0, "explanation": "Endpoint — конкретный URL (адрес) в API, к которому обращается клиент."},
        {"question": "Что такое JSON?", "options": ["JavaScript Object Notation", "Java Source Object Network", "JavaScript Online Node", "Java Standard Output Notation"], "correct": 0, "explanation": "JSON — JavaScript Object Notation, формат обмена данными."},
        {"question": "Что такое XML?", "options": ["eXtensible Markup Language", "External Module Library", "Extra Model Link", "eXtra Machine Learning"], "correct": 0, "explanation": "XML — eXtensible Markup Language (расширяемый язык разметки)."},
        {"question": "Что такое GraphQL?", "options": ["База данных графов", "Язык запросов для API", "Библиотека визуализации", "Тип SQL"], "correct": 1, "explanation": "GraphQL — язык запросов для API, позволяющий запрашивать именно нужные данные."},
        # 81-90: Облако, безопасность, прочее
        {"question": "Что такое облачные вычисления (cloud computing)?", "options": ["Вычисления в атмосфере", "Предоставление ИТ-ресурсов через интернет", "Беспроводная передача данных", "Распределённая база данных"], "correct": 1, "explanation": "Облачные вычисления — предоставление ИТ-ресурсов (серверов, хранилищ, ПО) через интернет."},
        {"question": "Что такое SaaS?", "options": ["Software as a Service", "Server as a System", "Security as a Standard", "Storage as a Service"], "correct": 0, "explanation": "SaaS — Software as a Service (программное обеспечение как услуга, например, Google Docs)."},
        {"question": "Что такое IaaS?", "options": ["Infrastructure as a Service", "Internet as a Service", "Integration as a Solution", "Input as a Source"], "correct": 0, "explanation": "IaaS — Infrastructure as a Service (инфраструктура как услуга, например, AWS EC2)."},
        {"question": "Что такое DoS-атака?", "options": ["Кража данных", "Атака отказа в обслуживании", "Взлом паролей", "SQL-инъекция"], "correct": 1, "explanation": "DoS (Denial of Service) — атака, цель которой — сделать сервис недоступным для пользователей."},
        {"question": "Что такое фишинг?", "options": ["Взлом через уязвимость ПО", "Мошенничество с целью кражи данных через поддельные сайты/письма", "DDoS-атака", "Вирус-шифровальщик"], "correct": 1, "explanation": "Фишинг — вид мошенничества, при котором злоумышленники создают поддельные сайты или письма для кражи данных."},
        {"question": "Что такое двухфакторная аутентификация (2FA)?", "options": ["Вход с двух устройств", "Подтверждение личности двумя независимыми способами", "Двойной пароль", "Биометрия"], "correct": 1, "explanation": "2FA — подтверждение личности двумя независимыми факторами (пароль + SMS-код)."},
        {"question": "Что такое хэширование пароля?", "options": ["Шифрование пароля с ключом", "Необратимое преобразование пароля в строку фиксированной длины", "Сжатие пароля", "Дублирование пароля"], "correct": 1, "explanation": "Хэширование — необратимое преобразование пароля (bcrypt, SHA-256) для безопасного хранения."},
        {"question": "Что такое SQL-инъекция?", "options": ["Оптимизация SQL-запросов", "Атака через вставку вредоносного SQL-кода в запросы", "Тип репликации БД", "Бэкап базы данных"], "correct": 1, "explanation": "SQL-инъекция — атака, при которой злоумышленник встраивает вредоносный SQL-код в запрос приложения."},
        {"question": "Для чего нужен HTTPS вместо HTTP?", "options": ["Для ускорения загрузки", "Для шифрования передаваемых данных", "Для сжатия трафика", "Для кэширования страниц"], "correct": 1, "explanation": "HTTPS шифрует данные между браузером и сервером, защищая их от перехвата."},
        {"question": "Что такое токен авторизации (JWT)?", "options": ["Куки браузера", "JSON Web Token — компактный способ передачи авторизационных данных", "Сессионный ключ Redis", "Тип SSL-сертификата"], "correct": 1, "explanation": "JWT (JSON Web Token) — компактный, подписанный токен для передачи авторизационных данных."},
        # 91-100: Разное
        {"question": "Что такое SEO?", "options": ["Server Execution Optimization", "Search Engine Optimization", "System Enhancement Operation", "Software Engineering Output"], "correct": 1, "explanation": "SEO — Search Engine Optimization (поисковая оптимизация)."},
        {"question": "Что такое CMS?", "options": ["Code Management System", "Content Management System", "Cloud Monitoring Service", "Centralized Mail Server"], "correct": 1, "explanation": "CMS — Content Management System (система управления контентом), например WordPress."},
        {"question": "Что означает responsive design?", "options": ["Быстро загружающийся дизайн", "Адаптивный дизайн под разные экраны", "Красивый дизайн", "Интерактивный дизайн"], "correct": 1, "explanation": "Responsive design — адаптивный дизайн, корректно отображающийся на разных устройствах и экранах."},
        {"question": "Что такое DevOps?", "options": ["Язык программирования", "Культура и практики объединения разработки и операций", "Тип базы данных", "Фреймворк для Python"], "correct": 1, "explanation": "DevOps — культура и набор практик, объединяющих разработку (Dev) и эксплуатацию (Ops)."},
        {"question": "Что такое CI/CD?", "options": ["Coding Interface/Code Deployment", "Continuous Integration/Continuous Delivery", "Client Interface/Client Development", "Code Inspection/Code Debug"], "correct": 1, "explanation": "CI/CD — Continuous Integration / Continuous Delivery (непрерывная интеграция и доставка)."},
        {"question": "Что такое Git?", "options": ["IDE для программирования", "Distributed version control system", "Облачный хостинг кода", "Язык сценариев"], "correct": 1, "explanation": "Git — распределённая система контроля версий, созданная Линусом Торвальдсом."},
        {"question": "Для чего используется Nginx?", "options": ["Управление базами данных", "Веб-сервер и обратный прокси", "Контейнеризация", "Мониторинг сети"], "correct": 1, "explanation": "Nginx — высокопроизводительный веб-сервер и обратный прокси-сервер."},
        {"question": "Что такое Docker?", "options": ["Язык программирования", "Система контейнеризации приложений", "Облачный провайдер", "Тип базы данных"], "correct": 1, "explanation": "Docker — платформа для создания и запуска приложений в контейнерах."},
        {"question": "Что такое API ключ?", "options": ["Пароль к базе данных", "Уникальный идентификатор для авторизации обращений к API", "Токен SSL", "Ключ шифрования файлов"], "correct": 1, "explanation": "API ключ — уникальный идентификатор, используемый для аутентификации при запросах к API."},
        {"question": "Чем отличается синхронный запрос от асинхронного в вебе?", "options": ["Синхронный быстрее", "Асинхронный не блокирует выполнение кода во время ожидания ответа", "Нет разницы", "Асинхронный использует другой протокол"], "correct": 1, "explanation": "Асинхронный запрос не блокирует выполнение кода — можно продолжать работу, пока ожидается ответ."},
    ],
    "visual": [
        # 1-10: Scratch
        {"question": "В каком году создан Scratch?", "options": ["2003", "2005", "2007", "2009"], "correct": 2, "explanation": "Scratch создан в 2007 году в MIT Media Lab."},
        {"question": "Где был создан Scratch?", "options": ["Google", "Stanford", "MIT Media Lab", "Carnegie Mellon"], "correct": 2, "explanation": "Scratch разработан в MIT Media Lab (Массачусетский технологический институт)."},
        {"question": "Для какой аудитории предназначен Scratch?", "options": ["Профессиональные разработчики", "Студенты вузов", "Дети от 8 лет и старше", "Системные администраторы"], "correct": 2, "explanation": "Scratch предназначен для детей от 8 лет и старше для обучения программированию."},
        {"question": "Как называются объекты в Scratch?", "options": ["Объекты", "Актёры", "Спрайты", "Модули"], "correct": 2, "explanation": "В Scratch объекты называются спрайтами (sprites)."},
        {"question": "Какой тип программирования использует Scratch?", "options": ["Текстовое программирование", "Блочное (визуальное) программирование", "Командная строка", "Бинарное программирование"], "correct": 1, "explanation": "Scratch использует блочное (визуальное) программирование — блоки соединяются как пазлы."},
        {"question": "На каком языке программирования написан Scratch 3.0?", "options": ["Python", "Java", "JavaScript", "C++"], "correct": 2, "explanation": "Scratch 3.0 написан с использованием JavaScript."},
        {"question": "Что можно создавать в Scratch?", "options": ["Только игры", "Только анимации", "Игры, анимации, истории и симуляции", "Только мобильные приложения"], "correct": 2, "explanation": "В Scratch можно создавать игры, анимации, интерактивные истории и симуляции."},
        {"question": "Как называется сцена в Scratch, на которой происходит действие?", "options": ["Canvas", "Stage (Сцена)", "Board", "Frame"], "correct": 1, "explanation": "В Scratch место действия называется Stage (Сцена)."},
        {"question": "Что такое костюм (costume) в Scratch?", "options": ["Фоновое изображение", "Внешний вид спрайта", "Звуковой эффект", "Скрипт управления"], "correct": 1, "explanation": "Костюм — это внешний вид (изображение) спрайта в Scratch; у спрайта может быть несколько костюмов."},
        {"question": "Сколько пользователей зарегистрировано на Scratch (приблизительно)?", "options": ["1 млн", "10 млн", "более 100 млн", "500 тыс"], "correct": 2, "explanation": "На платформе Scratch зарегистрировано более 100 миллионов пользователей по всему миру."},
        # 11-20: Blockly, MIT App Inventor, Code.org
        {"question": "Кто разработал Blockly?", "options": ["Apple", "Microsoft", "Google", "MIT"], "correct": 2, "explanation": "Blockly разработан Google в 2012 году."},
        {"question": "В каком году создан Blockly?", "options": ["2010", "2012", "2014", "2016"], "correct": 1, "explanation": "Blockly выпущен Google в 2012 году."},
        {"question": "Какие языки программирования может генерировать Blockly?", "options": ["Только JavaScript", "JavaScript, Python, PHP, Lua, Dart и другие", "Только Python", "Java и C++"], "correct": 1, "explanation": "Blockly генерирует код на JavaScript, Python, PHP, Lua, Dart и других языках."},
        {"question": "Что такое MIT App Inventor?", "options": ["IDE для Java", "Визуальная среда для создания Android-приложений", "Игровой движок", "Среда для Scratch"], "correct": 1, "explanation": "MIT App Inventor — визуальная среда разработки Android-приложений без написания кода."},
        {"question": "В каком году создан MIT App Inventor?", "options": ["2008", "2010", "2012", "2014"], "correct": 1, "explanation": "App Inventor создан в 2010 году в MIT (ранее в Google)."},
        {"question": "Приложения MIT App Inventor работают на какой платформе?", "options": ["iOS", "Android", "Windows Phone", "Все платформы"], "correct": 1, "explanation": "MIT App Inventor создаёт приложения для Android."},
        {"question": "Какой формат имеет собранное приложение в MIT App Inventor?", "options": [".app", ".exe", ".apk", ".ipa"], "correct": 2, "explanation": "Приложение, созданное в MIT App Inventor, экспортируется как .apk файл для Android."},
        {"question": "Кто основал Code.org?", "options": ["Билл Гейтс и Стив Джобс", "Хади и Али Партови", "Лейн Хорсли и Брайан Криггер", "Сундар Пичай и Марк Цукерберг"], "correct": 1, "explanation": "Code.org основан братьями Хади Партови и Али Партови в 2013 году."},
        {"question": "В каком году основан Code.org?", "options": ["2011", "2013", "2015", "2017"], "correct": 1, "explanation": "Code.org основан в 2013 году."},
        {"question": "Сколько человек прошли курсы Code.org?", "options": ["1 млн", "10 млн", "50 млн", "более 100 млн"], "correct": 3, "explanation": "Более 100 миллионов учащихся воспользовались курсами Code.org."},
        # 21-30: Snap!, Stencyl, Blockly Games, Alice, Logo
        {"question": "Как ещё называется Snap!?", "options": ["BYOB", "LEGO", "DRAG", "CLIP"], "correct": 0, "explanation": "Snap! ранее называлась BYOB — Build Your Own Blocks."},
        {"question": "Где разработан Snap! (BYOB)?", "options": ["MIT", "UC Berkeley", "Stanford", "Carnegie Mellon"], "correct": 1, "explanation": "Snap! разработан в Университете Калифорнии в Беркли (UC Berkeley)."},
        {"question": "В каком году создан Snap! (BYOB)?", "options": ["2007", "2009", "2011", "2013"], "correct": 1, "explanation": "Snap! (BYOB) создан в 2009 году."},
        {"question": "Для чего предназначен Stencyl?", "options": ["Веб-разработка", "Создание 2D-игр", "Анализ данных", "Работа с базами данных"], "correct": 1, "explanation": "Stencyl — среда визуального программирования для создания 2D-игр."},
        {"question": "В каком году создан Stencyl?", "options": ["2007", "2009", "2011", "2013"], "correct": 2, "explanation": "Stencyl выпущен в 2011 году."},
        {"question": "Кто разработал Blockly Games?", "options": ["MIT", "Google", "Apple", "Mozilla"], "correct": 1, "explanation": "Blockly Games разработаны Google."},
        {"question": "В каком году появились Blockly Games?", "options": ["2012", "2014", "2016", "2018"], "correct": 1, "explanation": "Blockly Games выпущены в 2014 году."},
        {"question": "Сколько обучающих игр входит в Blockly Games?", "options": ["3", "5", "7", "10"], "correct": 1, "explanation": "Blockly Games включает 5 основных обучающих игр."},
        {"question": "Кто создал язык Alice?", "options": ["Ричард Столман", "Рэнди Пауш", "Сеймур Пейперт", "Алан Тьюринг"], "correct": 1, "explanation": "Alice разработана Рэнди Паушем (Randy Pausch) в Carnegie Mellon University."},
        {"question": "В каком году создан Alice?", "options": ["1990", "1994", "1998", "2002"], "correct": 1, "explanation": "Alice разработана в 1994 году в Carnegie Mellon University."},
        # 31-40: Logo, RGB
        {"question": "Кто создал язык Logo?", "options": ["Алан Тьюринг", "Сеймур Пейперт", "Джон Маккарти", "Марвин Минский"], "correct": 1, "explanation": "Logo создал Сеймур Пейперт (Seymour Papert) в MIT в 1967 году."},
        {"question": "В каком году создан Logo?", "options": ["1960", "1963", "1967", "1972"], "correct": 2, "explanation": "Logo создан в 1967 году."},
        {"question": "Что управляет в Logo при рисовании?", "options": ["Мышь", "Черепаха (turtle)", "Карандаш", "Кисть"], "correct": 1, "explanation": "В Logo используется концепция черепашьей графики — управление черепахой, которая оставляет след."},
        {"question": "Какая цветовая модель складывается из красного, зелёного и синего?", "options": ["CMYK", "HSL", "RGB", "LAB"], "correct": 2, "explanation": "RGB — Red, Green, Blue — аддитивная цветовая модель для экранов."},
        {"question": "Сколько значений может принимать каждый канал в RGB?", "options": ["128", "256", "512", "1024"], "correct": 1, "explanation": "Каждый канал RGB (R, G, B) принимает значения от 0 до 255 — итого 256 значений."},
        {"question": "Сколько цветов можно представить в RGB?", "options": ["65 536", "1 048 576", "16 777 216", "4 294 967 296"], "correct": 2, "explanation": "RGB позволяет представить 256^3 = 16 777 216 примерно 16.7 млн цветов."},
        {"question": "Какой цвет соответствует RGB #FF0000?", "options": ["Зелёный", "Синий", "Белый", "Красный"], "correct": 3, "explanation": "#FF0000 — чистый красный (R=255, G=0, B=0)."},
        {"question": "Какой цвет соответствует RGB #00FF00?", "options": ["Красный", "Зелёный", "Синий", "Жёлтый"], "correct": 1, "explanation": "#00FF00 — чистый зелёный (R=0, G=255, B=0)."},
        {"question": "Какой цвет соответствует RGB #0000FF?", "options": ["Красный", "Зелёный", "Синий", "Белый"], "correct": 2, "explanation": "#0000FF — чистый синий (R=0, G=0, B=255)."},
        {"question": "Какой цвет соответствует RGB #FFFF00?", "options": ["Белый", "Оранжевый", "Жёлтый", "Голубой"], "correct": 2, "explanation": "#FFFF00 — жёлтый (R=255, G=255, B=0)."},
        # 41-50: RGB продолжение, HSL
        {"question": "Какой цвет соответствует RGB #808080?", "options": ["Чёрный", "Серый", "Белый", "Тёмно-синий"], "correct": 1, "explanation": "#808080 — средний серый (R=128, G=128, B=128)."},
        {"question": "Какой цвет соответствует RGB #FFFFFF?", "options": ["Чёрный", "Серый", "Белый", "Красный"], "correct": 2, "explanation": "#FFFFFF — белый (все каналы максимальны: R=255, G=255, B=255)."},
        {"question": "Какой цвет соответствует RGB #000000?", "options": ["Чёрный", "Серый", "Белый", "Синий"], "correct": 0, "explanation": "#000000 — чёрный (все каналы нулевые: R=0, G=0, B=0)."},
        {"question": "RGB является аддитивной моделью. Что это означает?", "options": ["Цвета вычитаются для получения оттенка", "Цвета складываются из световых источников", "Используются только тёмные тона", "Цвета зависят от носителя печати"], "correct": 1, "explanation": "Аддитивная модель: цвета образуются смешением световых лучей (как в мониторе). Смешение всех = белый."},
        {"question": "Что такое HSL в контексте цвета?", "options": ["Hue, Saturation, Lightness", "High Speed Light", "Hex Scale Level", "Horizontal Spatial Layout"], "correct": 0, "explanation": "HSL — Hue (тон), Saturation (насыщенность), Lightness (светлота)."},
        {"question": "В каком диапазоне измеряется оттенок (Hue) в HSL?", "options": ["0-100", "0-255", "0-360 градусов", "0-1"], "correct": 2, "explanation": "Hue (тон) в HSL измеряется в градусах от 0 до 360 (цветовой круг)."},
        {"question": "Какому цвету соответствует Hue = 0 градусов в HSL?", "options": ["Зелёный", "Синий", "Красный", "Жёлтый"], "correct": 2, "explanation": "Hue 0 градусов (и 360) соответствует красному цвету."},
        {"question": "Какому цвету соответствует Hue = 120 градусов в HSL?", "options": ["Красный", "Зелёный", "Синий", "Жёлтый"], "correct": 1, "explanation": "Hue 120 градусов соответствует зелёному цвету."},
        {"question": "Какому цвету соответствует Hue = 240 градусов в HSL?", "options": ["Красный", "Зелёный", "Синий", "Фиолетовый"], "correct": 2, "explanation": "Hue 240 градусов соответствует синему цвету."},
        {"question": "Какому цвету соответствует Hue = 60 градусов в HSL?", "options": ["Оранжевый", "Жёлтый", "Голубой", "Пурпурный"], "correct": 1, "explanation": "Hue 60 градусов соответствует жёлтому цвету."},
        # 51-60: CMYK, HSV, LAB, Pantone
        {"question": "Что такое CMYK?", "options": ["Cyan, Magenta, Yellow, Key (Black)", "Color Mode Yellow Kinetics", "Cyan, Maroon, Yellow, Khaki", "Creative Mix Your Kontours"], "correct": 0, "explanation": "CMYK — Cyan, Magenta, Yellow, Key (Black) — субтрактивная модель для печати."},
        {"question": "Что означает K в CMYK?", "options": ["Kolor (цвет)", "Key (чёрный)", "Khaki (хаки)", "Killer (яркость)"], "correct": 1, "explanation": "K в CMYK означает Key (чёрный) — ключевой цвет в полиграфии."},
        {"question": "Для чего используется CMYK?", "options": ["Для отображения на экране", "Для полиграфической печати", "Для видеопроизводства", "Для 3D-рендеринга"], "correct": 1, "explanation": "CMYK используется в полиграфии — при смешении красок на бумаге (субтрактивная модель)."},
        {"question": "CMYK является субтрактивной моделью. Что это означает?", "options": ["Цвета добавляются как свет", "Цвета вычитаются из белого (бумаги) при смешении красок", "Количество цветов ограничено", "Применяется только для цифрового контента"], "correct": 1, "explanation": "Субтрактивная: каждая краска поглощает часть спектра. Смешение всех красок даёт чёрный."},
        {"question": "Что такое HSV?", "options": ["Hue, Saturation, Value", "High Spectrum Video", "Hue, Shade, Vivid", "Horizontal Slice View"], "correct": 0, "explanation": "HSV — Hue (тон), Saturation (насыщенность), Value (яркость)."},
        {"question": "Где применяется HSV модель?", "options": ["В полиграфии", "В графических редакторах (Photoshop, GIMP)", "В телевидении", "В 3D-печати"], "correct": 1, "explanation": "HSV широко используется в графических редакторах для удобного выбора цвета."},
        {"question": "Что такое цветовая модель LAB?", "options": ["Light, Alpha, Blue", "Перцептуальная модель с каналами L*, a*, b*", "Linear Adobe Base", "Low Alpha Bridge"], "correct": 1, "explanation": "LAB (CIE L*a*b*) — перцептуальная модель: L* = светлота, a* = зелёный/красный, b* = синий/жёлтый."},
        {"question": "В каком году принята модель CIE LAB?", "options": ["1966", "1976", "1986", "1996"], "correct": 1, "explanation": "CIE LAB принята Международной комиссией по освещению (CIE) в 1976 году."},
        {"question": "Что делает LAB независимой от устройств моделью?", "options": ["Использует только 3 цвета", "Основана на восприятии человеческого глаза, а не характеристиках устройства", "Разработана для конкретного монитора", "Использует бесконечное число оттенков"], "correct": 1, "explanation": "LAB описывает цвет в терминах человеческого восприятия — поэтому не зависит от конкретного устройства."},
        {"question": "Для чего используется система Pantone?", "options": ["Отображение цвета на экране", "Стандартизация цветов в полиграфии", "Кодирование пикселей", "Хранение цветовых профилей"], "correct": 1, "explanation": "Pantone — система стандартизации цветов, используется в полиграфии для точного воспроизведения цвета."},
        # 61-70: Pantone, Alpha, PNG/JPG
        {"question": "В каком году основана компания Pantone?", "options": ["1953", "1963", "1973", "1983"], "correct": 1, "explanation": "Pantone Inc. основана в 1963 году."},
        {"question": "Что такое альфа-канал (alpha channel)?", "options": ["Яркость цвета", "Прозрачность пикселя", "Насыщенность цвета", "Первый канал RGB"], "correct": 1, "explanation": "Альфа-канал определяет прозрачность пикселя: 0 = полностью прозрачный, 1 (или 255) = полностью непрозрачный."},
        {"question": "Какой формат изображений поддерживает прозрачность (альфа-канал)?", "options": ["JPEG (JPG)", "BMP", "PNG", "GIF только"], "correct": 2, "explanation": "PNG поддерживает прозрачность через альфа-канал. JPEG не поддерживает прозрачность."},
        {"question": "Какой формат НЕ поддерживает прозрачность?", "options": ["PNG", "GIF", "JPEG", "WebP"], "correct": 2, "explanation": "JPEG (JPG) не поддерживает прозрачность — фон всегда заполняется цветом."},
        {"question": "Что такое RGBA?", "options": ["RGB с добавлением альфа-канала (прозрачности)", "Расширенный RGB с 4 цветами", "Формат видеофайла", "Разновидность CMYK"], "correct": 0, "explanation": "RGBA = Red, Green, Blue, Alpha — RGB с четвёртым каналом прозрачности."},
        {"question": "Чему равен альфа-канал у полностью прозрачного пикселя (диапазон 0-1)?", "options": ["1", "0.5", "0", "255"], "correct": 2, "explanation": "Alpha = 0 означает полную прозрачность (невидимый пиксель)."},
        {"question": "Чему равен альфа-канал у полностью непрозрачного пикселя (диапазон 0-1)?", "options": ["0", "0.5", "1", "100"], "correct": 2, "explanation": "Alpha = 1 (или 255 в диапазоне 0-255) означает полную непрозрачность."},
        {"question": "Какое минимальное соотношение контрастности требует WCAG AA для обычного текста?", "options": ["2:1", "3:1", "4.5:1", "7:1"], "correct": 2, "explanation": "WCAG 2.1 уровень AA требует минимум 4.5:1 для обычного текста (3:1 для крупного)."},
        {"question": "Что такое CSS-фреймворк Bootstrap?", "options": ["Серверный фреймворк", "Готовый набор CSS-стилей и компонентов для вёрстки", "JavaScript библиотека", "Графический редактор"], "correct": 1, "explanation": "Bootstrap — популярный CSS-фреймворк с готовыми компонентами для адаптивной вёрстки."},
        {"question": "Что такое Tailwind CSS?", "options": ["Компонентный CSS-фреймворк", "Utility-first CSS-фреймворк с атомарными классами", "Препроцессор CSS", "JavaScript библиотека"], "correct": 1, "explanation": "Tailwind CSS — utility-first фреймворк: вёрстка с помощью атомарных CSS-классов прямо в HTML."},
        # 71-80: Цветовые инструменты и концепции
        {"question": "Что такое градиент в веб-дизайне?", "options": ["Тип шрифта", "Плавный переход между двумя и более цветами", "Тип анимации", "CSS-фреймворк"], "correct": 1, "explanation": "Градиент — плавный переход от одного цвета к другому, создаётся через CSS свойство background."},
        {"question": "Что означает HEX-код цвета?", "options": ["Цвет в формате HSL", "Шестнадцатеричное представление RGB-цвета", "Яркость пикселя", "Тип цветового профиля"], "correct": 1, "explanation": "HEX-код (#RRGGBB) — шестнадцатеричное представление значений RGB каналов."},
        {"question": "Сколько символов в полном HEX-коде цвета?", "options": ["3", "4", "6", "8"], "correct": 2, "explanation": "Полный HEX-код цвета содержит 6 символов: 2 на каждый канал RGB (#RRGGBB)."},
        {"question": "Что такое векторная графика?", "options": ["Изображение из пикселей", "Изображение на основе математических кривых и фигур", "3D-модель", "Анимация"], "correct": 1, "explanation": "Векторная графика описывает изображение математически (линии, кривые) и масштабируется без потерь."},
        {"question": "Что такое растровая (пиксельная) графика?", "options": ["Изображение из математических кривых", "Изображение из сетки пикселей", "3D-объект", "Параметрическая модель"], "correct": 1, "explanation": "Растровая графика — изображение, состоящее из сетки пикселей (точек). JPEG, PNG — растровые форматы."},
        {"question": "Какой формат является векторным?", "options": ["JPEG", "PNG", "SVG", "BMP"], "correct": 2, "explanation": "SVG (Scalable Vector Graphics) — векторный формат, основанный на XML."},
        {"question": "Что такое DPI?", "options": ["Размер изображения в пикселях", "Количество точек на дюйм — характеристика разрешения", "Тип цветовой модели", "Формат файла"], "correct": 1, "explanation": "DPI — dots per inch, количество точек на дюйм — характеристика разрешения изображения."},
        {"question": "Что такое пиксель?", "options": ["Векторный элемент", "Минимальная единица растрового изображения", "Цветовая модель", "Единица измерения шрифта"], "correct": 1, "explanation": "Пиксель (pixel) — минимальный элемент растрового изображения или экрана."},
        {"question": "Что такое палитра цветов?", "options": ["Инструмент рисования", "Набор доступных цветов для использования", "Тип файла", "Настройка монитора"], "correct": 1, "explanation": "Палитра — набор (коллекция) цветов, из которых выбирают при создании дизайна."},
        {"question": "Что такое комплементарные (дополнительные) цвета?", "options": ["Цвета одного оттенка разной яркости", "Цвета, расположенные напротив друг друга на цветовом круге", "Оттенки серого", "Цвета, близкие по тону"], "correct": 1, "explanation": "Комплементарные цвета расположены напротив друг друга на цветовом круге (например, красный и зелёный)."},
        # 81-90: Инструменты дизайна и визуальные концепции
        {"question": "Что такое Figma?", "options": ["Язык программирования", "Онлайн-инструмент для UI/UX дизайна", "CSS-фреймворк", "CMS система"], "correct": 1, "explanation": "Figma — облачный инструмент для дизайна интерфейсов (UI/UX) с поддержкой совместной работы."},
        {"question": "Что такое Adobe Photoshop?", "options": ["Векторный редактор", "Растровый графический редактор", "Инструмент для прототипирования", "3D-редактор"], "correct": 1, "explanation": "Adobe Photoshop — профессиональный растровый графический редактор."},
        {"question": "Что такое Adobe Illustrator?", "options": ["Растровый редактор", "Векторный графический редактор", "Видеоредактор", "Инструмент для вёрстки"], "correct": 1, "explanation": "Adobe Illustrator — профессиональный векторный графический редактор."},
        {"question": "Что такое UI дизайн?", "options": ["User Intelligence Design", "User Interface Design (дизайн интерфейса)", "Unified Interaction Design", "Universal Input Design"], "correct": 1, "explanation": "UI — User Interface Design — проектирование визуального интерфейса пользователя."},
        {"question": "Что такое UX дизайн?", "options": ["User eXtreme Design", "User eXperience Design (дизайн пользовательского опыта)", "Universal eXchange Design", "Unified eXecution Design"], "correct": 1, "explanation": "UX — User Experience Design — проектирование пользовательского опыта взаимодействия."},
        {"question": "Что такое wireframe в дизайне?", "options": ["Готовый дизайн-макет", "Схематичный каркас интерфейса без деталей", "Финальный прототип", "CSS-шаблон"], "correct": 1, "explanation": "Wireframe — схематичный каркас (набросок) интерфейса, показывающий структуру без визуальных деталей."},
        {"question": "Что такое прототип в UI/UX?", "options": ["Готовый продукт", "Интерактивный макет для проверки концепции", "Код приложения", "Техническое задание"], "correct": 1, "explanation": "Прототип — интерактивный макет интерфейса для тестирования концепции до разработки."},
        {"question": "Что такое цветовая схема (color scheme)?", "options": ["Один цвет в разных оттенках", "Набор цветов, подобранных для совместного использования", "Настройка экрана", "Тип градиента"], "correct": 1, "explanation": "Цветовая схема — набор цветов, гармонично сочетающихся для использования в дизайне."},
        {"question": "Что такое типографика?", "options": ["Технология 3D-печати", "Искусство оформления шрифта и текста", "Тип анимации", "Метод кодирования"], "correct": 1, "explanation": "Типографика — искусство оформления текста: выбор шрифтов, размеров, межстрочных интервалов."},
        {"question": "Что такое em в CSS?", "options": ["Единица длины в пикселях", "Относительная единица, зависящая от размера шрифта родителя", "Тип шрифта", "Элемент HTML"], "correct": 1, "explanation": "em в CSS — относительная единица измерения: 1em = размер шрифта родительского элемента."},
        # 91-100: CSS и визуальные инструменты
        {"question": "Что такое rem в CSS?", "options": ["Пиксель на Retina-дисплее", "Относительная единица, зависящая от корневого шрифта (<html>)", "Тип медиазапроса", "Единица угла поворота"], "correct": 1, "explanation": "rem — root em — относительная единица: 1rem = размер шрифта корневого элемента html."},
        {"question": "Что такое CSS анимация?", "options": ["JavaScript-библиотека для анимации", "Изменение CSS свойств элемента во времени", "GIF-изображение", "Flash-элемент"], "correct": 1, "explanation": "CSS анимация — изменение CSS-свойств элемента во времени с помощью @keyframes."},
        {"question": "Что такое медиазапросы (media queries) в CSS?", "options": ["Запросы к API", "Условные правила CSS для разных размеров экрана", "SQL-запросы в базе данных", "HTTP-запросы"], "correct": 1, "explanation": "Media queries — условные CSS-правила, применяющиеся при определённых характеристиках устройства (ширина экрана)."},
        {"question": "Что такое CSS flexbox?", "options": ["Тип шрифта", "Модель одномерного выравнивания элементов", "Анимация", "Тип сетки"], "correct": 1, "explanation": "Flexbox — модель CSS для одномерного выравнивания элементов в строке или столбце."},
        {"question": "Что такое CSS Grid?", "options": ["Фреймворк Bootstrap", "Двумерная система вёрстки для строк и колонок", "Тип анимации", "JavaScript-библиотека"], "correct": 1, "explanation": "CSS Grid — двумерная система вёрстки, позволяющая размещать элементы по строкам и колонкам."},
        {"question": "Что такое CSS-препроцессор (SASS, LESS)?", "options": ["CSS-фреймворк", "Инструмент, расширяющий CSS переменными, вложенностью и функциями", "Библиотека анимаций", "Редактор кода"], "correct": 1, "explanation": "CSS-препроцессоры (SASS, LESS) добавляют к CSS переменные, вложенность, миксины и другие возможности."},
        {"question": "Что такое z-index в CSS?", "options": ["Размер шрифта", "Порядок наложения элементов по оси Z (глубина)", "Прозрачность элемента", "Тип позиционирования"], "correct": 1, "explanation": "z-index — CSS-свойство, определяющее порядок наложения позиционированных элементов (кто поверх кого)."},
        {"question": "Что такое opacity в CSS?", "options": ["Цвет фона", "Прозрачность всего элемента (0 = невидим, 1 = непрозрачен)", "Размер шрифта", "Отступ элемента"], "correct": 1, "explanation": "opacity — CSS-свойство прозрачности: 0 = полностью прозрачный, 1 = полностью непрозрачный."},
        {"question": "Что такое SVG?", "options": ["Scalable Vector Graphics", "Static Visual Generator", "Standard Video Graphics", "System Visual Grid"], "correct": 0, "explanation": "SVG — Scalable Vector Graphics (масштабируемая векторная графика), формат на основе XML."},
        {"question": "Какое преимущество SVG перед PNG?", "options": ["SVG поддерживает больше цветов", "SVG масштабируется без потери качества", "SVG меньше весит всегда", "SVG быстрее загружается"], "correct": 1, "explanation": "SVG — векторный формат, масштабируется без потери качества при любом размере экрана."},
    ],
    "variables": [
        # 1-10: Объявление переменных в JavaScript
        {"question": "Какое ключевое слово используется для объявления изменяемой переменной в современном JavaScript?", "options": ["var", "let", "dim", "set"], "correct": 1, "explanation": "let — современный способ объявить изменяемую переменную в JS (ES6+)."},
        {"question": "Что выведет этот код?\n```\nlet x = 5;\nx = 10;\nconsole.log(x);\n```", "options": ["5", "10", "undefined", "Ошибка"], "correct": 1, "explanation": "let позволяет переприсваивать значение, поэтому x станет 10."},
        {"question": "Что выведет этот код?\n```\nconst x = 5;\nconsole.log(x);\n```", "options": ["5", "undefined", "null", "Ошибка"], "correct": 0, "explanation": "const объявляет константу со значением 5, которое выводится без ошибок."},
        {"question": "Что произойдёт при выполнении этого кода?\n```\nconst x = 5;\nx = 10;\n```", "options": ["x станет 10", "x останется 5", "Будет ошибка TypeError", "x станет undefined"], "correct": 2, "explanation": "Попытка переприсвоить const вызывает TypeError: Assignment to constant variable."},
        {"question": "Что выведет этот код?\n```\nvar x = 1;\nvar x = 2;\nconsole.log(x);\n```", "options": ["1", "2", "Ошибка", "undefined"], "correct": 1, "explanation": "var позволяет повторно объявлять переменную — x перезапишется значением 2."},
        {"question": "Что выведет этот код?\n```\nconsole.log(x);\nvar x = 5;\n```", "options": ["5", "null", "undefined", "ReferenceError"], "correct": 2, "explanation": "var поднимается (hoisting), но без значения. До строки присваивания x === undefined."},
        {"question": "Что выведет этот код?\n```\nconsole.log(x);\nlet x = 5;\n```", "options": ["5", "undefined", "null", "ReferenceError"], "correct": 3, "explanation": "let также поднимается, но находится в 'temporal dead zone' до объявления — выбрасывается ReferenceError."},
        {"question": "Что выведет этот код?\n```\nlet a = '5';\nlet b = 3;\nconsole.log(a + b);\n```", "options": ["8", "'53'", "53", "Ошибка"], "correct": 2, "explanation": "Строка '5' + число 3: JS конвертирует b в строку, получается конкатенация '53'."},
        {"question": "Что выведет этот код?\n```\nlet a = 5;\nlet b = 3;\nconsole.log(a + b);\n```", "options": ["'53'", "53", "8", "Ошибка"], "correct": 2, "explanation": "Оба числа — операция сложения, результат 8."},
        {"question": "Что выведет этот код?\n```\nlet x = 2 ** 3;\nconsole.log(x);\n```", "options": ["6", "8", "9", "23"], "correct": 1, "explanation": "** — оператор возведения в степень в JS. 2 ** 3 = 8."},
        # 11-20: Типы данных и typeof в JS
        {"question": "Что выведет этот код?\n```\nlet x = 10 % 3;\nconsole.log(x);\n```", "options": ["3", "1", "0", "10"], "correct": 1, "explanation": "% — оператор остатка от деления. 10 % 3 = 1."},
        {"question": "Что выведет этот код?\n```\nconsole.log(typeof null);\n```", "options": ["'null'", "'undefined'", "'object'", "'number'"], "correct": 2, "explanation": "typeof null === 'object' — это исторический баг в JavaScript, существующий с 1995 года."},
        {"question": "Что выведет этот код?\n```\nlet x;\nconsole.log(typeof x);\n```", "options": ["'null'", "'undefined'", "'object'", "'void'"], "correct": 1, "explanation": "Переменная без значения имеет тип undefined."},
        {"question": "Что выведет этот код?\n```\nlet x = true;\nconsole.log(typeof x);\n```", "options": ["'bool'", "'boolean'", "'number'", "'string'"], "correct": 1, "explanation": "typeof true === 'boolean'."},
        {"question": "Что выведет этот код?\n```\nlet x = [1, 2, 3];\nconsole.log(typeof x);\n```", "options": ["'array'", "'list'", "'object'", "'number'"], "correct": 2, "explanation": "В JS массивы являются объектами, поэтому typeof [] === 'object'."},
        {"question": "Что выведет этот код?\n```\nlet x = 5;\nlet y = x;\nx = 10;\nconsole.log(y);\n```", "options": ["10", "5", "undefined", "Ошибка"], "correct": 1, "explanation": "Примитивы копируются по значению. y = 5 независимо от дальнейших изменений x."},
        {"question": "Что выведет этот код?\n```\nlet x = '5' == 5;\nconsole.log(x);\n```", "options": ["true", "false", "Ошибка", "undefined"], "correct": 0, "explanation": "== сравнивает с приведением типов: '5' преобразуется в 5, поэтому true."},
        {"question": "Что выведет этот код?\n```\nlet x = '5' === 5;\nconsole.log(x);\n```", "options": ["true", "false", "Ошибка", "undefined"], "correct": 1, "explanation": "=== строгое равенство без приведения типов: строка !== число, поэтому false."},
        {"question": "Что выведет этот код?\n```\nconsole.log(Boolean(0));\n```", "options": ["true", "false", "0", "undefined"], "correct": 1, "explanation": "0 — falsy значение в JS, Boolean(0) === false."},
        {"question": "Что выведет этот код?\n```\nlet x = null ?? 'default';\nconsole.log(x);\n```", "options": ["null", "'default'", "undefined", "Ошибка"], "correct": 1, "explanation": "?? (nullish coalescing): если левая сторона null или undefined — возвращает правую. Результат 'default'."},
        # 21-30: JavaScript — разное
        {"question": "Что выведет этот код?\n```\nconst arr = [1, 2, 3];\narr.push(4);\nconsole.log(arr.length);\n```", "options": ["3", "4", "Ошибка (const)", "undefined"], "correct": 1, "explanation": "const запрещает переприсвоение переменной, но не мутацию объекта/массива. arr.push(4) работает, длина = 4."},
        {"question": "Что выведет этот код?\n```\nlet x = 'hello';\nconsole.log(x[0]);\n```", "options": ["'hello'", "'h'", "undefined", "Ошибка"], "correct": 1, "explanation": "Строки в JS индексируются как массивы. x[0] === 'h'."},
        {"question": "Что выведет этот код?\n```\nlet x = 'hello';\nconsole.log(x.length);\n```", "options": ["4", "5", "6", "undefined"], "correct": 1, "explanation": "'hello' состоит из 5 символов, поэтому length === 5."},
        {"question": "Что выведет этот код?\n```\nlet x = parseInt('42abc');\nconsole.log(x);\n```", "options": ["NaN", "42", "Ошибка", "0"], "correct": 1, "explanation": "parseInt читает число до первого нечислового символа: '42abc' → 42."},
        {"question": "Что выведет этот код?\n```\nlet x = Number('abc');\nconsole.log(x);\n```", "options": ["0", "null", "NaN", "Ошибка"], "correct": 2, "explanation": "Number('abc') возвращает NaN — строка не является числом."},
        {"question": "Что выведет этот код?\n```\nconsole.log(0.1 + 0.2 === 0.3);\n```", "options": ["true", "false", "undefined", "Ошибка"], "correct": 1, "explanation": "Из-за погрешности IEEE 754: 0.1 + 0.2 = 0.30000000000000004 ≠ 0.3. Результат false."},
        {"question": "Что выведет этот код?\n```\nlet x;\nconsole.log(x);\n```", "options": ["null", "0", "undefined", "Ошибка"], "correct": 2, "explanation": "Переменная объявлена, но значение не присвоено — значение undefined."},
        {"question": "Сколько переменных объявлено в одной строке?\n```\nlet a = 1, b = 2, c = 3;\n```", "options": ["1", "2", "3", "Ошибка"], "correct": 2, "explanation": "JavaScript позволяет объявлять несколько переменных через запятую в одном let/var/const."},
        {"question": "Что выведет этот код?\n```\nlet x = 10;\nlet y = 3;\nconsole.log(Math.floor(x / y));\n```", "options": ["3", "3.33", "4", "0"], "correct": 0, "explanation": "Math.floor(10 / 3) = Math.floor(3.333...) = 3."},
        {"question": "Что выведет этот код?\n```\nlet [a, b] = [10, 20];\nconsole.log(a + b);\n```", "options": ["'1020'", "30", "Ошибка", "undefined"], "correct": 1, "explanation": "Деструктуризация массива: a=10, b=20. Оба числа, сумма = 30."},
        # 31-40: Python переменные
        {"question": "Как объявить переменную в Python?", "options": ["var x = 5", "int x = 5", "x = 5", "let x = 5"], "correct": 2, "explanation": "В Python не нужны ключевые слова для объявления — просто x = 5."},
        {"question": "Что выведет этот код?\n```python\nx = 5\ny = 3\nprint(x + y)\n```", "options": ["'53'", "8", "53", "Ошибка"], "correct": 1, "explanation": "Оба значения — целые числа, результат сложения 8."},
        {"question": "Что выведет этот код?\n```python\nx = 10\nx = 'hello'\nprint(x)\n```", "options": ["10", "'hello'", "hello", "Ошибка"], "correct": 2, "explanation": "Python динамически типизирован: x переопределяется как строку 'hello', print выводит hello."},
        {"question": "Что выведет этот код?\n```python\nx = 5\nprint(type(x))\n```", "options": ["int", "<class 'int'>", "5", "integer"], "correct": 1, "explanation": "type() в Python возвращает объект типа, выводится как <class 'int'>."},
        {"question": "Что выведет этот код?\n```python\nx = 2 ** 3\nprint(x)\n```", "options": ["6", "8", "9", "23"], "correct": 1, "explanation": "** — возведение в степень в Python. 2 ** 3 = 8."},
        {"question": "Что выведет этот код?\n```python\nx = 10 // 3\nprint(x)\n```", "options": ["3.33", "3", "4", "0"], "correct": 1, "explanation": "// — целочисленное (floor) деление в Python. 10 // 3 = 3."},
        {"question": "Что выведет этот код?\n```python\nx = 'ha' * 3\nprint(x)\n```", "options": ["'hahaha'", "hahaha", "Ошибка", "ha3"], "correct": 1, "explanation": "Умножение строки на число в Python повторяет её. 'ha' * 3 = 'hahaha'."},
        {"question": "Что выведет этот код?\n```python\na, b = 1, 2\nprint(a, b)\n```", "options": ["12", "1 2", "Ошибка", "(1, 2)"], "correct": 1, "explanation": "Множественное присваивание: a=1, b=2. print(a, b) выводит '1 2'."},
        {"question": "Что выведет этот код?\n```python\nx = 5\ny = x\nx = 10\nprint(y)\n```", "options": ["10", "5", "None", "Ошибка"], "correct": 1, "explanation": "Числа в Python — неизменяемые объекты. y ссылается на значение 5, изменение x не влияет на y."},
        {"question": "Что выведет этот код?\n```python\nx = int('42')\nprint(x + 1)\n```", "options": ["'421'", "421", "43", "Ошибка"], "correct": 2, "explanation": "int('42') преобразует строку в число 42, затем 42 + 1 = 43."},
        # 41-50: Python продолжение
        {"question": "Что выведет этот код?\n```python\nx = 0.1 + 0.2\nprint(x == 0.3)\n```", "options": ["True", "False", "Ошибка", "None"], "correct": 1, "explanation": "Погрешность IEEE 754: 0.1 + 0.2 = 0.30000000000000004 ≠ 0.3. Результат False."},
        {"question": "Что выведет этот код?\n```python\nx = None\nprint(x is None)\n```", "options": ["True", "False", "None", "Ошибка"], "correct": 0, "explanation": "None — специальное значение отсутствия. Проверка через is None возвращает True."},
        {"question": "Что выведет этот код?\n```python\nx = 'hello'\nprint(x[0])\n```", "options": ["'hello'", "h", "'h'", "Ошибка"], "correct": 1, "explanation": "Индексация строк в Python: x[0] — первый символ 'h'."},
        {"question": "Что выведет этот код?\n```python\nx = 'hello'\nprint(len(x))\n```", "options": ["4", "5", "6", "Ошибка"], "correct": 1, "explanation": "'hello' = 5 символов, len() возвращает 5."},
        {"question": "Что выведет этот код?\n```python\nprint(bool(0))\n```", "options": ["True", "False", "0", "None"], "correct": 1, "explanation": "В Python 0 — falsy значение. bool(0) === False."},
        {"question": "Что выведет этот код?\n```python\nprint(bool(5))\n```", "options": ["True", "False", "5", "None"], "correct": 0, "explanation": "Любое ненулевое число — truthy. bool(5) === True."},
        {"question": "Какое соглашение об именовании переменных принято в Python?", "options": ["camelCase", "PascalCase", "snake_case", "UPPER_CASE"], "correct": 2, "explanation": "PEP 8 рекомендует snake_case для переменных: my_variable, user_name."},
        {"question": "Что выведет этот код?\n```python\na = [1, 2, 3]\nb = a\na.append(4)\nprint(b)\n```", "options": ["[1, 2, 3]", "[1, 2, 3, 4]", "Ошибка", "None"], "correct": 1, "explanation": "Списки в Python — объекты. b = a создаёт ещё одну ссылку на тот же список. Изменение через a видно через b."},
        {"question": "Что выведет этот код?\n```python\nx = 10 % 3\nprint(x)\n```", "options": ["3", "1", "0", "3.3"], "correct": 1, "explanation": "% — остаток от деления. 10 % 3 = 1."},
        {"question": "Как в Python обменять значения двух переменных без третьей?", "options": ["a = b; b = a", "a, b = b, a", "swap(a, b)", "Нельзя без третьей"], "correct": 1, "explanation": "В Python можно a, b = b, a — множественное присваивание с распаковкой кортежа."},
        # 51-60: PHP переменные
        {"question": "С какого символа начинаются все переменные в PHP?", "options": ["@", "#", "$", "%"], "correct": 2, "explanation": "В PHP все переменные начинаются с символа $: $name, $count, $x."},
        {"question": "Что выведет этот код?\n```php\n$x = 5;\n$y = 3;\necho $x + $y;\n```", "options": ["53", "8", "'53'", "Ошибка"], "correct": 1, "explanation": "Оба значения — числа, echo выведет сумму 8."},
        {"question": "Что выведет этот код?\n```php\n$x = '5';\n$y = 3;\necho $x + $y;\n```", "options": ["'53'", "53", "8", "Ошибка"], "correct": 2, "explanation": "PHP автоматически преобразует строку '5' в число при арифметических операциях. Результат 8."},
        {"question": "Что выведет этот код?\n```php\n$x = true;\necho $x;\n```", "options": ["true", "1", "false", "Ошибка"], "correct": 1, "explanation": "PHP конвертирует true в 1 при выводе через echo."},
        {"question": "Что выведет этот код?\n```php\n$x = false;\necho $x;\n```", "options": ["false", "0", "'' (пустая строка)", "null"], "correct": 2, "explanation": "PHP конвертирует false в пустую строку '' при выводе через echo."},
        {"question": "Как проверить тип переменной в PHP?", "options": ["typeof($x)", "type($x)", "gettype($x)", "$x.type"], "correct": 2, "explanation": "gettype() возвращает тип переменной: 'integer', 'string', 'boolean' и т.д."},
        {"question": "Что выведет этот код?\n```php\n$x = 5;\necho gettype($x);\n```", "options": ["'int'", "integer", "number", "int"], "correct": 1, "explanation": "gettype(5) возвращает строку 'integer' в PHP."},
        {"question": "Как объявить константу в PHP?", "options": ["const $NAME = 5;", "define('NAME', 5);", "const NAME = 5;", "define или const (оба верны)"], "correct": 3, "explanation": "В PHP константу можно объявить через define('NAME', 5) или const NAME = 5 (в классах/глобально)."},
        {"question": "Начинаются ли константы в PHP с символа $?", "options": ["Да", "Нет", "Зависит от объявления", "Только глобальные"], "correct": 1, "explanation": "Константы в PHP не используют $. define('PI', 3.14) — обращение через PI, не $PI."},
        {"question": "Что выведет этот код?\n```php\n$x = 2 ** 3;\necho $x;\n```", "options": ["6", "8", "9", "Ошибка"], "correct": 1, "explanation": "** — оператор возведения в степень в PHP (с версии 5.6). 2 ** 3 = 8."},
        # 61-70: Java/C# переменные
        {"question": "Как объявить целочисленную переменную в Java?", "options": ["var x = 5;", "int x = 5;", "integer x = 5;", "x = 5;"], "correct": 1, "explanation": "В Java нужно явно указывать тип: int x = 5;"},
        {"question": "Что выведет этот код?\n```java\nint x = 10 / 3;\nSystem.out.println(x);\n```", "options": ["3.33", "3", "4", "Ошибка"], "correct": 1, "explanation": "Целочисленное деление в Java: 10 / 3 = 3 (дробная часть отбрасывается)."},
        {"question": "Что выведет этот код?\n```java\ndouble x = 10.0 / 3;\nSystem.out.println(x);\n```", "options": ["3", "3.3333333333333335", "3.33", "Ошибка"], "correct": 1, "explanation": "Деление двойной точности: 10.0 / 3 = 3.3333333333333335."},
        {"question": "Как объявить константу в Java?", "options": ["const int X = 5;", "final int X = 5;", "static int X = 5;", "readonly int X = 5;"], "correct": 1, "explanation": "В Java константы объявляются через final: final int X = 5;"},
        {"question": "Что означает ключевое слово final у переменной в Java?", "options": ["Переменная статическая", "Переменная публичная", "Значение нельзя изменить после присваивания", "Переменная будет удалена"], "correct": 2, "explanation": "final у переменной означает, что значение нельзя переприсвоить после первоначального присваивания."},
        {"question": "Какой тип данных используется для текстовых строк в Java?", "options": ["string", "String", "text", "char[]"], "correct": 1, "explanation": "В Java строки — объекты класса String (с заглавной буквы)."},
        {"question": "Как в Java 10+ объявить переменную без явного указания типа?", "options": ["auto x = 5;", "let x = 5;", "var x = 5;", "dynamic x = 5;"], "correct": 2, "explanation": "Java 10+ поддерживает var для вывода типа: var x = 5; (компилятор выведет int)."},
        {"question": "Что выведет этот код?\n```java\nint x = 2 + 3 * 4;\nSystem.out.println(x);\n```", "options": ["20", "14", "24", "Ошибка"], "correct": 1, "explanation": "Приоритет операций: умножение выполняется первым. 3 * 4 = 12, затем 2 + 12 = 14."},
        {"question": "Как объявить переменную в C# с автовыводом типа?", "options": ["auto x = 5;", "let x = 5;", "var x = 5;", "dynamic x = 5;"], "correct": 2, "explanation": "В C# var позволяет компилятору вывести тип автоматически: var x = 5; компилятор поймёт, что это int."},
        {"question": "Как объявить константу в C#?", "options": ["final int x = 5;", "readonly int x = 5;", "const int x = 5;", "static int x = 5;"], "correct": 2, "explanation": "В C# константы объявляются через const: const int x = 5;"},
        # 71-80: Go, Ruby, Swift — переменные
        {"question": "Как объявить переменную в Go с кратким синтаксисом?", "options": ["var x = 5", "x := 5", "let x = 5", "x = 5"], "correct": 1, "explanation": "В Go := — краткое объявление переменной с выводом типа. Эквивалентно var x int = 5."},
        {"question": "Нужно ли указывать тип при использовании := в Go?", "options": ["Да, обязательно", "Нет, тип выводится автоматически", "Только для чисел", "Зависит от пакета"], "correct": 1, "explanation": "При := компилятор Go выводит тип из правой части выражения."},
        {"question": "Как объявить константу в Go?", "options": ["final x = 5", "const x = 5", "readonly x = 5", "let x = 5"], "correct": 1, "explanation": "В Go константы объявляются через const: const x = 5."},
        {"question": "Что произойдёт в Go, если объявить переменную и не использовать её?", "options": ["Предупреждение при компиляции", "Ошибка компиляции", "Ничего", "Переменная удаляется"], "correct": 1, "explanation": "Go не компилирует код с неиспользуемыми переменными — это ошибка компиляции."},
        {"question": "Как объявить переменную в Ruby?", "options": ["var x = 5", "int x = 5", "x = 5", "let x = 5"], "correct": 2, "explanation": "В Ruby, как и в Python, переменная объявляется простым присваиванием: x = 5."},
        {"question": "Как обозначаются глобальные переменные в Ruby?", "options": ["@@x", "@x", "$x", "#x"], "correct": 2, "explanation": "В Ruby глобальные переменные начинаются с $: $global_var."},
        {"question": "Как обозначаются переменные экземпляра (instance variables) в Ruby?", "options": ["$x", "@@x", "@x", "#x"], "correct": 2, "explanation": "В Ruby переменные экземпляра начинаются с @: @instance_var."},
        {"question": "Как объявить константу в Swift?", "options": ["final x = 5", "const x = 5", "let x = 5", "var x = 5"], "correct": 2, "explanation": "В Swift let объявляет константу (неизменяемую), var — переменную."},
        {"question": "Как объявить изменяемую переменную в Swift?", "options": ["let x = 5", "var x = 5", "mut x = 5", "mutable x = 5"], "correct": 1, "explanation": "В Swift var объявляет изменяемую переменную: var x = 5."},
        {"question": "Как объявить переменную в Kotlin?", "options": ["int x = 5", "x := 5", "val x = 5 или var x = 5", "let x = 5"], "correct": 2, "explanation": "В Kotlin val — неизменяемая (аналог const/final), var — изменяемая переменная."},
        # 81-90: Общие концепции переменных
        {"question": "Что такое динамическая типизация?", "options": ["Тип определяется в момент компиляции", "Тип определяется и может меняться во время выполнения", "Переменная без типа", "Автоматическое удаление переменных"], "correct": 1, "explanation": "При динамической типизации (Python, JS) тип переменной определяется во время выполнения и может меняться."},
        {"question": "Что такое статическая типизация?", "options": ["Тип определяется во время выполнения", "Тип определяется при компиляции и не может измениться", "Все переменные одного типа", "Переменные нельзя менять"], "correct": 1, "explanation": "При статической типизации (Java, C#, Go) тип задаётся при объявлении и проверяется компилятором."},
        {"question": "Может ли имя переменной начинаться с цифры в большинстве языков?", "options": ["Да", "Нет", "Только в Python", "Только в JS"], "correct": 1, "explanation": "В большинстве языков имя переменной не может начинаться с цифры (1x — ошибка, x1 — норма)."},
        {"question": "Что такое camelCase?", "options": ["first_word_small_next_capital", "firstWordSmallNextCapital", "FirstWordCapital", "ALL_CAPS"], "correct": 1, "explanation": "camelCase: первое слово строчными, каждое следующее с заглавной буквы: myVariableName."},
        {"question": "Что такое PascalCase?", "options": ["firstWordSmall", "first_word_small", "FirstWordCapital", "ALL_CAPS"], "correct": 2, "explanation": "PascalCase: каждое слово начинается с заглавной буквы: MyVariableName. Используется для классов."},
        {"question": "Что такое SCREAMING_SNAKE_CASE?", "options": ["firstWordSmall", "FirstWordCapital", "first_word_small", "ALL_WORDS_UPPERCASE_WITH_UNDERSCORES"], "correct": 3, "explanation": "SCREAMING_SNAKE_CASE: всё заглавными буквами через подчёркивание. Используется для констант: MAX_SIZE."},
        {"question": "Что такое область видимости (scope) переменной?", "options": ["Тип данных переменной", "Область кода, в которой переменная доступна", "Размер занимаемой памяти", "Скорость доступа к переменной"], "correct": 1, "explanation": "Scope — область кода, в которой объявленная переменная доступна и может быть использована."},
        {"question": "Чем локальная переменная отличается от глобальной?", "options": ["Локальная быстрее", "Локальная видна только внутри функции, глобальная — везде", "Локальная занимает меньше памяти", "Нет разницы"], "correct": 1, "explanation": "Локальная переменная объявляется и видна только внутри функции/блока. Глобальная — во всей программе."},
        {"question": "Что такое присваивание (assignment)?", "options": ["Объявление переменной", "Запись значения в переменную", "Сравнение двух переменных", "Удаление переменной"], "correct": 1, "explanation": "Присваивание — операция записи значения в переменную: x = 5."},
        {"question": "Какие символы обычно допустимы в именах переменных?", "options": ["Только буквы", "Буквы, цифры и пробелы", "Буквы, цифры и подчёркивание (не начиная с цифры)", "Любые символы"], "correct": 2, "explanation": "В большинстве языков: буквы, цифры, подчёркивание. Начинаться может с буквы или _."},
        # 91-100: Смешанные вопросы и код
        {"question": "Что выведет этот код?\n```python\nx = 'hello'\ny = 'world'\nprint(x + ' ' + y)\n```", "options": ["helloworld", "hello world", "Ошибка", "'hello world'"], "correct": 1, "explanation": "Конкатенация строк: 'hello' + ' ' + 'world' = 'hello world'."},
        {"question": "Что выведет этот код?\n```javascript\nlet x = 5;\nlet y = '5';\nconsole.log(x == y, x === y);\n```", "options": ["true true", "false false", "true false", "false true"], "correct": 2, "explanation": "== с приведением типов: 5 == '5' → true. === строгое: 5 !== '5' → false."},
        {"question": "Что выведет этот код?\n```python\nx = 5\nprint(f'Значение: {x}')\n```", "options": ["Значение: {x}", "Значение: x", "Значение: 5", "Ошибка"], "correct": 2, "explanation": "f-строки в Python подставляют значение переменной: f'Значение: {x}' → 'Значение: 5'."},
        {"question": "Что выведет этот код?\n```javascript\nlet x = 5;\nconsole.log(`Значение: ${x}`);\n```", "options": ["Значение: ${x}", "Значение: x", "Значение: 5", "Ошибка"], "correct": 2, "explanation": "Шаблонные строки (template literals) в JS: `${x}` подставляет значение переменной."},
        {"question": "Какой результат у этого Python кода?\n```python\nx = 'Python'\nprint(x.upper())\n```", "options": ["python", "Python", "PYTHON", "Ошибка"], "correct": 2, "explanation": ".upper() возвращает строку в верхнем регистре: 'Python'.upper() = 'PYTHON'."},
        {"question": "Что выведет этот код?\n```python\nx = [1, 2, 3]\nprint(x[-1])\n```", "options": ["Ошибка", "1", "3", "None"], "correct": 2, "explanation": "Отрицательные индексы в Python: x[-1] — последний элемент, то есть 3."},
        {"question": "В каком языке объявление переменной выглядит как $name = value?", "options": ["Python", "JavaScript", "PHP", "Ruby"], "correct": 2, "explanation": "Синтаксис $name = value специфичен для PHP."},
        {"question": "В каком языке для объявления переменной используется :=?", "options": ["Kotlin", "Swift", "Go", "Rust"], "correct": 2, "explanation": "Оператор := для краткого объявления переменной используется в Go."},
        {"question": "Что такое null/None/nil в программировании?", "options": ["Ноль (число)", "Пустая строка", "Отсутствие значения / пустая ссылка", "Ложное булево значение"], "correct": 2, "explanation": "null (JS/Java), None (Python), nil (Go/Ruby) — специальные значения, обозначающие отсутствие значения."},
        {"question": "Что выведет этот код?\n```python\nx = 10\ny = 3\nprint(x / y)\n```", "options": ["3", "3.3333333333333335", "3.33", "Ошибка"], "correct": 1, "explanation": "В Python 3 / всегда возвращает float: 10 / 3 = 3.3333333333333335. Для целочисленного — //."},
    ],
}


def make_progress_bar(current, total):
    filled = int((current / total) * 10)
    return f"[{'▓' * filled}{'░' * (10 - filled)}]"


def get_category_keyboard():
    keyboard = [
        [InlineKeyboardButton("📚 Языки программирования", callback_data="cat_languages")],
        [InlineKeyboardButton("🌐 Сети, браузеры, серверы", callback_data="cat_networks")],
        [InlineKeyboardButton("🎨 Визуальные языки и цвета", callback_data="cat_visual")],
        [InlineKeyboardButton("🔢 Переменные и синтаксис", callback_data="cat_variables")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_mode_keyboard():
    keyboard = [
        [InlineKeyboardButton("🎲 20 случайных вопросов", callback_data="mode_20")],
        [InlineKeyboardButton("📋 Полный проход (100 вопросов)", callback_data="mode_100")],
        [InlineKeyboardButton("◀️ Назад", callback_data="menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {}
    await update.message.reply_text(
        "👋 <b>Добро пожаловать в Quiz Bot!</b>\n\nВыберите категорию для тестирования:",
        parse_mode="HTML",
        reply_markup=get_category_keyboard(),
    )


async def show_menu(query):
    await query.edit_message_text(
        "🏠 <b>Главное меню</b>\n\nВыберите категорию:",
        parse_mode="HTML",
        reply_markup=get_category_keyboard(),
    )


async def choose_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    category = query.data[4:]  # strip "cat_"

    user_data[user_id] = {"category": category}
    cat_name = CATEGORY_NAMES[category]

    await query.edit_message_text(
        f"Выбрана категория: <b>{cat_name}</b>\n\nВыберите режим прохождения:",
        parse_mode="HTML",
        reply_markup=get_mode_keyboard(),
    )


async def choose_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    mode = int(query.data[5:])  # strip "mode_"

    category = user_data[user_id]["category"]
    if mode == 20:
        questions_to_ask = random.sample(list(range(100)), 20)
    else:
        questions_to_ask = list(range(100))

    user_data[user_id] = {
        "category": category,
        "mode": mode,
        "questions_to_ask": questions_to_ask,
        "current_question": 0,
        "score": 0,
        "answers": [],
    }

    await send_question(query, user_id)


async def send_question(query, user_id):
    data = user_data[user_id]
    idx = data["current_question"]
    q_idx = data["questions_to_ask"][idx]
    total = len(data["questions_to_ask"])
    q = QUESTIONS_DATABASE[data["category"]][q_idx]

    progress = make_progress_bar(idx, total)
    header = f"<b>Вопрос {idx + 1}/{total}</b>  {progress}\n\n"

    keyboard = [
        [InlineKeyboardButton(f"{chr(65 + i)}. {opt}", callback_data=f"ans_{i}")]
        for i, opt in enumerate(q["options"])
    ]

    await query.edit_message_text(
        header + q["question"],
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def answer_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if user_id not in user_data or "questions_to_ask" not in user_data[user_id]:
        await query.edit_message_text("Сессия устарела. Нажмите /start для начала.")
        return

    data = user_data[user_id]
    ans = int(query.data[4:])  # strip "ans_"
    idx = data["current_question"]
    q_idx = data["questions_to_ask"][idx]
    q = QUESTIONS_DATABASE[data["category"]][q_idx]
    correct = q["correct"]
    total = len(data["questions_to_ask"])

    is_correct = ans == correct
    if is_correct:
        data["score"] += 1

    data["answers"].append({
        "question": q["question"],
        "your_answer": ans,
        "correct_answer": correct,
        "options": q["options"],
        "explanation": q["explanation"],
        "is_correct": is_correct,
    })

    result_icon = "✅" if is_correct else "❌"
    if is_correct:
        result_text = "Верно!"
    else:
        result_text = f"Неверно! Правильный ответ: <b>{chr(65 + correct)}. {q['options'][correct]}</b>"
    feedback = f"{result_icon} {result_text}\n\n💡 {q['explanation']}"

    data["current_question"] += 1

    if data["current_question"] >= total:
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("📊 Результаты", callback_data="show_results_now")]])
        await query.edit_message_text(feedback, parse_mode="HTML", reply_markup=keyboard)
    else:
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("➡️ Следующий вопрос", callback_data="next_question")]])
        await query.edit_message_text(feedback, parse_mode="HTML", reply_markup=keyboard)


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    cb = query.data

    if cb == "menu":
        user_data[user_id] = {}
        await show_menu(query)

    elif cb == "next_question":
        await send_question(query, user_id)

    elif cb == "show_results_now":
        await show_results(query, user_id)

    elif cb == "restart_20":
        category = user_data[user_id].get("category", "languages")
        user_data[user_id] = {
            "category": category,
            "mode": 20,
            "questions_to_ask": random.sample(list(range(100)), 20),
            "current_question": 0,
            "score": 0,
            "answers": [],
        }
        await send_question(query, user_id)

    elif cb == "restart_100":
        category = user_data[user_id].get("category", "languages")
        user_data[user_id] = {
            "category": category,
            "mode": 100,
            "questions_to_ask": list(range(100)),
            "current_question": 0,
            "score": 0,
            "answers": [],
        }
        await send_question(query, user_id)

    elif cb == "show_answers":
        await show_detailed_answers(query, user_id)


async def show_results(query, user_id):
    data = user_data[user_id]
    score = data["score"]
    total = len(data["questions_to_ask"])
    cat_name = CATEGORY_NAMES[data["category"]]
    mode = data["mode"]

    pct = int(score / total * 100)
    if pct >= 90:
        grade = "🏆 Отлично!"
    elif pct >= 70:
        grade = "👍 Хорошо!"
    elif pct >= 50:
        grade = "📚 Неплохо, но есть куда расти"
    else:
        grade = "💪 Нужно повторить материал"

    progress_bar = make_progress_bar(score, total)
    mode_label = "20 случайных" if mode == 20 else "100 вопросов"

    text = (
        f"📊 <b>Результаты теста</b>\n\n"
        f"📁 Категория: {cat_name}\n"
        f"🎯 Режим: {mode_label}\n\n"
        f"Правильных ответов: <b>{score}/{total}</b>  {progress_bar}\n"
        f"Результат: <b>{pct}%</b>\n\n"
        f"{grade}"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎲 Пройти снова (20 вопросов)", callback_data="restart_20")],
        [InlineKeyboardButton("📋 Полный проход (100 вопросов)", callback_data="restart_100")],
        [InlineKeyboardButton("🔍 Посмотреть ответы", callback_data="show_answers")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="menu")],
    ])

    await query.edit_message_text(text, parse_mode="HTML", reply_markup=keyboard)


async def show_detailed_answers(query, user_id):
    data = user_data[user_id]
    answers = data["answers"]
    lines = ["📝 <b>Разбор ответов:</b>\n"]

    for i, a in enumerate(answers, 1):
        icon = "✅" if a["is_correct"] else "❌"
        your = chr(65 + a["your_answer"])
        correct = chr(65 + a["correct_answer"])
        lines.append(f"{icon} <b>Вопрос {i}:</b> {a['question']}")
        if not a["is_correct"]:
            lines.append(f"   Ваш ответ: {your}. {a['options'][a['your_answer']]}")
            lines.append(f"   Правильно: {correct}. {a['options'][a['correct_answer']]}")
        lines.append(f"   💡 {a['explanation']}\n")

    full_text = "\n".join(lines)
    if len(full_text) > 4000:
        full_text = full_text[:3950] + "\n\n<i>...список обрезан из-за ограничений Telegram</i>"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎲 Пройти снова (20 вопросов)", callback_data="restart_20")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="menu")],
    ])
    await query.edit_message_text(full_text, parse_mode="HTML", reply_markup=keyboard)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(choose_category, pattern=r"^cat_"))
    app.add_handler(CallbackQueryHandler(choose_mode, pattern=r"^mode_"))
    app.add_handler(CallbackQueryHandler(answer_question, pattern=r"^ans_"))
    app.add_handler(CallbackQueryHandler(handle_callback, pattern=r"^(menu|next_question|show_results_now|restart_20|restart_100|show_answers)$"))

    logger.info("Bot started")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
