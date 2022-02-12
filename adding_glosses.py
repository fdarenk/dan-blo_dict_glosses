import re


def main():
    def read_file(name):
        fh = open(name, 'r', encoding='utf8')
        dict = fh.read()
        fh.close()
        return dict
    def write_file(name, content):
        fh = open(name, 'w', encoding='utf8')
        fh.write(content)
        fh.close()
    dict_text = read_file('blodaba_07feb2022.txt')
    new_dict = get_new_dict(dict_text)
    write_file('blodaba_autoglosses', new_dict)


def get_new_dict(dict_text):
    lexemes = dict_text.split('\n\n')
    new_dict = ''

    for lexeme in lexemes:
        # если уже есть глоссы, оставляем без изменений (+ первые две тех. лексемы)
        existing_glosses = re.search('\n\\\gr .*\n\\\gf .*\n\\\ge .*(\n|$)', lexeme)
        if existing_glosses or lexeme == '\_sh v3.0  1285 Mande general' or lexeme == '\le\n\dt 14/Jan/2017':
            pass
        else:
            glosses = process_lexeme(lexeme)
            lexeme = add_glosses(lexeme, glosses)

        new_dict = '\n\n'.join([new_dict, lexeme])

    return new_dict


def process_lexeme(lexeme):

    def count_glosses(array):
        count = 0
        for el in array:
            count += 1 if el else 0
        return count

    # если несколько значений (то есть и несколько толкований), выбираем откуда будем брать глоссы
    if re.search('\\\ms ', lexeme):
        all_ms = lexeme.split('\n\ms ')
        max_glosses_amount = 0
        glosses = []
        for ms in all_ms:
            cur_glosses = get_glosses(ms)
            cur_amount = count_glosses(cur_glosses)
            if cur_amount > max_glosses_amount:
                glosses = cur_glosses
                max_glosses_amount = cur_amount
        return glosses
    # если значение одно:
    else:
        return get_glosses(lexeme)


def get_glosses(lexeme):
    rows = lexeme.split('\n')
    glosses = {'r': '',
               'f': '',
               'e': ''}
    for row in rows:
        if len(row) < 7:
            continue
        lang = row[3]
        # строка с толкованием
        if row.startswith('\df') and lang in ('r', 'f', 'e') and row[4] == ' ':
            # если еще нет глоссы на этом языке
            if glosses[lang] == '':
                glosses[lang] = extract_gloss(row, lang)
            else:
                pass

    if (glosses['r'], glosses['f'], glosses['e']) == ('', '', ''):
        return []
    return ['\gr ' + glosses['r'], '\gf ' + glosses['f'], '\ge ' + glosses['e']]


def extract_gloss(definition, lang):
    definition = definition.replace('\df' + lang + ' ', '')
    definition = re.sub('^, ', '', definition)
    if lang == 'r':
        definition = re.sub('[́\\\]', '', definition)
        definition = re.sub('( (на|в))? (ко|ке|ч[её])(го|му|м)-л', '', definition)
        definition = re.sub(' \(что-л\)', '', definition)
        definition = re.sub(' что-л', '', definition)
        definition = re.sub('(\(ая\)|/ая)', '', definition)
        definition = re.sub('-', '.', definition)
        if len(definition.split(' ')) < 4:
            definition = re.sub(' ', '.', definition)
        if len(definition.split(' ')) == 1 and re.search('^[а-яА-ЯёЁ.]+$', definition):
            return definition
        else:
            pass
            #print(definition)
    if lang == 'f':
        definition = re.sub(' q(n|ch)', '', definition)
        definition = re.sub(' \([mfn](,? ?pl|, f)?\)', '', definition)
        definition = re.sub(', -(i?èr)?e', '', definition)
        definition = re.sub('\(s\)[ $]', '', definition)
        definition = re.sub('-', '.', definition)
        if len(definition.split(' ')) < 4:
            definition = re.sub(' ', '.', definition)
        if len(definition.split(' ')) == 1 and re.search('^[\wçèéàùâêûîô\'.]+$', definition) and not re.search('\.\.', definition):
            return definition
        else:
            pass
            #print(definition)
    if lang == 'e':
        definition = re.sub('-', '.', definition)
        if len(definition.split(' ')) < 4:
            definition = re.sub(' ', '.', definition)
        if len(definition.split(' ')) == 1 and re.search('^[\w\'.]+$', definition) and not re.search('\.\.', definition):
            return definition
        else:
            pass
            #print(definition)
    return ''


def add_glosses(lexeme, glosses):

    all_and_date = lexeme.split('\n\dt ')
    all = all_and_date[0]
    date = all_and_date[1] if len(all_and_date) > 1 else None

    if len(glosses) == 3:
        pass
    else:
        assert glosses == []
        glosses = ['\gr ', '\gf ', '\ge ']
    glosses_text = '\n'.join(glosses)

    all_and_glosses = '\n'.join([all, glosses_text])
    if date:
        result = '\n\dt '.join([all_and_glosses, date])
    else:
        result = all_and_glosses
    return result


if __name__ == '__main__':
    main()