import pandas as pd
import pymysql
conn = pymysql.connect(host="121.37.68.231", user="ZhenShanMei", password="Lxp6869882699", db="Cook", port=3306)
cur = conn.cursor()
def insertTable(sql):
    try:
        cur.execute(sql)
        conn.commit()
    except Exception as e :
        print("There is a error in sql which is: " + sql)
df = pd.read_csv("full_dataset_sample.csv")
df = df.drop(['unknow'],axis= 1)
id = 1
for index, item in df.iterrows():
    sqlInsertDish = 'insert into Dishes values({id},{search},"{title}","{ingredients}","{directions}","{link}","{source}");'
    # format the ingredients by deleting [ and ] and "
    ingredients = item["ingredients"]
    ingredients = ingredients.replace("[","")
    ingredients = ingredients.replace("]", "")
    ingredients = ingredients.replace('"', "")
    item["ingredients"] = ingredients
    # format the directions by deleting [ and ]
    directions = item["directions"]
    directions = directions.replace("[", "")
    directions = directions.replace("]", "")
    directions = directions.replace('"', "")
    item["directions"] = directions
    sqlInsertDish = sqlInsertDish.format(id = id,search=item["search"],title=item["title"].replace('"',""),ingredients=item["ingredients"],directions=item["directions"],link=item["link"],source=item["source"])
    #insertTable(sqlInsertDish)
    print(sqlInsertDish)
    # Get the Keywords list by string (including the "")
    KeyWords = item["NER"][1 : len(item["NER"]) - 1].split(",")
    # delete the "" and insert into the keyword table -- >hope you know what i mean sandro hey hey
    for i in range(len(KeyWords)):
        sqlInsertKeyWord = 'insert into KeyWordDish(keyWord,dishId) values("{keyWord}",{dishId});'
        temp = KeyWords[i].strip()
        temp = temp[1 : len(temp) - 1]
        KeyWords[i] = temp
        sqlInsertKeyWord = sqlInsertKeyWord.format(keyWord=temp,dishId=id)
        print(sqlInsertKeyWord)
        #insertTable(sqlInsertKeyWord)
    id += 1

conn.close()
