with open('s3_timestamp.txt', 'r') as file:
    text = file.read()

html_text = '<html>\n<body>\n'

for line in text.split('\n'):
    html_text += f'<p>{line}</p>\n'

html_text += '</body>\n</html>'

with open('s3_timestamp.html', 'w') as file:
    file.write(html_text)

