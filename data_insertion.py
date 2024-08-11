from models import engine , db_session , Base , Banks , Branches 
import glob
import os
import pandas as pd
from sqlalchemy import text

Base.metadata.create_all(bind = engine)

bank_list = [None]*200 


def create_banks():
    bank_data = pd.read_csv('banks.csv')

    for ind in bank_data.index:
        name = bank_data['name'][ind]
        id = bank_data['id'][ind]

        # Check if the bank already exists
        existing_bank = db_session.query(Banks).filter_by(id=id).first()
        if existing_bank:
            # Update the existing bank record if necessary
            existing_bank.name = name
            db_session.add(existing_bank)
        else:
            # Insert new bank record
            bank_row = Banks(name=name, id=int(id))
            db_session.add(bank_row)
            bank_list[int(id)] = bank_row


def create_branches():

	branches_data = pd.read_csv('bank_branches.csv')

	for ind in branches_data.index:
		ifsc = branches_data['ifsc'][ind] 
		bank_id = branches_data['bank_id'][ind] 
		branch = branches_data['branch'][ind] 
		address = branches_data['address'][ind] 
		city=branches_data['city'][ind] 
		district=branches_data['district'][ind] 
		state=branches_data['state'][ind]
		bank= bank_list[int(bank_id)]
		
		# print(f"{ifsc} , {bank_id} , {branch} , {address} , {branch} , {address} , {city} , {district} , {state} ")
		branch_row = Branches(ifsc = ifsc ,bank_id = int(bank_id) , branch = branch , address = address , city=city , district=district , state=state , bank=bank )
		db_session.add(branch_row)


create_banks()
create_branches()

db_session.commit()

print("inserted data in db session")
