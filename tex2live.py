from flask import Flask, request, send_file
import subprocess
import time
import re
import os

app = Flask('tex2image')


def sanitize(input):
    return re.sub(r'\\write18\{.*\}', 'sanitized for the security', input)


@app.route('/', methods=['GET'])
def index():
    if 'expr' in request.args:
        expr = request.args.get('expr')
        expr = sanitize(expr)

        document = '\n'.join((
            '\documentclass{minimal}',
            '\\begin{document}',
            expr,
            '\\end{document}'
        ))

        filename = "tex2image_" + time.strftime('%Y%m%d_%H%M%S')
        with open(f'{filename}.tex', 'w') as f:
            f.write(document)

        subprocess.call(['latex', '-src', '-interaction=nonstopmode',
                         f'{filename}.tex'])
        subprocess.call(['dvipng', '-T', 'tight', '-D', '120',
                         '-o', f'{filename}.png', f'{filename}.dvi'])

        if os.path.isfile(f'{filename}.png'):
            return send_file(f'{filename}.png',
                             'image/png')
        else:
            return send_file(f'invalid_expression.png',
                             'image/png')

    return 'LaTex to image'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
