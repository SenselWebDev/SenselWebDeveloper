X_DIMENSION = 16
Y_DIMENSION = 16
ABSOLUTE_FILE_PATH = '/Users/bgm9103/Desktop/test.html'

def create_html(grid_size, css_properties, body):
	w = "<!doctype html><header><link href='http://fonts.googleapis.com/css?family=Lato:300' rel='stylesheet' type='text/css'><style>body {font-family: 'Lato', sans-serif;font-size: 30px;} .wrapper {display: grid; grid-template-columns: "

	x = ""
	for i in range(0, X_DIMENSION):
		x += (grid_size + 'px ')
	x += ';' 

	w += x
	w += 'grid-template-rows: '

	y = ""
	for i in range(0, Y_DIMENSION):
		y += (grid_size + 'px ')
	y += ';}' 

	w += y
	w += '</style></header>'

	return w + css_properties + body

def get_css_properties(elements):
	property = ''

	for element in elements:
		property += '.' + element.name + '{ '
		property += 'grid-column: ' + str(element.position[0][0]) + '/' + str(element.position[1][0]) + ';'
		property += 'grid-row: ' + str(element.position[0][1]) + '/' + str(element.position[1][1]) + ';'
		if element.state == 'txt' or element.state == 'shape':
			property += 'background: ' + element.color + ';'
			property += 'text-align: center;'
		property += '} '

	return property

def get_body(elements):
	body = '<body>'

	for element in elements:
		if element.state == 'img':
			body += generate_element(element.name, '', 'img', 'src=' + element.content)
		elif element.state == 'txt':
			body += generate_div(element.name, generate_element('', element.content, 'h1', ''))
		elif element.state == 'shape':
			body += generate_div(element.name, '')

	body += '</body>'

	return body

def generate_element(name, content, type, property):
	return '<' + type + ' class="box ' + name + '" ' + property + '>' + content + '</' + type + '>'

def generate_div(name, content):
	return generate_element(name, content, 'div', '')

def create_html_file(html_content):
	with open(ABSOLUTE_FILE_PATH, 'w') as f:
		f.write(html_content)

def main():
	elements = ''

	css = get_css_properties(elements)
	body = get_body(elements)
	grid_size = 94				# 94px per grid cell

	html_content = create_html(grid_size, css, body)

	create_html_file(html_content)



if __name__ == '__main__':
	main()