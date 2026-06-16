# ============================================================
#   OLA Ride Insights — Streamlit Web Application
#   Author: [Your Name]
#   Description: Interactive web app showing OLA ride analysis
# ============================================================

import streamlit as st
import pymysql
import pandas as pd
import plotly.express as px

# ── PAGE CONFIGURATION ────────────────────────────────────────
st.set_page_config(
    page_title="OLA Ride Insights",
    page_icon="🚗",
    layout="wide"
)

# ── DATABASE CONNECTION ───────────────────────────────────────
def get_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root123',
        database='ola_db'
    )
    return connection

# ── RUN QUERY FUNCTION ────────────────────────────────────────
def run_query(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# ── SIDEBAR NAVIGATION ────────────────────────────────────────
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Ola_Cabs_logo.svg/2560px-Ola_Cabs_logo.svg.png", width=150)
st.sidebar.title("OLA Ride Insights")
st.sidebar.markdown("---")

page = st.sidebar.selectbox("Navigate to:", [
    "🏠 Home",
    "📊 SQL Query Results",
    "🚗 Vehicle Analysis",
    "💰 Revenue Analysis",
    "⭐ Ratings Analysis"
])

# ══════════════════════════════════════════════════════════════
#   PAGE 1 — HOME
# ══════════════════════════════════════════════════════════════
if page == "🏠 Home":
    st.title("🚗 OLA Ride Insights Dashboard")
    st.markdown("### Welcome to the OLA Ride Analytics Platform")
    st.markdown("""
    This application provides interactive analysis of OLA ride-sharing data.
    Use the sidebar to navigate between different analysis sections.
    """)

    st.markdown("---")

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)

    total = run_query("SELECT COUNT(*) as total FROM ola_rides")
    success = run_query("SELECT COUNT(*) as total FROM ola_rides WHERE Booking_Status='Success'")
    revenue = run_query("SELECT SUM(Booking_Value) as total FROM ola_rides WHERE Booking_Status='Success'")
    cancelled = run_query("SELECT COUNT(*) as total FROM ola_rides WHERE Booking_Status='Canceled by Customer'")

    with col1:
        st.metric("Total Rides", f"{total['total'][0]:,}")
    with col2:
        st.metric("Successful Rides", f"{success['total'][0]:,}")
    with col3:
        st.metric("Total Revenue", f"₹{revenue['total'][0]:,}")
    with col4:
        st.metric("Customer Cancellations", f"{cancelled['total'][0]:,}")

    st.markdown("---")
    st.markdown("### Project Overview")
    st.info("""
    **Domain:** Ride-Sharing & Mobility Analytics

    **Tools Used:** Python, Pandas, MySQL, Power BI, Streamlit

    **Skills:** Data Cleaning, SQL Querying, Data Visualization, 
    Business Intelligence
    """)

# ══════════════════════════════════════════════════════════════
#   PAGE 2 — SQL QUERY RESULTS
# ══════════════════════════════════════════════════════════════
elif page == "📊 SQL Query Results":
    st.title("📊 SQL Query Results")
    st.markdown("All 10 SQL queries from the project with results.")
    st.markdown("---")

    query_option = st.selectbox("Select a Query:", [
        "Q1 - Successful Bookings",
        "Q2 - Average Ride Distance by Vehicle Type",
        "Q3 - Total Cancelled Rides by Customers",
        "Q4 - Top 5 Customers by Number of Rides",
        "Q5 - Rides Cancelled by Drivers (Personal & Car Issues)",
        "Q6 - Max & Min Driver Ratings for Prime Sedan",
        "Q7 - Rides with UPI Payment",
        "Q8 - Average Customer Rating by Vehicle Type",
        "Q9 - Total Revenue from Successful Rides",
        "Q10 - Incomplete Rides with Reason"
    ])

    queries = {
        "Q1 - Successful Bookings":
            "SELECT * FROM ola_rides WHERE Booking_Status='Success' LIMIT 100",

        "Q2 - Average Ride Distance by Vehicle Type":
            "SELECT Vehicle_Type, ROUND(AVG(Ride_Distance),2) AS Avg_Distance FROM ola_rides GROUP BY Vehicle_Type ORDER BY Avg_Distance DESC",

        "Q3 - Total Cancelled Rides by Customers":
            "SELECT COUNT(*) AS Total_Cancelled_by_Customer FROM ola_rides WHERE Booking_Status='Canceled by Customer'",

        "Q4 - Top 5 Customers by Number of Rides":
            "SELECT Customer_ID, COUNT(*) AS Total_Rides FROM ola_rides GROUP BY Customer_ID ORDER BY Total_Rides DESC LIMIT 5",

        "Q5 - Rides Cancelled by Drivers (Personal & Car Issues)":
            "SELECT COUNT(*) AS Cancelled_Personal_Car FROM ola_rides WHERE Canceled_Rides_by_Driver='Personal & Car related issue'",

        "Q6 - Max & Min Driver Ratings for Prime Sedan":
            "SELECT MAX(Driver_Ratings) AS Max_Rating, MIN(Driver_Ratings) AS Min_Rating FROM ola_rides WHERE Vehicle_Type='Prime Sedan' AND Booking_Status='Success'",

        "Q7 - Rides with UPI Payment":
            "SELECT Booking_ID, Customer_ID, Booking_Value, Payment_Method FROM ola_rides WHERE Payment_Method='UPI' LIMIT 100",

        "Q8 - Average Customer Rating by Vehicle Type":
            "SELECT Vehicle_Type, ROUND(AVG(Customer_Rating),2) AS Avg_Customer_Rating FROM ola_rides WHERE Booking_Status='Success' GROUP BY Vehicle_Type ORDER BY Avg_Customer_Rating DESC",

        "Q9 - Total Revenue from Successful Rides":
            "SELECT SUM(Booking_Value) AS Total_Revenue FROM ola_rides WHERE Booking_Status='Success'",

        "Q10 - Incomplete Rides with Reason":
            "SELECT Booking_ID, Customer_ID, Vehicle_Type, Incomplete_Rides_Reason FROM ola_rides WHERE Incomplete_Rides='Yes' LIMIT 100"
    }

    selected_query = queries[query_option]
    st.code(selected_query, language='sql')

    df = run_query(selected_query)
    st.success(f"Query returned {len(df)} rows")
    st.dataframe(df, use_container_width=True)

# ══════════════════════════════════════════════════════════════
#   PAGE 3 — VEHICLE ANALYSIS
# ══════════════════════════════════════════════════════════════
elif page == "🚗 Vehicle Analysis":
    st.title("🚗 Vehicle Type Analysis")
    st.markdown("---")

    # Chart 1 - Average ride distance by vehicle type
    df1 = run_query("""
        SELECT Vehicle_Type, ROUND(AVG(Ride_Distance),2) AS Avg_Distance 
        FROM ola_rides 
        GROUP BY Vehicle_Type 
        ORDER BY Avg_Distance DESC
    """)
    fig1 = px.bar(df1, x='Avg_Distance', y='Vehicle_Type',
                  orientation='h',
                  title='Average Ride Distance by Vehicle Type',
                  color='Avg_Distance',
                  color_continuous_scale='Blues')
    st.plotly_chart(fig1, use_container_width=True)

    # Chart 2 - Ride count by vehicle type
    df2 = run_query("""
        SELECT Vehicle_Type, COUNT(*) AS Total_Rides 
        FROM ola_rides 
        GROUP BY Vehicle_Type 
        ORDER BY Total_Rides DESC
    """)
    fig2 = px.pie(df2, values='Total_Rides', names='Vehicle_Type',
                  title='Ride Distribution by Vehicle Type',
                  hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════════════════════════════
#   PAGE 4 — REVENUE ANALYSIS
# ══════════════════════════════════════════════════════════════
elif page == "💰 Revenue Analysis":
    st.title("💰 Revenue Analysis")
    st.markdown("---")

    # Chart 1 - Revenue by payment method
    df1 = run_query("""
        SELECT Payment_Method, SUM(Booking_Value) AS Total_Revenue 
        FROM ola_rides 
        WHERE Payment_Method != 'Not Applicable'
        GROUP BY Payment_Method 
        ORDER BY Total_Revenue DESC
    """)
    fig1 = px.bar(df1, x='Payment_Method', y='Total_Revenue',
                  title='Revenue by Payment Method',
                  color='Total_Revenue',
                  color_continuous_scale='Greens')
    st.plotly_chart(fig1, use_container_width=True)

    # Chart 2 - Top 5 customers
    df2 = run_query("""
        SELECT Customer_ID, SUM(Booking_Value) AS Total_Spent 
        FROM ola_rides 
        GROUP BY Customer_ID 
        ORDER BY Total_Spent DESC 
        LIMIT 5
    """)
    fig2 = px.bar(df2, x='Customer_ID', y='Total_Spent',
                  title='Top 5 Customers by Total Booking Value',
                  color='Total_Spent',
                  color_continuous_scale='Blues')
    st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════════════════════════════
#   PAGE 5 — RATINGS ANALYSIS
# ══════════════════════════════════════════════════════════════
elif page == "⭐ Ratings Analysis":
    st.title("⭐ Ratings Analysis")
    st.markdown("---")

    # Chart 1 - Average ratings by vehicle type
    df1 = run_query("""
        SELECT Vehicle_Type, 
               ROUND(AVG(Driver_Ratings),2) AS Avg_Driver_Rating,
               ROUND(AVG(Customer_Rating),2) AS Avg_Customer_Rating
        FROM ola_rides 
        WHERE Booking_Status='Success'
        GROUP BY Vehicle_Type
    """)
    fig1 = px.bar(df1, x='Vehicle_Type',
                  y=['Avg_Driver_Rating', 'Avg_Customer_Rating'],
                  title='Average Driver vs Customer Ratings by Vehicle Type',
                  barmode='group')
    st.plotly_chart(fig1, use_container_width=True)

    # Chart 2 - Driver ratings distribution
    df2 = run_query("""
        SELECT Driver_Ratings, COUNT(*) AS Count 
        FROM ola_rides 
        WHERE Booking_Status='Success'
        GROUP BY Driver_Ratings 
        ORDER BY Driver_Ratings
    """)
    fig2 = px.bar(df2, x='Driver_Ratings', y='Count',
                  title='Driver Ratings Distribution',
                  color='Count',
                  color_continuous_scale='Oranges')
    st.plotly_chart(fig2, use_container_width=True)
    
    
    
    
    
    