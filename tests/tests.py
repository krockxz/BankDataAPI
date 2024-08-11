import unittest
import json
from app import app, db_session
from models import Base, Banks, Branches

class BankBranchAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Create all tables
        Base.metadata.create_all(bind=db_session.get_bind())

        # Clear the tables to avoid UNIQUE constraint failures
        db_session.execute("DELETE FROM branches")
        db_session.execute("DELETE FROM banks")
        db_session.commit()

        # Now create test data
        self.create_test_data()

    def create_test_data(self):
        # Create a test bank
        bank = Banks(id=1, name='Test Bank')
        db_session.add(bank)

        # Create a test branch
        branch = Branches(
            ifsc='TEST0001',
            bank_id=1,
            branch='Test Branch',
            address='123 Test St',
            city='Test City',
            district='Test District',
            state='Test State',
            bank=bank
        )
        db_session.add(branch)
        db_session.commit()

    def tearDown(self):
        db_session.remove()
        # Drop all tables after each test
        Base.metadata.drop_all(bind=db_session.get_bind())

    def test_graphql_all_banks(self):
        query = """
        {
            banks {
                edges {
                    node {
                        name
                        id
                    }
                }
            }
        }
        """
        response = self.app.post('/gql', json={'query': query})
        print(response.data.decode('utf-8'))  # Print the response content for debugging
        self.assertEqual(response.status_code, 200)

    def test_graphql_all_banks(self):
        query = """
        {
            allBanks {
                edges {
                    node {
                        name
                        id
                    }
                }
            }
        }
        """
        response = self.app.post('/gql', json={'query': query})
        print(response.data.decode('utf-8'))  # Print the response content for debugging
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        print(data)  # Debugging output to see the structure of the response
        self.assertIn('allBanks', data['data'])  # Adjust this based on the actual response structure


if __name__ == '__main__':
    unittest.main()
