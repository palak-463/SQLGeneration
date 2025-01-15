from sqlalchemy import create_engine
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())

with engine.connect() as conn:
    result = conn.execute(text("SELECT dealer_name, monthstartdate FROM throughput"))
    for row in result:
        print(f"x: {row.dealer_name}  y: {row.monthstartdate}")