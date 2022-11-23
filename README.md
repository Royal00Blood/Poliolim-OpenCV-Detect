# Poliolim-OpenCV-Detect

Программа предназначена для определения взаимного положения неких целевых объектов-точек и подвижного объекта-робота.

Для использования приложения ознакомтесь с базовым алгоритмом действий, выполнение которого является обязательным условием работоспособности программы.
---
1. Проведите настройку чернобелого фильтра , изменяя бегунками значения, пока искомый контрастный элемент не станет единственным белым обьектом на видео.
2. Для выхода из настроек контраста нажмите "ESC".
3. Введите в консоли колличество точек, которые ваш подвижный обьект будет пытаться достичь.
4. После появления окна с видео, кликните курсором на обьекты или точки, которые вам необходимо достичь.
    * Координаты выбранных точек автоматически запишутся в массив, который можно получить по запросу.
    * Опциональная функция, после обозначения точек вам будет предложено отметить обьект отслеживания на видео, либо воспользоваться автоматическим определением его местонахождения на основе исторических изображений.
5. Результатом верного выполнения выше изложенных пунктов является верное выделение вашего обьекта(контрастного изображения в видео потоке).

## Контрастный обьект должен быть однотонным и отличным от отенков чернобелого.


