from sqlalchemy import column, table

transactions_table = table("transactions",
                           column("t_id"),
                           column("amount"),
                           column("date"),
                           column("notes"),
                           column("category"),
                           column("card"),
                           column("type")
                           )

tags_table = table("tags",
                   column("tag_id"),
                   column("transaction_id"),
                   column("tag"),
                   )