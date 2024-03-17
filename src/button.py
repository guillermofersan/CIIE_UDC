class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        """
        Inicializa todos los parámetros necesarios para la creación del botón:
        fondo, posición(x e y), texto, fuente, color y color de hover
        """
        self.pos = pos
        self.font = font
        self.image = image or self.font.render(text_input, True, base_color)
        self.colors = {'base': base_color, 'hover': hovering_color}
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.colors['base'])
        self.rect = self.image.get_rect(center=self.pos)
        self.text_rect = self.text.get_rect(center=self.pos)

    def update(self, screen):
        """
        Muestra el botón por pantalla haciendo un blit
        """
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def is_hovered(self, position):
        """
        Comprueba si el ratón está sobre el botón
        """
        return self.rect.left <= position[0] <= self.rect.right and self.rect.top <= position[1] <= self.rect.bottom

    def checkForInput(self, position):
        """
        Comprueba que el click se realice en el botón comparando sus posiciones
        """
        return self.is_hovered(position)

    def changeColor(self, position):
        """
        Cuando se pasa el ratón por encima del botón, se le cambia el color a las letras al color de hover.
        """
        color_key = 'hover' if self.is_hovered(position) else 'base'
        self.text = self.font.render(self.text_input, True, self.colors[color_key])