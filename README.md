# Python Tetris

Una implementación moderna del clásico juego Tetris usando Pygame. Este proyecto incluye características adicionales como sistema de puntuación, niveles dinámicos, visualización de la siguiente pieza y pieza fantasma.

## 🎮 Características

- Sistema de puntuación completo con combos
- Niveles dinámicos que aumentan la dificultad
- Panel de información con estadísticas en tiempo real
- Previsualización de la siguiente pieza
- Pieza fantasma para ayudar en la colocación
- Sistema de pausa
- Controles intuitivos

## 🛠️ Requisitos

- Python 3.x
- Pygame

## ⚙️ Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/tu-usuario/python-tetris.git
cd python-tetris
```

2. Instala las dependencias:
```bash
pip install pygame
```

## 🎯 Cómo jugar

Ejecuta el juego con:
```bash
python main.py
```

### Controles:

- **←/→**: Mover pieza izquierda/derecha
- **↑**: Rotar pieza
- **↓**: Acelerar caída
- **Espacio**: Caída instantánea
- **P**: Pausar/Reanudar juego
- **H**: Mostrar/Ocultar pieza fantasma

### Sistema de Puntuación:

- 1 línea: 40 puntos × nivel
- 2 líneas: 100 puntos × nivel
- 3 líneas: 300 puntos × nivel
- 4 líneas: 1200 puntos × nivel
- Bonus por combo: +10% por cada línea consecutiva

## 🎲 Características del Juego

### Panel de Información
- Nivel actual
- Puntuación
- Líneas eliminadas
- Total de piezas usadas
- Mejor combo
- Combo actual
- Tiempo de juego
- Previsualización de siguiente pieza

### Niveles
- La velocidad aumenta cada 10 líneas completadas
- Los puntos se multiplican por el nivel actual
- La velocidad máxima se alcanza en niveles avanzados

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes:

1. Haz fork del repositorio
2. Crea una nueva rama (`git checkout -b feature/nueva-caracteristica`)
3. Realiza tus cambios
4. Haz commit de tus cambios (`git commit -am 'Agrega nueva característica'`)
5. Haz push a la rama (`git push origin feature/nueva-caracteristica`)
6. Abre un Pull Request

## 📝 Licencia

[MIT](https://choosealicense.com/licenses/mit/)

## 🙋‍♂️ Autor

Tu Nombre - [@tu-usuario](https://github.com/andreiveisuade)

## ⭐ Agradecimientos

- Inspirado en el Tetris original de Alexey Pajitnov
- Desarrollado usando Pygame
