"""
Customer Churn & Revenue Intelligence - Production Data Cleaning Pipeline
Author: Senior Data Analyst & Analytics Engineer
File: Python/data_cleaning.py
"""

import pandas as pd
import numpy as np
import os

class CustomerDataCleaner:
    def __init__(self, raw_filepath: str, output_filepath: str):
        self.raw_filepath = raw_filepath
        self.output_filepath = output_filepath
        self.df = None
        self.audit_log = {}

    def load_data(self):
        """Loads the raw customer dataset."""
        print(f"[ETL] Loading raw dataset from: {self.raw_filepath}")
        self.df = pd.read_csv(self.raw_filepath)
        self.audit_log['raw_row_count'] = len(self.df)
        self.audit_log['raw_columns'] = list(self.df.columns)
        print(f"[ETL] Successfully loaded {len(self.df):,} rows across {len(self.df.columns)} columns.")
        return self

    def audit_quality(self):
        """Audits missing values, duplicates, and column data types."""
        print("[ETL] Performing preliminary data quality audit...")
        duplicates = self.df.duplicated(subset=['CustomerID']).sum()
        self.audit_log['duplicates_found'] = int(duplicates)
        
        # Check blank strings and NaNs
        blank_total_charges = self.df['Total_Charges'].astype(str).str.strip().isin(['', 'nan', 'None']).sum()
        self.audit_log['blank_total_charges'] = int(blank_total_charges)
        
        missing_internet = self.df['Internet_Service'].isna().sum()
        self.audit_log['missing_internet_service'] = int(missing_internet)
        
        print(f" -> Duplicate Customer IDs: {duplicates}")
        print(f" -> Blank / Missing Total_Charges: {blank_total_charges}")
        print(f" -> Missing Internet_Service records: {missing_internet}")
        return self

    def clean_and_transform(self):
        """Performs robust data type casting, imputation, and string normalization."""
        print("[ETL] Executing cleaning transformations and type casting...")
        
        # 1. Deduplication
        if self.audit_log['duplicates_found'] > 0:
            self.df = self.df.drop_duplicates(subset=['CustomerID'])
            print(f" -> Dropped {self.audit_log['duplicates_found']} duplicate rows.")

        # 2. String trimming
        string_cols = self.df.select_dtypes(include=['object']).columns
        for col in string_cols:
            self.df[col] = self.df[col].astype(str).str.strip()

        # 3. Handle Total_Charges imputation
        # Replace empty strings or whitespace with NaN, then impute 0.00 for new customers
        self.df['Total_Charges'] = pd.to_numeric(self.df['Total_Charges'].replace('', np.nan), errors='coerce')
        new_cust_mask = self.df['Total_Charges'].isna()
        self.df.loc[new_cust_mask, 'Total_Charges'] = 0.00
        print(f" -> Imputed {new_cust_mask.sum()} blank Total_Charges with $0.00.")

        # 4. Handle Internet_Service nulls
        self.df['Internet_Service'] = self.df['Internet_Service'].replace(['nan', 'None', ''], 'None')

        # 5. Type Conversions
        self.df['Age'] = self.df['Age'].astype(int)
        self.df['Tenure_Months'] = self.df['Tenure_Months'].astype(int)
        self.df['Monthly_Charges'] = self.df['Monthly_Charges'].astype(float).round(2)
        self.df['Total_Charges'] = self.df['Total_Charges'].astype(float).round(2)
        self.df['Support_Tickets'] = self.df['Support_Tickets'].astype(int)
        self.df['Usage_Hours'] = self.df['Usage_Hours'].astype(float).round(1)
        self.df['Last_Login_Date'] = pd.to_datetime(self.df['Last_Login_Date'])
        self.df['Signup_Date'] = pd.to_datetime(self.df['Signup_Date'])

        # 6. Feature Engineering for Downstream Analytics
        # Age Groups
        self.df['Age_Group'] = pd.cut(
            self.df['Age'],
            bins=[17, 25, 40, 55, 65, 100],
            labels=['<25 Young Adult', '25-39 Early Career', '40-54 Mid Career', '55-64 Mature', '65+ Senior']
        )

        # Tenure Cohorts
        self.df['Tenure_Cohort'] = pd.cut(
            self.df['Tenure_Months'],
            bins=[-1, 6, 12, 24, 48, 100],
            labels=['0-6 Mos (Onboarding)', '7-12 Mos (First Year)', '13-24 Mos (Growth)', '25-48 Mos (Mature)', '49+ Mos (Loyalist)']
        )

        # Behavioral Churn Risk Score (Rule-based benchmark 0 to 100)
        risk_score = np.zeros(len(self.df))
        risk_score += np.where(self.df['Contract_Type'] == 'Month-to-Month', 35, 0)
        risk_score += np.where(self.df['Payment_Method'] == 'Electronic Check', 15, 0)
        risk_score += np.where(self.df['Support_Tickets'] >= 4, 30, np.where(self.df['Support_Tickets'] >= 2, 15, 0))
        risk_score += np.where(self.df['Tenure_Months'] <= 6, 15, np.where(self.df['Tenure_Months'] <= 12, 8, 0))
        risk_score += np.where(self.df['Usage_Hours'] < 20, 15, np.where(self.df['Usage_Hours'] < 50, 8, 0))
        self.df['Risk_Score'] = np.clip(risk_score, 0, 100).astype(int)

        self.df['Risk_Tier'] = pd.cut(
            self.df['Risk_Score'],
            bins=[-1, 29, 49, 69, 100],
            labels=['Low Risk', 'Medium Risk', 'High Risk', 'Critical Risk']
        )

        # Engagement Metric: Usage per Dollar
        self.df['Usage_Per_Dollar'] = (self.df['Usage_Hours'] / self.df['Monthly_Charges']).round(2)

        print("[ETL] Feature engineering completed successfully.")
        return self

    def save_clean_data(self):
        """Saves the verified clean dataset to disk."""
        os.makedirs(os.path.dirname(self.output_filepath), exist_ok=True)
        self.df.to_csv(self.output_filepath, index=False)
        print(f"[ETL] Clean dataset exported to: {self.output_filepath}")
        print(f"[ETL] Final clean record count: {len(self.df):,} rows.")
        return self.df

if __name__ == '__main__':
    cleaner = CustomerDataCleaner(
        raw_filepath='dataset/customer_churn.csv',
        output_filepath='dataset/customer_churn_cleaned.csv'
    )
    cleaner.load_data().audit_quality().clean_and_transform().save_clean_data()
