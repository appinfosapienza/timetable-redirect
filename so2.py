'''
Script per generare la pagina HTML so2.html
'''

print('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SO2</title>

    <style>
        .show-answer .correct + label {
            color: #09af00;
        }

        .show-answer .wrong + label {
            color: red;
        }

        fieldset {
            margin-top: 32px;
        }
    </style>
</head>
<body>
    <p><a href="#" id="show-past-errors" style="display: none" onclick="showPastErrors()">Mostra le sbagliate l'ultima volta</a></p>
    <div id="questions-form">
    ''')

def is_ans(line):
    return line and line[0:2] in ('v ', '> ')

question_index, answer_index, old_line, in_code = 0, 0, '', False
for line in open(sys.argv[1], 'r').readlines():
    line = line.strip().replace('&', '&amp;')
    if not line and old_line:
        print('</fieldset>')
    elif is_ans(line) and not is_ans(old_line):
        print('</legend>')

    if '<code>' in line or '<pre>' in line:
        in_code = True
    if '</code>' in line or '</pre>' in line:
        in_code = False

    if line.startswith('v '):
        print(f'''
        <div>
              <input type="radio" id="{question_index}_{answer_index}" name="{question_index}" class="correct">
              <label for="{question_index}_{answer_index}">{line[2:]}</label>
            </div>
        ''')
        answer_index += 1
    elif line.startswith('> '):
        print(f'''
        <div>
              <input type="radio" id="{question_index}_{answer_index}" name="{question_index}">
              <label for="{question_index}_{answer_index}">{line[2:]}</label>
            </div>
        ''')
        answer_index += 1
    elif not is_ans(line) and not old_line:
        print(f'<fieldset id="{question_index}"><legend>{line}')
        answer_index = 0
        question_index += 1
    else:
        print(line)
        if not in_code: print('<br>')
    
    old_line = line


print('''</fieldset> <input type="submit" value="Rispondi" onclick="checkAnswers()">
    </div>

    <script>
        const questionFields = () => document.querySelectorAll('#questions-form > fieldset');
        const pastErrorsButton = document.getElementById('show-past-errors');

        const pastErrors = localStorage.getItem('past-errors');
        if (pastErrors) {
            pastErrorsButton.style = '';
        }

        function showPastErrors() {
            const pastErrorsIds = pastErrors.split(',');
            questionFields().forEach(fieldset => {
                if (pastErrorsIds.indexOf(fieldset.id) < 0) {
                    fieldset.remove();
                }
            });
            pastErrorsButton.style = 'display: none';
        }

        function checkAnswers() {
            const wrongAnswers = [];

            questionFields().forEach(fieldset => {
                const inputs = [...fieldset.querySelectorAll('input')];
                // Disable input
                inputs.forEach(input => input.disabled = true);

                const givenAnswer = inputs.find(input => input.checked);

                if (givenAnswer && givenAnswer.classList.contains('correct')) {
                    // Correct!
                    // Hide question from result
                    fieldset.remove();
                } else {
                    // Wrong!
                    wrongAnswers.push(fieldset.id);
                    fieldset.classList.add('show-answer');
                    // Highlight given answer
                    if (givenAnswer) {
                        givenAnswer.classList.add('wrong');
                    }
                }
            });

            if (wrongAnswers.length == 0) {
                alert('Tutte giuste, mostro!');
            } else {
                alert('Verranno mostrate le domande sbagliate o in bianco');
                window.scrollTo(0, 0);
            }

            localStorage.setItem('past-errors', wrongAnswers.join(','));
        }
    </script>
</body>
</html>''')
