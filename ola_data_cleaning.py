# ============================================================
#   OLA Ride Insights — Step 1: Data Cleaning & Preprocessing
#   Author: [Your Name]
#   Description: Load raw OLA dataset, clean it, and save
#                a clean version for SQL and Power BI use.
# ============================================================

import pandas as pd
import numpy as np

# ── STEP 1: Load the dataset ─────────────────────────────────
# Make sure OLA_DataSet.xlsx is in the same folder as this script.

df = pd.read_excel('C:/Users/Admin/OneDrive/Desktop/DS_Sec_Project/Data/OLA_DataSet.xlsx')

print("✅ Dataset Loaded Successfully")
print(f"   Total Rows    : {df.shape[0]}")
print(f"   Total Columns : {df.shape[1]}")


# ── STEP 2: Drop useless column ──────────────────────────────
# 'Vehicle Images' only has image URLs — not useful for analysis.

df = df.drop(columns=['Vehicle Images'])
print("\n✅ Dropped 'Vehicle Images' column")


# ── STEP 3: Fix the Date column ──────────────────────────────
# Convert to datetime, then extract Day, Month, Year, Day_Name.
# These extra columns help with trend charts in Power BI.

df['Date']     = pd.to_datetime(df['Date'])
df['Day']      = df['Date'].dt.day
df['Month']    = df['Date'].dt.month
df['Year']     = df['Date'].dt.year
df['Day_Name'] = df['Date'].dt.day_name()

print("\n✅ Date column fixed. Added: Day, Month, Year, Day_Name")


# ── STEP 4: Fix the Time column ──────────────────────────────
# Extract the HOUR (0-23) to analyse peak booking hours.

df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.hour
print("\n✅ Extracted 'Hour' from Time column")


# ── STEP 5: Handle Missing Values ────────────────────────────
# Missing values here are LOGICAL — cancelled rides have
# no payment, no ratings, no turnaround times.
# We fill them with 0 or 'Not Applicable' — NOT delete rows.

df['Driver_Ratings']              = df['Driver_Ratings'].fillna(0)
df['Customer_Rating']             = df['Customer_Rating'].fillna(0)
df['V_TAT']                       = df['V_TAT'].fillna(0)
df['C_TAT']                       = df['C_TAT'].fillna(0)
df['Payment_Method']              = df['Payment_Method'].fillna('Not Applicable')
df['Canceled_Rides_by_Customer']  = df['Canceled_Rides_by_Customer'].fillna('Not Applicable')
df['Canceled_Rides_by_Driver']    = df['Canceled_Rides_by_Driver'].fillna('Not Applicable')
df['Incomplete_Rides']            = df['Incomplete_Rides'].fillna('No')
df['Incomplete_Rides_Reason']     = df['Incomplete_Rides_Reason'].fillna('Not Applicable')

print("\n✅ Missing values handled (filled with 0 or 'Not Applicable')")
print("   Remaining nulls:", df.isnull().sum().sum())


# ── STEP 6: Remove duplicate Booking IDs ─────────────────────
duplicates = df.duplicated(subset='Booking_ID').sum()
print(f"\n✅ Duplicate Booking IDs found: {duplicates}")
if duplicates > 0:
    df = df.drop_duplicates(subset='Booking_ID')
    print(f"   Removed. New row count: {df.shape[0]}")


# ── STEP 7: Final summary ────────────────────────────────────
print(f"\n✅ Final cleaned dataset shape: {df.shape}")
print("\nBooking Status breakdown:")
print(df['Booking_Status'].value_counts())

print("\nVehicle Type breakdown:")
print(df['Vehicle_Type'].value_counts())

print("\nPayment Method breakdown:")
print(df['Payment_Method'].value_counts())


# ── STEP 8: Save cleaned file ────────────────────────────────
# CSV format is easiest to import into MySQL and Power BI.

df.to_csv('Data/OLA_Cleaned.csv', index=False)
print("\n✅ Saved as 'OLA_Cleaned.csv' — ready for MySQL and Power BI!")
