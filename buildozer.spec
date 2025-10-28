[app]
# Название приложения
title = CaseDotka

# Имя пакета (латиницей, без пробелов), например: casedotka
package.name = casedotka

# Домен вашего приложения, можно оставить так
package.domain = org.casedotka

# Версия приложения
version = 1.0

# Папка, где лежит main.py и mykv.kv (обычно это просто точка)
source.dir = .

# Включаемые расширения
source.include_exts = py,kv,png,jpg,ttf,txt,md

# Требуемые библиотеки для Python
requirements = python3,kivy,kivymd,pyjnius

# Ориентация экрана
orientation = portrait

# Полноэкранный режим
fullscreen = 1

# Минимальные разрешения (по желанию)
android.permissions = INTERNET

# Фоновый цвет
window.clearcolor = (0.12, 0.12, 0.18, 1)
