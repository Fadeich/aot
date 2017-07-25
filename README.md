# aot
### Load dictionary

import pickle
from collections import namedtuple
features = namedtuple('features', ['word', 'part_of_speech', 'tonality', 'source', 'extra'])
with open('dict.pickle', 'rb') as f:
    Dict = pickle.load(f)
    
### Example

Dict['аборт'][0].word

features:
'word', 'part_of_speech', 'tonality', 'source', 'extra'

from dictionary:
! 1. слово или словосочетание,
! 2. Часть речи или синтаксический тип группы,
! 3. слово или словосочетание в лемматизированной форме, 
! 4. Тональность: позитивная (positive), негативная(negative), нейтральная (neutral) или неопределеная оценка, зависит от контекста (positive/negative),
! 5. Источник: оценка (opinion), чувство (feeling), факт (fact),
! 6. Если тональность отличается для разных значений многозначного слова, то перечисляются все значения слова по тезаурусу РуТез и дается отсылка на сооветствующее понятие - имя понятия в кавычках.
!
!RuSentiLex Structure
!1. word or phrase,
!2. part of speech or type of syntactic group,
!3. initial word (phrase) in a lemmatized form,
!4. Sentiment: positive, negative, neutral or positive/negative (indefinite, depends on the context),
!5. Source: opinion, feeling (private state), or fact (sentiment connotation),
!6. Ambiguity: if sentiment is different for senses of an ambiguous word, then sentiment orientations for all senses are described, the senses
