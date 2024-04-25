from library_utils import get_sf_cur
import pandas as pd
from datetime import datetime

"""
App Name: Fiserv PbP Account Balance Reconciliation

Description:
This application is responsible for automating the reconciliation of account balances 
between the Fiserv system and the PbP system. The app performs the following tasks:

1. Connects to the 'WHEELER' database environment specified by the 'ENVIRONMENT' variable.
2. Fetches account balance data using pre-defined SQL queries for:
    - Matching balances between Fiserv and PbP
    - Mismatches in balances between the two systems
3. Creates dataframes from the fetched data.
4. Checks the dataframes for any records. If records are found:
    - The type (matches or mismatches) and the number of records are stored.
    - Data is exported to an Excel file, which is saved with a timestamped filename.
5. Depending on the reconciliation results (all matched, all mismatched, or a mix of both),
   an appropriate email is drafted. The email content is generated dynamically, including a subject 
   line, main message, and sometimes an attached dad joke or an emoji for added context.
6. The email is sent to a pre-defined list of recipients with an option to attach the exported Excel files.

Author: [Your Name]
Date Created: [Date]
Last Updated: [Last Updated Date]
"""

# Set the environment variable for database operations. Defaulted to the 'DEV' environment.
ENVIRONMENT = 'DEV'

# Establish a connection to the WHEELER database (specific to the environment) 
# and retrieve both the cursor and connection object.
wheeler_cur, wheeler_con = get_sf_cur(f'WHEELER-{ENVIRONMENT}')

# Configuration dictionary to store SQL queries and other related information 
# for both account balance matches and mismatches.
config = {
    # Configuration for fetching matched account balances.
    "balance_matches":
        {
            # SQL query to fetch matched account balances between Fiserv and PbP systems.
            # It retrieves account numbers, balances, and file datetime from both systems 
            # where account balances are the same.
            "sql": """
                select 
                    CAST(ps.ACCOUNT_NUMBER as varchar) AS ACCOUNT_NUMBER_PBP, 
                    CAST(ra.ACCOUNT_NUMBER as varchar) AS FISERV_ACCOUNT,
                    ps.ACCOUNT_BALANCE as PBP_SHADOW_BALANCE,
                    ra.ACCOUNT_BALANCE as FISERV_BALANCE,
                    ps.FILE_DATETIME as PbP_File_datetime,
                    ra.FILE_DATETIME as FISERV_FILE_DATETIME
                from 
                    "RA_DB_DEV"."LIVE"."PBP_SHADOW_BALANCE" ps 
                join 
                    "RA_DB_DEV"."LIVE"."RA_SHADOW_BALANCE" ra on ps.ACCOUNT_NUMBER = ra.PBP_ACCOUNT_NUMBER
                where 
                    ps.ACCOUNT_BALANCE = ra.ACCOUNT_BALANCE
                group by
                    CAST(ps.ACCOUNT_NUMBER as varchar), 
                    CAST(ra.ACCOUNT_NUMBER as varchar),
                    ps.ACCOUNT_BALANCE,
                    ra.ACCOUNT_BALANCE,
                    ps.FILE_DATETIME,
                    ra.FILE_DATETIME""",
            # Flag to check if there are any records returned by the query.
            "there_are_records": False,
            # Count of records returned by the query.
            "num_records": 0
        },
    # Configuration for fetching mismatched account balances.
    "balance_mismatches":
        {
            # SQL query to fetch mismatched account balances between Fiserv and PbP systems.
            # It retrieves account numbers, balances, variance in balances, and file datetime 
            # from both systems where account balances are different.
            "sql": """
                select
                    CAST(ps.ACCOUNT_NUMBER as varchar) AS ACCOUNT_NUMBER_PBP, 
                    CAST(ra.ACCOUNT_NUMBER as varchar) AS FISERV_ACCOUNT,
                    ps.ACCOUNT_BALANCE as PBP_SHADOW_BALANCE,
                    ra.ACCOUNT_BALANCE as FISERV_BALANCE,
                    ra.ACCOUNT_BALANCE - ps.ACCOUNT_BALANCE as "Variance0",
                    ps.FILE_DATETIME as PBP_File_Datetime,
                    ra.FILE_DATETIME as FISERV_FILE_DATETIME
                from 
                    "RA_DB_DEV"."LIVE"."PBP_SHADOW_BALANCE" ps 
                join
                    "RA_DB_DEV"."LIVE"."RA_SHADOW_BALANCE" ra on ps.ACCOUNT_NUMBER=ra.PBP_ACCOUNT_NUMBER
                where 
                    ps.ACCOUNT_BALANCE <> ra.ACCOUNT_BALANCE
                group by
                    CAST(ps.ACCOUNT_NUMBER as varchar), 
                    CAST(ra.ACCOUNT_NUMBER as varchar),
                    ps.ACCOUNT_BALANCE,
                    ra.ACCOUNT_BALANCE,
                    ra.ACCOUNT_BALANCE - ps.ACCOUNT_BALANCE,
                    ps.FILE_DATETIME,
                    ra.FILE_DATETIME""",
            # Flag to check if there are any records returned by the query.
            "there_are_records": False,
            # Count of records returned by the query.
            "num_records": 0
        }
}





def get_df(type):
    """
    Retrieves data from the database based on the type of comparison (matches or mismatches) 
    and returns it as a Pandas DataFrame.

    Parameters:
    - type (str): Type of comparison. Expected values are keys in the config dictionary such as "balance_matches" or "balance_mismatches".

    Returns:
    - DataFrame: Contains the result of the executed SQL query.
    """
    
    # Extract the SQL query from the config dictionary based on the provided type
    sql = config[type]['sql']
    
    # Execute the SQL query using the wheeler_cur cursor object
    wheeler_cur.execute(sql)
    
    # Convert the result of the executed query into a Pandas DataFrame
    df = pd.DataFrame(wheeler_cur.fetchall())
    
    return df



# Initialize an empty list to store file paths of the generated Excel attachments.
attachments = []

# Iterate through each type (e.g. "balance_matches" or "balance_mismatches") in the config dictionary.
for type, configs in config.items():
    
    # Retrieve the dataframe for the current type using the get_df function.
    df = get_df(type)
    
    # Check if the dataframe has any records.
    if len(df) > 0:
        
        # Update the 'there_are_records' flag to True for the current type in the config dictionary.
        config[type]['there_are_records'] = True
        
        # Update the 'num_records' with the number of records in the dataframe for the current type in the config dictionary.
        config[type]['num_records'] = len(df)
        
        # Define the path where the Excel file will be saved. The filename will be based on the type and current datetime.
        local_file = f'/home/admin.eng/python/automations/fiserv_recon/{type}_{datetime.now().strftime("%Y%m%d%H%M%S")}.xlsx'
        
        # Save the dataframe as an Excel file at the specified path.
        df.to_excel(local_file, index=False)
        
        # Append the file path to the attachments list.
        attachments.append(local_file)


# Check if there are any attachments generated from the previous block.
if len(attachments) > 0:
    # Import required libraries for sending an email and interacting with the OpenAI API.
    from library_graph_api_calls import send_email
    from library_openai import send_chat
    
    # Calculate the total number of records by adding matches and mismatches.
    total_records = config['balance_matches']['num_records'] + config['balance_mismatches']['num_records']
    
    # Calculate the percentage of matches to the total number of records.
    percent_matched = round((config['balance_matches']['num_records'] / total_records)*100, 2)
    
    # Check various conditions to decide the subject and message for the email.
    # Case 1: All account balances matched
    if config['balance_matches']['there_are_records'] and not config['balance_mismatches']['there_are_records']:
        # Define email subject and message.
        subject = f'Daily Fiserv PbP Account Balance Reconciliation - All Matched'
        message = f'Good news - here were no mismatches!'
        # Construct a prompt for OpenAI to generate an appropriate email body.
        openai_prompt = """...""" # [Truncated for brevity]
    
    # Case 2: None of the account balances matched.
    elif not config['balance_matches']['there_are_records'] and config['balance_mismatches']['there_are_records']:
        # Define email subject and message.
        subject = f'Daily Fiserv PbP Account Balance Reconciliation'
        message = f'Attached are today\'s balance mismatches. Today is not what I would call a "good day" - no account balances matched ☹'
        # Construct a prompt for OpenAI to generate an appropriate email body.
        openai_prompt = """...""" # [Truncated for brevity]
    
    # Case 3: Some account balances matched, others did not.
    else:
        # Define email subject and message.
        subject = f'Daily Fiserv PbP Account Balance Reconciliation'
        message = f'Attached are today\'s balance mismatches. There were {config["balance_matches"]["num_records"]} accounts that matched and {config["balance_mismatches"]["num_records"]} that didn\'t match for a match rate of {percent_matched}%'
        # Construct a prompt for OpenAI to generate an appropriate email body.
        openai_prompt = """...""" # [Truncated for brevity]
    
    # Define the list of email recipients and cc recipients.
    to_recipients = ['filip.watorek@pb.com','thomas.coon@pb.com', 'jaclyn.desroches@pb.com', 'ramprakash.achuthan@pb.com', 'edward.dyroff@pb.com', 'kimberly.rice@pb.com', 'val.cuccurullo@pb.com']
    cc_recipients = ['jordan.buser@pb.com']
    
    # Get the message generated by OpenAI using the defined prompt.
    openai_message = send_chat(openai_prompt)
    if not openai_message:
        pass
    else:
        message = openai_message
    
    # Send the email using the send_email function.
    send_email('otis', to_recipients, subject, message, cc_recipients=cc_recipients, attachments=attachments)
    print('email sent')



