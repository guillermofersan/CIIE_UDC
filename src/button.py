class Button():

	"""
	
	Clase encargada de manejar los botones de los diferentes menus.
	
	"""

	def __init__(self, image, pos, text_input, font, base_color, hovering_color):

		"""
		
		Inicializa todos los parametros necesarios para la creacion del boton: fondo, posicion(x e y), texto, fuente, color y color de hover
		
		"""

		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):

		"""
		
		Muestra el boton por pantalla haciendo un blit
		
		"""

		if self.image is not None:
			screen.blit(self.image, self.rect)
		
		# En caso de que no haya fondo
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):

		"""
		
		Comprueba que el click se realice en el boton comparando sus posiciones
		
		"""

		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):

		"""
		
		Cuando se pasa el raton por encima del boton, se le cambia el color a las letras al color de hover.
		
		"""
		
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)