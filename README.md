# poly_an
 
Микросервис реализованный для хранения положения объектов с описанием.
Проект заточен под быстрый поиск рядом стоящих элементов (ближайших объектов в радиусе объекта) и рассчитан на большое количество точек. Поскольку реализация поиска при помощи грубого перебора слишком медленная, приходится избегать прямого сравнения введенной точки с остальными. Решение заключается в применении разновидности древовидных алгоритмов - R-дерева.

Для хранения точек плоскость делится на области. Каждая область также делится на области при увеличении количества точек более определенного порога - в итоге получится серия вложенных пространств, в конце которой будут находится точки в малом количестве.

Для поиска центральная точка не сравнивается со всеми точками в базе, напротив находятся области, которые охвачены поисковым радиусом, внутри данных областей процедура повторяется и так пока алгоритм не придёт к финальным областям, которые в свою очередь содержат потенциально близкие точки.

![Image alt](https://github.com/Konsyl/poly_an/blob/master/tree.png)

REST api реализован на Django REST framework вместе с использованием PostgreSQL
