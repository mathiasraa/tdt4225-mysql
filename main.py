import dataset

db = dataset.connect("mysql://root:password@db/sample")

table = db["Alchemist"]

table.insert(dict(name="Alphonse Elric"))
table.insert_many(
    [
        dict(name="Edward Elric", titled="Fullmetal"),
        dict(name="Roy Mustang", titled="Flame"),
    ]
)
