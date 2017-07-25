# aot
Файл содержит все исходные данные. На каждой строчке одно слово.

Поля 
- word_id	- идентификатор слова в предложении 
- word - само слово 	
- parent_id	- идентификатор родителя
- tag	- часть речи
- dependency	
- sentence_id - идентификатор пре	
- lemmatized - лемматизированное слово


Загрузка
fr = pd.read_csv('syntaxnet_output.csv',sep="\t",encoding="utf-8")
