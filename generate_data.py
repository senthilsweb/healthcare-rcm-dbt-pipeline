import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random
from typing import List, Dict
import os

# Initialize Faker
fake = Faker()
Faker.seed(42)
np.random.seed(42)

class HealthcareDataGenerator:
    def __init__(self):
        self.users = []
        self.facilities = []
        self.health_plans = []
        self.claims = []
        self.encounters = []
        self.claim_activities = []
        self.collections = []
        
    def generate_users(self):
        users_data = []
        
        # Generate doctors
        specialties = ['Cardiology', 'Pediatrics', 'Orthopedics', 'Neurology', 
                      'Internal Medicine', 'Family Medicine']

        for i in range(20):
            users_data.append({
                'id': i + 1,
                'userID': f'DR{fake.unique.random_number(digits=6)}',
                'userType': 'DOCTOR',
                'name': fake.name(),
                'dateOfBirth': fake.date_of_birth(minimum_age=30, maximum_age=70),
                'contactInfo': fake.phone_number(),
                'specialty': random.choice(specialties),
                'department': None,
                'role': None
            })
        
        departments = ['Administration', 'Billing', 'Nursing', 'Laboratory', 'Radiology']
        roles = ['Administrator', 'Nurse', 'Lab Technician', 'Office Manager', 'Medical Assistant']
        for i in range(15):
            users_data.append({
                'id': len(users_data) + 1,
                'userID': f'STF{fake.unique.random_number(digits=6)}',
                'userType': 'STAFF',
                'name': fake.name(),
                'dateOfBirth': fake.date_of_birth(minimum_age=22, maximum_age=65),
                'contactInfo': fake.phone_number(),
                'specialty': None,
                'department': random.choice(departments),
                'role': random.choice(roles)
            })

        # Generate payers (insurance companies)
        insurance_companies = [
            'Blue Cross Blue Shield',
            'UnitedHealth Group',
            'Aetna',
            'Cigna',
            'Humana'
        ]
        
        for i, company in enumerate(insurance_companies):
            users_data.append({
                'id': len(users_data) + 1,
                'userID': f'PAY{fake.unique.random_number(digits=6)}',
                'userType': 'PAYER',
                'name': company,
                'dateOfBirth': None,
                'contactInfo': fake.phone_number(),
                'specialty': None,
                'department': None,
                'role': None
            })
        
        # Generate patients
        for i in range(100):
            users_data.append({
                'id': len(users_data) + 1,
                'userID': f'PT{fake.unique.random_number(digits=6)}',
                'userType': 'PATIENT',
                'name': fake.name(),
                'dateOfBirth': fake.date_of_birth(),
                'contactInfo': fake.phone_number(),
                'specialty': None,
                'department': None,
                'role': None
            })
        
        self.users = pd.DataFrame(users_data)
        return self.users
    
    def generate_facilities(self):
        facilities_data = []
        for i in range(10):
            facilities_data.append({
                'id': i + 1,
                'facilityID': f'FAC{fake.unique.random_number(digits=6)}',
                'name': f"{fake.company()} {random.choice(['Hospital', 'Medical Center', 'Clinic', 'Healthcare Center'])}",
                'location': f"{fake.street_address()}, {fake.city()}",
                'contactInfo': fake.phone_number()
            })
        self.facilities = pd.DataFrame(facilities_data)
        return self.facilities
    
    def generate_health_plans(self):
        health_plans_data = []
        payer_ids = self.users[self.users['userType'] == 'PAYER']['id'].tolist()
        
        for payer_id in payer_ids:
            num_plans = random.randint(3, 5)
            for _ in range(num_plans):
                tier = random.choice(['Bronze', 'Silver', 'Gold', 'Platinum', 'Essential'])
                plan_type = random.choice(['PPO', 'HMO', 'EPO', 'POS'])
                health_plans_data.append({
                    'id': len(health_plans_data) + 1,
                    'healthPlanID': f'HP{fake.unique.random_number(digits=6)}',
                    'planName': f'{tier} {plan_type}',
                    'payerID': payer_id
                })
        
        self.health_plans = pd.DataFrame(health_plans_data)
        return self.health_plans
    
    def generate_encounters(self):
        encounters_data = []
        patient_ids = self.users[self.users['userType'] == 'PATIENT']['id'].tolist()
        doctor_ids = self.users[self.users['userType'] == 'DOCTOR']['id'].tolist()
        facility_ids = self.facilities['id'].tolist()
        
        for i in range(200):
            encounters_data.append({
                'id': i + 1,
                'encounterID': f'ENC{fake.unique.random_number(digits=8)}',
                'patientID': random.choice(patient_ids),
                'doctorID': random.choice(doctor_ids),
                'facilityID': random.choice(facility_ids),
                'date': fake.date_between(start_date='-2y', end_date='+1y'),
                'type': random.choice(['Initial Visit', 'Follow-up', 'Emergency', 
                                     'Routine Checkup', 'Specialist Consultation']),
                'duration': random.randint(15, 120),
                'notes': fake.text(max_nb_chars=200)
            })
        
        self.encounters = pd.DataFrame(encounters_data)
        return self.encounters
    
    def generate_claims(self):
        claims_data = []
        patient_ids = self.users[self.users['userType'] == 'PATIENT']['id'].tolist()
        payer_ids = self.users[self.users['userType'] == 'PAYER']['id'].tolist()
        
        for i in range(300):
            created_date = fake.date_between(start_date='-2y', end_date='today')
            updated_date = fake.date_between(start_date=created_date, end_date='today')
            
            claims_data.append({
                'id': i + 1,
                'claimID': f'CLM{fake.unique.random_number(digits=8)}',
                'patientID': random.choice(patient_ids),
                'payerID': random.choice(payer_ids),
                'status': random.choice(['Submitted', 'In Review', 'Approved', 'Denied', 'Appealed']),
                'dateCreated': created_date,
                'dateUpdated': updated_date,
                'amount': round(random.uniform(100, 10000), 2)
            })
        
        self.claims = pd.DataFrame(claims_data)
        return self.claims
    
    def generate_claim_activities(self):
        claim_activities_data = []
        activity_counter = 1
        
        for _, claim in self.claims.iterrows():
            num_activities = random.randint(2, 5)
            for _ in range(num_activities):
                claim_activities_data.append({
                    'id': activity_counter,
                    'activityID': f'ACT{fake.unique.random_number(digits=8)}',
                    'claimID': claim['id'],
                    'activityDate': fake.date_between(start_date=claim['dateCreated'], 
                                                    end_date=claim['dateUpdated']),
                    'activityType': random.choice(['Submission', 'Review', 'Documentation Request',
                                                 'Appeal', 'Payment Processing']),
                    'diagnosisCode': f'ICD-{fake.unique.random_number(digits=5)}',
                    'procedureCode': f'CPT-{fake.unique.random_number(digits=5)}',
                    'notes': fake.text(max_nb_chars=100)
                })
                activity_counter += 1
        
        self.claim_activities = pd.DataFrame(claim_activities_data)
        return self.claim_activities
    
    def generate_collections(self):
        collections_data = []
        approved_claims = self.claims[self.claims['status'] == 'Approved']
        
        for idx, claim in approved_claims.iterrows():
            collections_data.append({
                'id': len(collections_data) + 1,
                'collectionID': f'COL{fake.unique.random_number(digits=8)}',
                'claimID': claim['id'],
                'date': fake.date_between(start_date=claim['dateUpdated'], end_date='today'),
                'methodOfCollection': random.choice(['Credit Card', 'Bank Transfer', 'Check', 
                                                  'Cash', 'Electronic Payment']),
                'amountCollected': round(random.uniform(50, claim['amount']), 2),
                'status': random.choice(['Processed', 'Pending', 'Completed', 'Failed'])
            })
        
        self.collections = pd.DataFrame(collections_data)
        return self.collections
    
    def generate_all_data(self):
        print("Generating users...")
        self.generate_users()
        
        print("Generating facilities...")
        self.generate_facilities()
        
        print("Generating health plans...")
        self.generate_health_plans()
        
        print("Generating encounters...")
        self.generate_encounters()
        
        print("Generating claims...")
        self.generate_claims()
        
        print("Generating claim activities...")
        self.generate_claim_activities()
        
        print("Generating collections...")
        self.generate_collections()
        

        output_path = '/Users/skaruppaiah1/data-pipelines/healthcare_dbt_project/healthcare_analytics/seeds/healthcare_data'

        # Create directory if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Define a dictionary mapping dataframe attributes to filenames
        df_mapping = {
            'users': 'stg_users.csv',
            'facilities': 'stg_facilities.csv',
            'health_plans': 'stg_health_plans.csv',
            'encounters': 'stg_encounters.csv',
            'claims': 'stg_claims.csv',
            'claim_activities': 'stg_claim_activities.csv',
            'collections': 'stg_collections.csv'
        }

        # Save all dataframes to CSV
        for df_name, filename in df_mapping.items():
            df = getattr(self, df_name)
            output_file = os.path.join(output_path, filename)
            df.to_csv(output_file, index=False)
            print(f"Saved {filename}")
        
        print("All data generated and saved to CSV files in 'healthcare_data' directory!")
        
        # Return dictionary of all dataframes
        return {
            'users': self.users,
            'facilities': self.facilities,
            'health_plans': self.health_plans,
            'encounters': self.encounters,
            'claims': self.claims,
            'claim_activities': self.claim_activities,
            'collections': self.collections
        }

# Usage
if __name__ == "__main__":
    generator = HealthcareDataGenerator()
    data = generator.generate_all_data()
    print("Users Sample:")
    print(data['users'].head())

    print("\nClaims Sample:")
    print(data['claims'].head())