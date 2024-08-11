from models import Banks , Branches , db_session

banks = db_session.query(Banks).all()
branches = db_session.query(Branches).all()


for bank in banks:
    print(f"{bank.name} , {bank.id}" )

# for branch in branches:
# 	print(branch.address)

