import csv
import mysql.connector
from mysql.connector import Error
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # safe backend for non-interactive/terminal use
import matplotlib.pyplot as plt
import seaborn as sns

# Define connection parameters globally for convenience
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'H@rshit1234',
    'database': 'ola_ride_booking'
}

TABLE_NAME = "ola_ride_booking_50000"


def get_connection():
    """Establishes and returns a database connection."""
    return mysql.connector.connect(**DB_CONFIG)

# =====================================================================
# 1. TABLE STRUCTURE MANAGEMENT (DDL)
# =====================================================================

def manage_table_structure():
    """Demonstrates how to create, alter, and drop a table safely."""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # A. CREATE TABLE (Matches the ola_ride_booking_50000 schema)
        create_query = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            Booking_ID TEXT,
            Ride_Date TEXT,
            Ride_Time TEXT,
            Pickup_City TEXT,
            Pickup_Location TEXT,
            Drop_Location TEXT,
            Customer_ID TEXT,
            Driver_ID TEXT,
            Vehicle_Type TEXT,
            Ride_Distance_KM DOUBLE,
            Ride_Duration_Minutes INT,
            Base_Fare DOUBLE,
            Surge_Multiplier DOUBLE,
            Discount DOUBLE,
            Platform_Fee DOUBLE,
            GST DOUBLE,
            Total_Fare DOUBLE,
            Net_Revenue DOUBLE,
            Profit DOUBLE,
            Payment_Method TEXT,
            Booking_Status TEXT,
            Cancellation_Reason TEXT,
            Customer_Rating DOUBLE,
            Driver_Rating DOUBLE,
            Customer_Name TEXT,
            Driver_Name TEXT,
            Driver_Age INT,
            Customer_Gender TEXT,
            Driver_Experience_Years INT,
            Vehicle_Number TEXT,
            Vehicle_Model TEXT,
            Fuel_Type TEXT,
            Weather TEXT,
            Traffic_Level TEXT,
            Ride_Type TEXT,
            Coupon_Code TEXT,
            Coupon_Discount DOUBLE,
            Peak_Hour TEXT,
            Weekend TEXT,
            Month TEXT,
            Quarter INT,
            Year INT
        )
        """
        cursor.execute(create_query)
        print(f"Table '{TABLE_NAME}' verified/created successfully.")

        # B. ALTER TABLE (Example: Safely adding a temporary column)
        cursor.execute(f"ALTER TABLE {TABLE_NAME} ADD COLUMN temp_notes TEXT")
        print("Table altered: Added 'temp_notes' column.")

        # C. DROP COLUMN (Example: Dropping the temporary column to keep things clean)
        cursor.execute(f"ALTER TABLE {TABLE_NAME} DROP COLUMN temp_notes")
        print("Table altered: Dropped 'temp_notes' column.")

        connection.commit()
    except Error as e:
        print(f"Structure Management Error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# =====================================================================
# 2. DATA MANIPULATION OPERATIONS (CRUD)
# =====================================================================

def insert_booking(booking_id, ride_date, ride_time, pickup_city, pickup_location,
                    drop_location, customer_id, driver_id, vehicle_type,
                    ride_distance_km, ride_duration_minutes, base_fare, total_fare,
                    payment_method, booking_status):
    """Inserts a new ride booking record using parameterized queries to prevent SQL injection."""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = f"""
        INSERT INTO {TABLE_NAME}
        (Booking_ID, Ride_Date, Ride_Time, Pickup_City, Pickup_Location, Drop_Location,
         Customer_ID, Driver_ID, Vehicle_Type, Ride_Distance_KM, Ride_Duration_Minutes,
         Base_Fare, Total_Fare, Payment_Method, Booking_Status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (booking_id, ride_date, ride_time, pickup_city, pickup_location,
                drop_location, customer_id, driver_id, vehicle_type,
                ride_distance_km, ride_duration_minutes, base_fare, total_fare,
                payment_method, booking_status)

        cursor.execute(query, data)
        connection.commit()
        print(f"\n[SUCCESS] Booking added! Inserted Booking ID: {booking_id}")
    except Error as e:
        print(f"\n[ERROR] Insert Failed: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def update_booking_status(booking_id, new_status):
    """Updates the booking status for a specific Booking ID."""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = f"UPDATE {TABLE_NAME} SET Booking_Status = %s WHERE Booking_ID = %s"
        cursor.execute(query, (new_status, booking_id))
        connection.commit()

        if cursor.rowcount > 0:
            print(f"\n[SUCCESS] Booking updated! Affected rows: {cursor.rowcount}")
        else:
            print(f"\n[WARNING] No record found with Booking ID: {booking_id}")
    except Error as e:
        print(f"\n[ERROR] Update Failed: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def delete_booking(booking_id):
    """Deletes a record based on its Booking ID."""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = f"DELETE FROM {TABLE_NAME} WHERE Booking_ID = %s"
        cursor.execute(query, (booking_id,))
        connection.commit()

        if cursor.rowcount > 0:
            print(f"\n[SUCCESS] Booking deleted! Affected rows: {cursor.rowcount}")
        else:
            print(f"\n[WARNING] No record found with Booking ID: {booking_id}")
    except Error as e:
        print(f"\n[ERROR] Delete Failed: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# =====================================================================
# 3. EXPORT DATA TO CSV & DISPLAY ALL
# =====================================================================

def display_all_bookings():
    """Fetches and displays all contents of the table in the console."""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(f"SELECT * FROM {TABLE_NAME}")
        rows = cursor.fetchall()

        if not rows:
            print("\nThe table is currently empty.")
            return False

        column_headers = [i[0] for i in cursor.description]

        print("\n" + "=" * 80)
        print(" | ".join(column_headers))
        print("=" * 80)
        for row in rows:
            print(" | ".join(str(item) for item in row))
        print("=" * 80)
        return True
    except Error as e:
        print(f"\n[ERROR] Failed to fetch data: {e}")
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def export_to_csv(file_name="ola_ride_booking_export.csv"):
    """Executes SELECT * and outputs all table content into a clean CSV file."""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(f"SELECT * FROM {TABLE_NAME}")
        rows = cursor.fetchall()

        column_headers = [i[0] for i in cursor.description]

        with open(file_name, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(column_headers)
            writer.writerows(rows)

        print(f"\n[SUCCESS] Export successful! Saved to '{file_name}'.")
    except Error as e:
        print(f"\n[ERROR] Export Failed: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# =====================================================================
# 4. CHART VISUALIZATION (Seaborn)
# =====================================================================

def chart_visualisation():
    """Fetches ride booking data and renders charts using Seaborn."""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(f"SELECT * FROM {TABLE_NAME}")
        rows = cursor.fetchall()
        column_headers = [i[0] for i in cursor.description]

        if not rows:
            print("\nThe table is currently empty. Nothing to visualize.")
            return

        df = pd.DataFrame(rows, columns=column_headers)

        print("\n--- Chart Options ---")
        print("a. Total Revenue by Vehicle Type (bar chart)")
        print("b. Booking Count by Pickup City (bar chart)")
        print("c. Ride Distance Distribution (histogram)")
        print("d. Total Fare by Vehicle Type per City (grouped bar chart)")
        print("e. Booking Status Breakdown (bar chart)")
        chart_choice = input("Choose a chart (a-e): ").strip().lower()

        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(10, 6))

        if chart_choice == 'a' and "Vehicle_Type" in df.columns and "Total_Fare" in df.columns:
            summary = df.groupby("Vehicle_Type")["Total_Fare"].sum().sort_values(ascending=False).reset_index()
            sns.barplot(data=summary, x="Vehicle_Type", y="Total_Fare", palette="viridis")
            plt.title("Total Revenue by Vehicle Type")
            plt.xlabel("Vehicle Type")
            plt.ylabel("Total Fare Revenue")
            plt.xticks(rotation=45, ha="right")
            out_file = "chart_revenue_by_vehicle_type.png"

        elif chart_choice == 'b' and "Pickup_City" in df.columns:
            summary = df["Pickup_City"].value_counts().reset_index()
            summary.columns = ["Pickup_City", "Booking_Count"]
            sns.barplot(data=summary, x="Pickup_City", y="Booking_Count", palette="magma")
            plt.title("Booking Count by Pickup City")
            plt.xlabel("Pickup City")
            plt.ylabel("Number of Bookings")
            plt.xticks(rotation=45, ha="right")
            out_file = "chart_bookings_by_city.png"

        elif chart_choice == 'c' and "Ride_Distance_KM" in df.columns:
            sns.histplot(df["Ride_Distance_KM"], bins=20, kde=True, color="teal")
            plt.title("Ride Distance Distribution")
            plt.xlabel("Ride Distance (KM)")
            plt.ylabel("Frequency")
            out_file = "chart_ride_distance_distribution.png"

        elif chart_choice == 'd' and "Vehicle_Type" in df.columns and "Pickup_City" in df.columns and "Total_Fare" in df.columns:
            summary = df.groupby(["Pickup_City", "Vehicle_Type"])["Total_Fare"].sum().reset_index()
            sns.barplot(data=summary, x="Pickup_City", y="Total_Fare", hue="Vehicle_Type")
            plt.title("Total Fare by Vehicle Type per City")
            plt.xlabel("Pickup City")
            plt.ylabel("Total Fare")
            plt.xticks(rotation=45, ha="right")
            plt.legend(title="Vehicle Type", bbox_to_anchor=(1.05, 1), loc="upper left")
            out_file = "chart_fare_by_vehicle_per_city.png"

        elif chart_choice == 'e' and "Booking_Status" in df.columns:
            summary = df["Booking_Status"].value_counts().reset_index()
            summary.columns = ["Booking_Status", "Count"]
            sns.barplot(data=summary, x="Booking_Status", y="Count", palette="crest")
            plt.title("Booking Status Breakdown")
            plt.xlabel("Booking Status")
            plt.ylabel("Count")
            plt.xticks(rotation=45, ha="right")
            out_file = "chart_booking_status_breakdown.png"

        else:
            print("\n[INVALID INPUT] Unrecognized chart option or missing required columns.")
            plt.close()
            return

        plt.tight_layout()
        plt.savefig(out_file, dpi=150)
        plt.close()
        print(f"\n[SUCCESS] Chart saved to '{out_file}'.")

    except Error as e:
        print(f"\n[ERROR] Chart Visualization Failed: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# =====================================================================
# INTERACTIVE USER OPTION CONSOLE
# =====================================================================
def user_interface_menu():
    # Make sure table is built before showing the menu
    manage_table_structure()

    while True:
        print("\n" + " OLA RIDE BOOKING DATABASE CONTROL PANEL ".center(60, "="))
        print("1. Add New Ride Booking")
        print("2. Update Booking Status")
        print("3. Delete Ride Booking")
        print("4. View All Bookings (SELECT *)")
        print("5. Export Database Rows to CSV File")
        print("6. Generate Chart Visualisation (Seaborn)")
        print("7. Exit Terminal Application")
        print("=" * 60)

        choice = input("Enter your selection (1-7): ").strip()

        if choice == '1':
            print("\n--- Enter Ride Booking Details ---")
            booking_id = input("Booking ID (e.g. B999999): ")
            ride_date = input("Ride Date (YYYY-MM-DD): ")
            ride_time = input("Ride Time (HH:MM:SS): ")
            pickup_city = input("Pickup City: ")
            pickup_location = input("Pickup Location: ")
            drop_location = input("Drop Location: ")
            customer_id = input("Customer ID: ")
            driver_id = input("Driver ID: ")
            vehicle_type = input("Vehicle Type (Auto/Bike/Mini/Prime Sedan/Prime SUV): ")
            ride_distance_km = float(input("Ride Distance (KM): "))
            ride_duration_minutes = int(input("Ride Duration (Minutes): "))
            base_fare = float(input("Base Fare: "))
            total_fare = float(input("Total Fare: "))
            payment_method = input("Payment Method (Cash/Card/UPI/Wallet): ")
            booking_status = input("Booking Status (Completed/Cancelled by Customer/Cancelled by Driver): ")

            insert_booking(booking_id, ride_date, ride_time, pickup_city, pickup_location,
                           drop_location, customer_id, driver_id, vehicle_type,
                           ride_distance_km, ride_duration_minutes, base_fare, total_fare,
                           payment_method, booking_status)

        elif choice == '2':
            print("\n--- Update Booking Status ---")
            b_id = input("Enter target Booking ID to alter: ").strip()
            new_status = input("Enter new Booking Status: ").strip()
            update_booking_status(b_id, new_status)

        elif choice == '3':
            print("\n--- Remove Ride Booking ---")
            b_id = input("Enter target Booking ID to drop: ").strip()
            confirm = input(f"Are you completely sure you want to drop {b_id}? (y/n): ").lower()
            if confirm == 'y':
                delete_booking(b_id)
            else:
                print("Operation aborted.")

        elif choice == '4':
            display_all_bookings()

        elif choice == '5':
            file_out = input("Enter output filename (Press Enter for default 'ola_ride_booking_export.csv'): ")
            if file_out.strip() == "":
                export_to_csv()
            else:
                export_to_csv(file_out.strip())

        elif choice == '6':
            chart_visualisation()

        elif choice == '7':
            print("\nShutting down control application loop. Goodbye!")
            break
        else:
            print("\n[INVALID INPUT] Selection out of boundaries. Choose an index from 1 to 7.")

if __name__ == "__main__":
    user_interface_menu()
